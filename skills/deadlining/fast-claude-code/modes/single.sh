#!/bin/bash
# Single Mode - Run a single Claude Code task with callback
# Usage: single.sh --task <prompt> --project <path> [--permission-mode plan|auto] [--callback <type>]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BASE_DIR="$(dirname "$SCRIPT_DIR")"

# Default values
TASK=""
PROJECT_DIR=""
PERMISSION_MODE="auto"
CALLBACK="openclaw"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --task)
            TASK="$2"
            shift 2
            ;;
        --project)
            PROJECT_DIR="$2"
            shift 2
            ;;
        --permission-mode)
            PERMISSION_MODE="$2"
            shift 2
            ;;
        --callback)
            CALLBACK="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Validate required arguments
if [[ -z "$TASK" ]]; then
    echo "Error: --task is required"
    exit 1
fi

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

log_error() {
    echo -e "${RED}❌${NC} $*"
}

log_warn() {
    echo -e "${YELLOW}⚠️${NC} $*"
}

# Build task with completion protocol
# We ask Claude to output a marker when done, then we detect it and trigger callback
TASK_WITH_CALLBACK="$TASK

When the task is fully completed, output exactly:

CC_CALLBACK_DONE

If you need to manually trigger completion, type: TASK_COMPLETE
When you receive TASK_COMPLETE, output exactly:

CC_CALLBACK_DONE"

log_info "Starting Single mode..."
log_info "Project: $PROJECT_DIR"
log_info "Permission mode: $PERMISSION_MODE"

if [[ "$PERMISSION_MODE" == "auto" ]]; then
    log_warn "⚠️  Auto mode uses --dangerously-skip-permissions"
    log_warn "   Claude Code will run all tools without confirmation"
    log_warn "   Only use in trusted environments with version-controlled code"
fi

# Run Claude Code in non-interactive mode
cd "$PROJECT_DIR"

log_info "Running Claude Code..."

# Map permission modes to Claude Code values
# Note: We use --dangerously-skip-permissions directly for auto mode to avoid confirmation prompt
case "$PERMISSION_MODE" in
    plan)
        CLAUDE_CMD="claude -p --permission-mode plan"
        ;;
    auto)
        CLAUDE_CMD="claude -p --dangerously-skip-permissions"
        ;;
    *)
        echo "Error: --permission-mode must be 'plan' or 'auto'"
        exit 1
        ;;
esac

# Capture output and check for completion
OUTPUT=$($CLAUDE_CMD "$TASK_WITH_CALLBACK" 2>&1) || EXIT_CODE=$?

# Check if CC_CALLBACK_DONE was output
if grep -q "CC_CALLBACK_DONE" <<< "$OUTPUT"; then
    log_success "Task completed successfully"

    # Extract task output (everything before LAST CC_CALLBACK_DONE)
    # Extract from line 1 to CC_CALLBACK_DONE, then remove last line (CC_CALLBACK_DONE)
    TASK_OUTPUT=$(echo "$OUTPUT" | sed -n '1,/CC_CALLBACK_DONE/p' | sed '$d')

    # Trigger callback with output
    "$BASE_DIR/callbacks/$CALLBACK.sh" \
        --status done \
        --mode single \
        --task "$TASK" \
        --output "$TASK_OUTPUT"
    exit 0
else
    # Check for specific error patterns
    if grep -qi "permission" <<< "$OUTPUT"; then
        log_error "Task failed: Permission required"
        log_info "Try using --permission-mode auto (use with caution)"
    elif grep -qiE "error|failed" <<< "$OUTPUT"; then
        log_error "Task failed with errors"
    else
        log_warn "Task completed but CC_CALLBACK_DONE marker not found"
        log_info "This may be normal - Claude may have completed without outputting the marker"
    fi

    # Show output for debugging
    echo ""
    echo "--- Claude Code Output ---"
    echo "$OUTPUT"
    echo "--- End Output ---"
    echo ""

    # Try to trigger error callback
    "$BASE_DIR/callbacks/$CALLBACK.sh" \
        --status error \
        --mode single \
        --task "$TASK" \
        --message "CC_CALLBACK_DONE marker not found in output" \
        --output "$OUTPUT"

    # Exit with the original exit code if available, otherwise 1
    exit ${EXIT_CODE:-1}
fi
