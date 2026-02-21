---
name: soulforge
description: "Dispatch multi-step coding workflows to Claude Code CLI or Codex CLI from YAML definitions via a persistent background daemon. Use when: (1) implementing a feature end-to-end (plan → implement → verify → PR), (2) delegating coding tasks to run in the background while you do other work, (3) running development workflows that need human review checkpoints, (4) automating feature branch creation, implementation, and PR submission. Requires the @ghostwater/soulforge npm package."
repository: "https://github.com/ghostwater-ai/soulforge"
metadata:
  {
    "openclaw":
      {
        "emoji": "🔥",
        "requires":
          {
            "bins": ["soulforge", "claude", "gh"],
            "env": ["GITHUB_TOKEN or gh auth login"],
            "optional_bins": ["codex"],
          },
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

Daemon-based workflow engine that dispatches coding steps to Claude Code CLI or Codex CLI, with human review checkpoints between stages.

## Security & Data Flow

⚠️ **What this tool sends externally:**
- **Model CLIs (claude/codex):** Repository contents and prompts are sent to the configured model provider (Anthropic, OpenAI). Only run on repos where you accept this exposure.
- **Callbacks:** Run metadata (run ID, task description, step status) is POSTed to the URL you configure via `--callback-url`. Never point callbacks at endpoints you don't control. Avoid putting secrets in callback headers or body templates.
- **GitHub:** PRs are created via `gh pr create`, which requires authenticated GitHub CLI. Runs push branches and create PRs on the configured repo.

**Required credentials:**
- `gh` CLI must be authenticated (`gh auth login`) for PR creation
- Claude Code or Codex CLI must be installed and configured with API keys
- Callback URLs and auth tokens are user-supplied — keep them to trusted, local endpoints

## Quick Start

```bash
npm install -g @ghostwater/soulforge
soulforge daemon start
```

## Running a Workflow

The primary command. Only one built-in workflow exists: `feature-dev`.

```bash
soulforge run feature-dev "<task description>" \
  --var repo=/path/to/project \
  --var build_cmd="npm run build" \
  --var test_cmd="npm test"
```

### What Happens (feature-dev pipeline)

1. **plan** (claude-code, opus) — decomposes task into ordered user stories
2. **review-plan** (self) — ⏸️ pauses for human approval; reject loops back to plan with feedback
3. **implement** (claude-code, opus) — implements each story in a loop, verified individually
4. **verify** (claude-code, opus) — checks acceptance criteria per story
5. **test** (claude-code, opus) — runs integration/E2E tests
6. **pr** (claude-code, opus) — creates PR via `gh pr create`
7. **final-review** (self) — ⏸️ pauses for final human review

### Defaults (feature-dev)

| Setting | Default | Override |
|---------|---------|----------|
| Executor | `claude-code` | Per-step in workflow YAML |
| Model | `opus` (auto-latest) | Per-step in workflow YAML |
| Timeout | 600s per step | Per-step in workflow YAML |
| Max retries | 2 | Per-step in workflow YAML |
| Worktree | Auto-created | `--no-worktree` or `--workdir` |
| Branch name | `soulforge/<short-run-id>` | `--branch <name>` |

### Git Worktree Behavior

When `--var repo=<path>` points to a git repository, Soulforge **auto-creates a worktree by default**:

- **Bare+worktree layout** (`.bare/` + `main/`): worktree created in sibling `worktrees/` directory
- **Standard `.git` layout**: worktree created in `worktrees/` inside the repo
- **Not a git repo**: errors out (use `--workdir` instead)

**Override worktree behavior:**
- `--workdir /some/path` — use an existing directory, no git operations at all
- `--no-worktree` — work directly in the repo (no worktree creation)
- `--branch my-branch` — custom branch name instead of `soulforge/<id>`

`--workdir` and `--var repo=` are mutually exclusive.

## Checkpoints (approve/reject)

Steps with `executor: self` pause the pipeline and wait for human input.

```bash
soulforge status                        # see what's waiting
soulforge approve <run-id>              # continue pipeline
soulforge approve <run-id> --message "looks good, but watch edge cases"
soulforge reject <run-id> --reason "too many stories, simplify"
```

**Reject with loopback:** When a checkpoint has `on_reject.reset_to` configured (e.g., `review-plan` → `plan`), rejecting resets the pipeline to the target step. Your rejection reason is injected as `{{rejection_feedback}}` in the next run of that step.

Without `on_reject`, rejecting retries the same step.

## Monitoring

```bash
soulforge status                # active runs overview
soulforge status <query>        # filter by run ID prefix or task substring
soulforge runs                  # all runs (including completed)
soulforge events --run <id>     # event log for a run
soulforge events --follow       # stream all events
soulforge logs 50               # last 50 daemon log lines
```

## Lifecycle Commands

```bash
soulforge cancel <run-id>       # kill a running workflow
soulforge resume <run-id>       # retry a failed run from the failed step
soulforge daemon start          # start daemon (background)
soulforge daemon start -f       # start daemon (foreground, for debugging)
soulforge daemon stop           # stop daemon
soulforge daemon status         # check if daemon is running
```

## Callbacks (Framework-Agnostic)

Soulforge can POST to any URL on run and step events. Fully opaque — Soulforge doesn't know what's receiving the callback. Callers own routing.

`--callback-url` is **required**. Use `--no-callback` to explicitly opt out (silences all callbacks including run completion).

```bash
soulforge run feature-dev "Add caching layer" \
  --var repo=/path/to/project \
  --callback-url "http://127.0.0.1:18789/hooks/agent" \
  --callback-headers '{"Authorization":"Bearer <token>","Content-Type":"application/json"}' \
  --callback-body '{"message":"Run {{run_id}} finished: {{status}}. Task: {{task}}"}'
```

Template variables in `--callback-body`: `{{run_id}}`, `{{status}}`, `{{task}}`, `{{step_id}}`, `{{step_status}}`.

### Per-Step Notifications

Workflow steps can specify which events trigger callbacks via the `notify` field:

```yaml
steps:
  - id: implement
    executor: claude-code
    notify: [on_complete, on_fail]   # callback on complete or failure
    input: "Implement the feature"

  - id: review
    executor: self
    # self executor defaults to [on_waiting] — always notifies on checkpoint
    input: "Review the implementation"
```

Notify events: `on_complete`, `on_waiting`, `on_fail`.

Workflow-level defaults apply to steps that don't specify their own:

```yaml
defaults:
  notify: [on_complete, on_fail]
```

Self executor steps (checkpoints) auto-default to `[on_waiting]` when no notify is specified — checkpoints always notify.

## Convention: Specs as GitHub Issues

Write detailed specs as GitHub issue bodies, then reference them in the task:

```bash
soulforge run feature-dev \
  "Fix GitHub issue #5: https://github.com/org/repo/issues/5 — implement reject loopback" \
  --var repo=/path/to/project
```

The executor reads the issue URL and implements accordingly. This avoids orphaned spec files.

## Prerequisites

- **`soulforge` CLI** — `npm install -g @ghostwater/soulforge`
- **`claude` CLI** (Claude Code) — the executor that runs code steps
- **`gh` CLI** — authenticated (`gh auth login`) for PR creation
- **Git** — for worktree and branch management

## Workflow Format

See [references/workflow-format.md](references/workflow-format.md) for the full YAML schema, template variables, loop steps, and how to write custom workflows.
