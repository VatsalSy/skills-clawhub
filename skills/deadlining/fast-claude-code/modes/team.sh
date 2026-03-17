#!/bin/bash
# Team Mode - Start a Claude Code team session with callback
# Usage: team.sh --project <path> --template <name> --task <description> [--callback <type>]
#
# This script is called by OpenClaw after selecting the appropriate template.
# It does NOT auto-select templates - that's done by OpenClaw (LLM).
#
# Flow:
#   User → OpenClaw (LLM) → Understands task → Selects template → Calls this script
#                                                    ↓
#                           team.sh --template xxx --task "xxx"
#                                                    ↓
#                                     Installs hooks + Generates spawn prompt

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BASE_DIR="$(dirname "$SCRIPT_DIR")"
TEMPLATES_DIR="$BASE_DIR/templates"

# Default values
PROJECT_DIR=""
TASK=""
TEMPLATE=""
CALLBACK="openclaw"
PERMISSION_MODE="auto"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --project)
            PROJECT_DIR="$2"
            shift 2
            ;;
        --task)
            TASK="$2"
            shift 2
            ;;
        --template)
            TEMPLATE="$2"
            shift 2
            ;;
        --callback)
            CALLBACK="$2"
            shift 2
            ;;
        --permission-mode)
            PERMISSION_MODE="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Validate required arguments
if [[ -z "$PROJECT_DIR" ]]; then
    echo "Error: --project is required"
    exit 1
fi

# Validate permission mode
if [[ "$PERMISSION_MODE" != "plan" && "$PERMISSION_MODE" != "auto" ]]; then
    echo "Error: --permission-mode must be 'plan' or 'auto'"
    exit 1
fi

# Expand ~ to home directory
PROJECT_DIR="${PROJECT_DIR/#\~/$HOME}"

if [[ ! -d "$PROJECT_DIR" ]]; then
    echo "Error: Project directory does not exist: $PROJECT_DIR"
    exit 1
fi

# Set default template if not specified
if [[ -z "$TEMPLATE" ]]; then
    if [[ -n "$TASK" ]]; then
        # Task provided but no template - OpenClaw should have chosen one
        # Use parallel-review as safe default
        TEMPLATE="parallel-review"
        log_warn "No template specified, using 'parallel-review' as default."
        log_warn "Tip: Let OpenClaw choose the template based on your task."
    else
        # No task and no template - use parallel-review as default
        TEMPLATE="parallel-review"
        log_info "No template specified, using 'parallel-review' as default."
    fi
fi

# Check if CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS is set
if [[ -z "${CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS:-}" ]]; then
    log_warn "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS is not set"
    log_warn "Team mode may not work without it"
    log_warn "Run: export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1"
    echo ""
fi

# Check if jq is available (required for hooks)
if ! command -v jq &> /dev/null; then
    log_error "jq is required for Team mode but not installed"
    log_error "Install: brew install jq  (macOS)"
    log_error "        sudo apt-get install jq  (Ubuntu/Debian)"
    exit 1
fi

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() {
    echo -e "${BLUE}ℹ${NC} $*"
}

log_success() {
    echo -e "${GREEN}✅${NC} $*"
}

log_warn() {
    echo -e "${YELLOW}⚠️${NC} $*"
}

log_info "Starting Team mode..."
log_info "Project: $PROJECT_DIR"
log_info "Template: $TEMPLATE"
log_info "Permission mode: $PERMISSION_MODE"
log_info ""

if [[ "$PERMISSION_MODE" == "auto" ]]; then
    log_warn "⚠️  Auto mode uses --dangerously-skip-permissions"
fi

# Install hooks for team completion detection
log_info "Installing completion hooks..."
HOOKS_DIR="$PROJECT_DIR/.claude/hooks"
mkdir -p "$HOOKS_DIR"

# Create on-stop hook
cat > "$HOOKS_DIR/on-stop.sh" << EOF
#!/bin/bash
# Team completion detection hook
# This hook fires when Claude Code stops

INPUT=\$(cat)
SESSION_ID=\$(echo "\$INPUT" | jq -r '.session_id // "unknown"')
CWD=\$(echo "\$INPUT" | jq -r '.cwd // "unknown")

# Find team output files and aggregate them
TEAM_OUTPUTS=""
while IFS= read -r -d '' file; do
    if [[ -f "\$file" ]]; then
        filename=\$(basename "\$file")
        TEAM_OUTPUTS="\$TEAM_OUTPUTS\n\n=== \${filename} ===\n\$(cat "\$file")"
    fi
done < <(find "\$CWD" -maxdepth 1 -type f \
    \\( -name "findings-*.md" \
       -o -name "hypothesis-*-investigation.md" \
       -o -name "*-implementation.md" \
       -o -name "*-analysis.md" \
       -o -name "synthesis-*.md" \
       -o -name "debate-transcript.md" \
       -o -name "root-cause-conclusion.md" \
       -o -name "integration-summary.md" \
       -o -name "aggregated-results.md" \
       -o -name "summary-report.md" \\) \
    -print0)

# Trigger callback with outputs
"$BASE_DIR/callbacks/$CALLBACK.sh" \\
    --status done \\
    --mode team \\
    --task "team-session-\$SESSION_ID" \\
    --message "Team session completed in \$CWD" \\
    --output "\$TEAM_OUTPUTS"
EOF

chmod +x "$HOOKS_DIR/on-stop.sh"

# Create or update .claude/settings.json with hooks configuration
SETTINGS_FILE="$PROJECT_DIR/.claude/settings.json"
HOOKS_CONFIG=$(cat <<'HOOKSJSON'
{
  "Stop": [
    {
      "matcher": "",
      "hooks": [
        {
          "type": "command",
          "command": ".claude/hooks/on-stop.sh"
        }
      ]
    }
  ]
}
HOOKSJSON
)

mkdir -p "$PROJECT_DIR/.claude"
if [ -f "$SETTINGS_FILE" ]; then
    # Merge hooks into existing settings
    EXISTING=$(cat "$SETTINGS_FILE")
    echo "$EXISTING" | jq --argjson hooks "$HOOKS_CONFIG" '.hooks = (.hooks // {}) + $hooks' > "$SETTINGS_FILE.tmp"
    mv "$SETTINGS_FILE.tmp" "$SETTINGS_FILE"
else
    # Create new settings file with hooks
    jq -n --argjson hooks "$HOOKS_CONFIG" '$hooks' > "$SETTINGS_FILE"
fi

log_success "Hooks installed to $HOOKS_DIR/"
log_info "Settings updated: $SETTINGS_FILE"
log_info ""

# Generate spawn prompt based on task
SPAWN_PROMPT=""
if [[ -n "$TASK" ]]; then
    log_info "Starting Claude Code in Team mode..."
    log_info "Task: $TASK"
    log_info "Template: $TEMPLATE"
    log_info ""

    # Get template-specific spawn prompt
    if [[ -f "$TEMPLATES_DIR/$TEMPLATE.sh" ]]; then
        SPAWN_PROMPT=$(bash "$TEMPLATES_DIR/$TEMPLATE.sh")
        # Substitute variables using sed (handles special chars correctly)
        SPAWN_PROMPT=$(echo "$SPAWN_PROMPT" | sed "s/\${TASK_DESCRIPTION}/$TASK/g")
        SPAWN_PROMPT=$(echo "$SPAWN_PROMPT" | sed "s|\${TARGET_DIR}|$PROJECT_DIR|g")
        # Integrate CC_CALLBACK_DONE into the final reporting step
        # Replace "Report completion with summary" with instructions to output marker
        SPAWN_PROMPT=$(echo "$SPAWN_PROMPT" | sed 's/Report completion with summary/Report completion with summary, then output exactly CC_CALLBACK_DONE/')
    else
        log_warn "Template not found: $TEMPLATE, using default"
        SPAWN_PROMPT="I need to complete a complex task using a team approach.

Task: ${TASK}
Target: ${PROJECT_DIR}

Template approach: ${TEMPLATE}

Please spawn a team to handle this task efficiently. Consider:
1. What roles/teammates are needed for this task
2. How to divide the work to avoid conflicts
3. What each teammate should focus on
4. How to coordinate and synthesize results

Use delegate mode: I coordinate, teammates execute.

When ready, spawn the team and begin working on the task."
    fi

    log_info "Spawning team..."
    log_info ""
else
    log_error "Error: --task is required for Team mode"
    log_info "Team mode requires a task description to spawn the team."
    exit 1
fi

# Change to project directory
cd "$PROJECT_DIR"

# Execute team spawn using tmux (PTY mode required for agent teams)
log_info "Team will work on the task and exit when complete."
log_info "Completion will be detected by hooks automatically."
log_info ""
log_info "⏳ Team execution in progress (this may take some time)..."
log_info "    No output during this time is normal - agents are working."
log_info ""

# Create unique session name for this team run
SESSION="cc-team-$(date +%s)"
TMUX_SERVER="cc"

# Kill existing session if any
tmux -L "$TMUX_SERVER" kill-session -t "$SESSION" 2>/dev/null || true

# Create tmux session in project directory
tmux -L "$TMUX_SERVER" new-session -d -s "$SESSION" -c "$PROJECT_DIR"
sleep 0.5

# Start Claude Code (same as interactive.sh)
if [[ "$PERMISSION_MODE" == "auto" ]]; then
    CLAUDE_CMD="claude --dangerously-skip-permissions"
else
    CLAUDE_CMD="claude --permission-mode $PERMISSION_MODE"
fi

tmux -L "$TMUX_SERVER" send-keys -t "$SESSION" "$CLAUDE_CMD" Enter
sleep 4

# Auto-accept safety confirmation if using auto mode
if [[ "$PERMISSION_MODE" == "auto" ]]; then
    OUTPUT=$(tmux -L "$TMUX_SERVER" capture-pane -p -t "$SESSION" 2>/dev/null || echo "")
    # Check for new safety confirmation (current version)
    if grep -q "Yes, I trust this folder" <<< "$OUTPUT"; then
        log_info "Auto-accepting safety confirmation..."
        tmux -L "$TMUX_SERVER" send-keys -t "$SESSION" 1
        sleep 0.5
        tmux -L "$TMUX_SERVER" send-keys -t "$SESSION" Enter
        sleep 5  # Give Claude Code time to fully start
    # Check for old permissions warning (previous version)
    elif grep -q "Yes, I accept" <<< "$OUTPUT"; then
        log_info "Auto-accepting permissions warning..."
        tmux -L "$TMUX_SERVER" send-keys -t "$SESSION" 2
        sleep 0.3
        tmux -L "$TMUX_SERVER" send-keys -t "$SESSION" Enter
        sleep 4
    fi
fi

# Send spawn prompt via temp file (handles multi-line)
TMPFILE=$(mktemp /tmp/cc-spawn-XXXXXX.txt)
printf '%s' "$SPAWN_PROMPT" > "$TMPFILE"
tmux -L "$TMUX_SERVER" load-buffer "$TMPFILE"
tmux -L "$TMUX_SERVER" paste-buffer -t "$SESSION"
rm -f "$TMPFILE"
sleep 0.3
tmux -L "$TMUX_SERVER" send-keys -t "$SESSION" Enter

log_info "✅ Team spawn prompt sent"

# Monitor session for completion (wait for synthesis file)
log_info "Waiting for team to complete..."
ELAPSED=0
# Default timeout: 1 hour (3600s) for complex team tasks
# Can be overridden with TEAM_TIMEOUT env var
# Examples:
#   Quick testing (90s): TEAM_TIMEOUT=90
#   Medium tasks (10min): TEAM_TIMEOUT=600
#   Complex tasks (30min): TEAM_TIMEOUT=1800
#   Very complex tasks (1h): TEAM_TIMEOUT=3600 (default)
MAX_WAIT=${TEAM_TIMEOUT:-3600}

while [[ $ELAPSED -lt $MAX_WAIT ]]; do
    # Check if session still exists
    if ! tmux -L "$TMUX_SERVER" has-session -t "$SESSION" 2>/dev/null; then
        log_info "Team session ended"
        break
    fi

    # Check for completion (synthesis file exists)
    if [[ -f "$PROJECT_DIR/synthesis-review.md" ]] \
       || [[ -f "$PROJECT_DIR/root-cause-conclusion.md" ]] \
       || [[ -f "$PROJECT_DIR/integration-summary.md" ]] \
       || [[ -f "$PROJECT_DIR/aggregated-results.md" ]]; then
        log_success "✅ Team completed (synthesis file detected)"
        # Give it a moment to finalize
        sleep 2
        # Send /exit to trigger hooks, then wait for graceful shutdown
        tmux -L "$TMUX_SERVER" send-keys -t "$SESSION" "/exit" Enter
        sleep 3
        # Kill session if still exists
        tmux -L "$TMUX_SERVER" kill-session -t "$SESSION" 2>/dev/null || true
        break
    fi

    sleep 2
    ((ELAPSED+=2))
done

# Final check
if [[ $ELAPSED -ge $MAX_WAIT ]]; then
    log_warn "⏰ Team session timed out after ${MAX_WAIT}s"
    EXIT_CODE=124
    # Send /exit to trigger hooks, then wait for graceful shutdown
    tmux -L "$TMUX_SERVER" send-keys -t "$SESSION" "/exit" Enter 2>/dev/null || true
    sleep 3
    # Force kill if still exists
    tmux -L "$TMUX_SERVER" kill-session -t "$SESSION" 2>/dev/null || true
fi

# Team mode completion is handled by hooks, so we just report the exit
if [[ ${EXIT_CODE:-0} -eq 0 ]]; then
    log_success "✅ Team session completed successfully"
elif [[ ${EXIT_CODE:-0} -eq 124 ]]; then
    # 124 is the exit code for timeout
    log_warn "⏰ Team session timed out after ${TEAM_TIMEOUT}s"
    log_info "    This is normal - team tasks may take longer than expected"
    log_info "    Hooks will still be triggered on exit"
else
    log_warn "Team session exited with code ${EXIT_CODE:-1}"
fi

# Exit with the same code
exit ${EXIT_CODE:-0}
