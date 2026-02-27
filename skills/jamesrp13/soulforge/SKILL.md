---
name: soulforge
description: "Dispatch multi-step coding workflows to Claude Code CLI or Codex CLI from YAML definitions via a persistent background daemon. Use when: (1) implementing a feature end-to-end (plan → implement → verify → PR), (2) delegating coding tasks to run in the background while you do other work, (3) running development workflows that need human review checkpoints, (4) automating feature branch creation, implementation, and PR submission. Requires the @ghostwater/soulforge npm package."
metadata:
  {
    "openclaw":
      {
        "emoji": "🔥",
        "requires": { "bins": ["soulforge", "claude", "gh"], "env": [] },
        "install":
          [
            {
              "id": "npm",
              "kind": "npm",
              "package": "@ghostwater/soulforge",
              "global": true,
              "bins": ["soulforge"],
              "label": "Install Soulforge CLI (npm)",
            },
          ],
      },
  }
---

# Soulforge

Soulforge is a daemon-based workflow engine that dispatches coding steps to executor CLIs (Claude Code, Codex) and pauses at human review checkpoints.

## Install & Start

```bash
npm install -g @ghostwater/soulforge
soulforge daemon start
```

The daemon auto-starts on `soulforge run` if not already running.

## Quick Start

```bash
# Run a feature-dev workflow
soulforge run feature-dev "Add user authentication with JWT tokens" \
  --workdir /path/to/project

# Run a bugfix workflow
soulforge run bugfix "Fix race condition in session handler" \
  --workdir /path/to/project \
  --var build_cmd="npm run build" \
  --var test_cmd="npm test"
```

`--workdir` is **required** — it must point to an existing directory. Soulforge creates a git worktree from it automatically.

> ⚠️ `--var repo=` is no longer supported. Use `--workdir` instead.

## Built-in Workflows

| Workflow | Steps | What it does |
|----------|-------|-------------|
| `feature-dev` | plan → review → implement (loop) → verify → test → PR → code-review → gate → final-review | Full feature development with story decomposition |
| `bugfix` | diagnose → review-diagnosis → fix → verify → PR → code-review → gate → final-review | Surgical bugfix with failing test first |

Both workflows default to `codex-cli` executor with `gpt-5.3-codex` model.

## Key Commands

| Command | What it does |
|---------|-------------|
| `soulforge run <workflow> "<task>" [flags]` | Start a workflow run |
| `soulforge status [<query>]` | Check run status (ID prefix or task substring) |
| `soulforge runs` | List all runs |
| `soulforge approve <run-id> [--message "..."]` | Approve a checkpoint |
| `soulforge reject <run-id> --reason "…"` | Reject with feedback (rewinds to prior step) |
| `soulforge complete --run-id <id> --step-id <id> --data '<json>'` | Complete a structured-output step |
| `soulforge cancel <run-id>` | Cancel a running workflow |
| `soulforge resume <run-id>` | Resume a failed run |
| `soulforge events [--run <id>] [--follow]` | Stream workflow events |
| `soulforge logs [<lines>]` | Show daemon log |
| `soulforge daemon start/stop/status` | Manage the daemon |
| `soulforge workflow list` | List available workflows |
| `soulforge workflow show <name>` | Show a workflow's YAML |
| `soulforge workflow create <name> [--from <template>]` | Create custom workflow |

## Run Flags

- `--workdir <path>` — **required**, project directory (must exist)
- `--var key=value` — pass variables (e.g. `build_cmd`, `test_cmd`)
- `--keep-worktree` — keep worktree metadata/files after run completion
- `--executor <name>` — override executor for all code steps (e.g. `codex-cli`, `claude-code`)
- `--model <name>` — override model for all code steps (e.g. `gpt-5.3-codex`, `opus`)
- `--callback-exec <command>` — shell command callback for step notifications (see Callbacks)
- `--no-callback` — run without any callbacks

⚠️ The task is a **positional argument**, not a flag. It must come after the workflow name:
```bash
soulforge run feature-dev "Your task here" --workdir /path/to/project
```

## Callbacks

Soulforge supports two callback methods for step notifications:

### OpenClaw CLI callback

```bash
soulforge run feature-dev "Add caching layer" \
  --workdir /path/to/project \
  --callback-exec 'openclaw agent --session-key "agent:myagent:slack:channel:c0123abc" --message "Soulforge run {{run_id}} step {{step_id}} status: {{step_status}}" --deliver'
```

Routes callbacks to the correct OpenClaw agent session automatically — no tokens or HTTP config.

> **Note:** `--session-key` requires the `ghostwater-ai/openclaw` fork (not yet in upstream). Available in OpenClaw builds from 2026.2.26+.

### Template variables

- `{{run_id}}` — run identifier
- `{{status}}` — run status
- `{{task}}` — original task string
- `{{step_id}}` — current step identifier
- `{{step_status}}` — current step status

### Per-step notify control

Steps define when callbacks fire via `notify`:
- `on_complete` — step finished successfully
- `on_waiting` — step is waiting for human approval
- `on_fail` — step failed

`executor: self` steps default to `[on_waiting]`.

## Checkpoint Workflow

Steps with `executor: self` pause for human approval:

```bash
# Check what's waiting
soulforge status

# Approve a checkpoint (optionally with context)
soulforge approve <run-id> --message "Looks good, proceed"

# Reject with feedback (rewinds to the step defined in on_reject.reset_to)
soulforge reject <run-id> --reason "Stories are too granular, combine 3 and 4"
```

The review-gate steps in both workflows use a `gate` type for conditional routing:
- **pass** → proceed to final-review
- **fix** → loop back through review-fix → code-review → gate (up to 5 times)

## Executor Override

Override which CLI runs the code steps:

```bash
# Use Claude Code instead of Codex
soulforge run feature-dev "Refactor auth module" \
  --workdir /path/to/project \
  --executor claude-code \
  --model opus
```

Available executors: `claude-code`, `codex-cli`, `codex` (legacy). The override only applies to code steps — `self` (checkpoint) steps are never overridden.

## Structured Step Output

Steps with `output_schema` use `soulforge complete` instead of stdout parsing:

1. Runner auto-injects completion instructions into the executor's prompt
2. Executor calls `soulforge complete --run-id <id> --step-id <id> --data '<json>'`
3. Data is validated against the schema
4. If executor exits without calling `complete`, runner resumes the session up to 3 times

## Git Worktree Behavior

When `--workdir` points to a git repository:
- **Bare+worktree layout** (`.bare/` + `main/`): creates worktree in sibling `worktrees/` directory
- **Standard `.git` layout**: creates worktree in `worktrees/` inside the repo
- **Not a git repo**: works in-place

## Best Practices (Operational Learnings)

### Task strings
- **Be extremely specific.** Without constraints, plans balloon to 10-12 stories. Include:
  - Explicit file paths when possible
  - Max story count ("3 stories maximum")
  - DO NOT lists ("DO NOT refactor unrelated code, DO NOT add documentation stories")
- Reference GitHub issues for detailed specs: `"Implement https://github.com/org/repo/issues/42"`

### Workflow management
- **One daemon per machine.** Multiple daemon processes from different install paths can share the same DB and cause conflicts. Kill strays with `pgrep -af "soulforge.*daemon-entry"`.
- **Check daemon health:** `soulforge daemon status` shows last tick time — "may be hung" means >5min since last poll.
- **Cancelled runs can leave orphaned steps.** Use `soulforge cancel <run-id>` explicitly; if steps are stuck, restart the daemon.

### Review gate workflow
- The code-review → gate → fix loop posts findings as PR comments (audit trail)
- Gate triage: FIX anything related to the task, SEPARATE genuine scope creep into new issues
- Gate is `executor: self` — the calling agent (you) triages, not a human

### Build/test discovery
- Workflows tell executors to "discover from AGENTS.md and repo scripts"
- For bugfix workflow, pass `--var build_cmd=` and `--var test_cmd=` explicitly for reliability
- Feature-dev workflow relies on AGENTS.md discovery — make sure the target repo has one

## Prerequisites

- **`soulforge` CLI** — `npm install -g @ghostwater/soulforge`
- **`codex` CLI** or **`claude` CLI** — the executor that runs code (must be authenticated with model provider)
- **`gh` CLI** — for PR creation (must be authenticated via `gh auth login`)
- **Git** — for worktree creation and branch management

### Credential requirements

Soulforge itself requires no API keys or tokens. All credentials are managed by the executor CLIs:
- **GitHub:** `gh auth login` (used for PR creation, issue filing, code review comments)
- **Claude Code:** Anthropic API key or OAuth (managed by `claude` CLI)
- **Codex CLI:** OpenAI API key or OAuth (managed by `codex` CLI)

No environment variables need to be set for Soulforge — it delegates all authenticated operations to the underlying CLIs.

## Environment Variables

- `SOULFORGE_DATA_DIR` — override data directory (default: `~/.soulforge`)

## Workflow Format Reference

See [references/workflow-format.md](references/workflow-format.md) for the full YAML schema, step types, gate routing, loop configuration, and template variables.
