---
name: coding-lead
description: Smart coding skill that routes tasks by complexity. Simple tasks (<60 lines, single file) execute directly via OpenClaw agent tools. Medium/complex tasks spawn Claude Code via ACP with full project context, coding standards, and historical decisions from agent memory. Use when user asks to write code, fix bugs, build features, refactor, review PRs, deploy, or any software engineering task. Combines OpenClaw long-term memory with Claude Code deep coding ability.
---

# Coding Lead

Route coding tasks by complexity: simple = do it yourself, complex = spawn Claude Code with full context.

## System Impact

- **Simple tasks**: uses read/write/edit/exec tools to modify project files directly
- **Medium/Complex tasks**: spawns Claude Code via `sessions_spawn(runtime: "acp")` which creates a subprocess with file system access to the specified project directory
- **Memory writes**: logs decisions and changes to agent memory files after each task
- **No credentials required**: uses whatever model providers are already configured
- **ACP requirement**: Claude Code (or compatible coding agent) must be available as an ACP harness for medium/complex tasks. Simple tasks work without ACP.

## Why This Exists

OpenClaw agents have memory but limited coding depth. Claude Code has deep coding ability but no memory across sessions. This skill bridges the gap: the agent acts as engineering manager with persistent context, Claude Code acts as the expert coder.

## Tech Stack Preferences (New Projects)

When starting a new project, propose tech stack based on these preferences and get confirmation before coding:

| Layer | Preferred | Fallback |
|-------|-----------|----------|
| Backend | PHP (Laravel or ThinkPHP) | Python |
| Frontend | Vue.js | React |
| Mobile | Flutter | UniApp-X |
| CSS | Tailwind CSS | - |
| Database | MySQL | PostgreSQL |

- **Existing projects**: follow their current stack, never migrate without explicit approval
- **New projects**: propose stack in the PLAN phase, wait for confirmation
- Include tech stack choice in the Claude Code prompt so it uses the right framework
## Task Classification

Assess every coding request before executing:

| Level | Criteria | Action |
|-------|----------|--------|
| **Simple** | Single file, clear requirement, <60 lines changed | Execute directly with read/write/edit/exec tools |
| **Medium** | 2-5 files, needs investigation, clear scope | Spawn Claude Code with context |
| **Complex** | Architecture change, multi-module, high uncertainty | Plan first, then spawn Claude Code |

When in doubt, go one level up.

## Simple Tasks: Direct Execution

Use agent tools: read, write, edit, exec.

Before coding:
1. Read the target file(s)
2. Check for coding standards (look for tech-standards.md, CLAUDE.md, .cursorrules, or similar in the project or shared knowledge)
3. Search memory for related past decisions

After coding:
4. Self-check: does it follow standards?
5. Log the change in daily memory file

Examples: config edits, small bug fixes, adding a field, renaming, formatting.

## Medium/Complex Tasks: Spawn Claude Code

### Step 1: Gather Context (agent does this)

Before spawning, collect from available sources:
1. **Project info**: read CLAUDE.md, README, or package.json/composer.json
2. **Coding standards**: check for tech-standards.md (shared knowledge), CLAUDE.md (project), .cursorrules, or equivalent
3. **Past decisions**: search MEMORY.md and daily memory for related work
4. **Task context**: inbox messages, kanban items, product docs if applicable
5. **Known pitfalls**: anything from memory about this codebase

### Step 2: Build the Prompt

Structure for Claude Code:

```
## Project
- Path: [project directory]
- Tech stack: [from docs or memory]
- Key architecture notes: [from CLAUDE.md or memory]

## Coding Standards (mandatory)
[Paste or summarize from whatever standards file exists]
- [Key rule 1]
- [Key rule 2]
- [Project-specific rules]

## Historical Context
[From agent memory — skip if no relevant history]
- [Past decision 1]
- [Known pitfall]
- [Related prior work]

## Task
[Clear description]

## Acceptance Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] Existing tests pass
- [ ] No unrelated changes
- [ ] Cleaned up: no debug logs, unused imports, temp files
```

### Step 3: Spawn

Medium tasks: `sessions_spawn(runtime: "acp", task: <prompt>, cwd: <project dir>, mode: "run")`
Complex tasks: `sessions_spawn(runtime: "acp", task: <prompt>, cwd: <project dir>, mode: "session")`

Session mode allows follow-up via sessions_send if needed.

### Step 4: Review Output

When Claude Code completes:
1. Check acceptance criteria
2. Verify no unrelated changes
3. Run tests if available
4. If not satisfied, send follow-up via sessions_send

### Step 5: Record to Memory

Update daily memory file with:
- What was done and why
- Key decisions made
- Pitfalls encountered
- Anything future sessions need to know

This is the agent's key advantage: it remembers everything across sessions.

## Complex Task Flow: RESEARCH > PLAN > EXECUTE > REVIEW

### RESEARCH
Spawn Claude Code in session mode to investigate only (no changes):
- List files that need changes
- Identify dependencies and call chains
- Find reusable existing code
- Flag risks

### PLAN
Review findings. Present options if multiple approaches exist. Get confirmation before proceeding.

### EXECUTE
Spawn Claude Code with confirmed plan + full context. Break into sub-tasks if needed.

### REVIEW
Verify output. Run tests. Update memory with decisions and lessons.

## Claude Code Tool Tips

When building prompts for Claude Code, remind it to use its specialized tools:
- LSP (goToDefinition, findReferences) for code structure
- Grep/Glob for finding files and patterns
- mcp__context7 for library documentation
- mcp__mcp-deepwiki for open-source project docs

These are Claude Code tools, not OpenClaw tools. Only include in spawned prompts.

## Memory Integration Patterns

### Before spawning
Search memory for related past work. Include findings as "Historical Context" in the prompt.

### After completion
Write detailed record: files changed, decisions made, pitfalls, test results.

### Cross-session continuity
When tasks span multiple sessions:
1. End of session: write detailed status to memory
2. Next session: read memory, reconstruct context
3. Spawn Claude Code with accumulated context

This is the core value: Claude Code gets amnesia every session, the agent does not.


## Progress Updates

When spawning Claude Code for medium/complex tasks, keep the user informed:

1. **On start**: send 1 short message — what task, which project, estimated complexity
2. **On milestone**: only when something meaningful happens (build done, tests passed, blocked)
3. **On error**: immediately report what went wrong and whether retry is planned
4. **On completion**: summarize what changed, what files were touched, test results

Do NOT poll silently. Do NOT go quiet for long periods. The user should never wonder "is it still running?"

## Auto-Notify on Completion

When spawning Claude Code, append a notification command to the end of the prompt so the agent announces completion automatically:

```
... your task description here.

When completely finished, run this command to notify:
openclaw system event --text "Done: [brief summary of what was built/changed]" --mode now
```

This triggers an immediate notification instead of waiting for the next poll cycle.

## Workdir Isolation

Always specify `cwd` when spawning to keep the coding agent focused:

- Set `cwd` to the **project directory**, not the agent workspace
- This prevents the coding agent from reading team management files (SOUL.md, inboxes, etc.)
- If the project path is unknown, ask the user before spawning

```
sessions_spawn(runtime: "acp", task: <prompt>, cwd: "/path/to/project", mode: "run")
```

## Parallel Tasks

Independent coding tasks can run in parallel:

- Spawn multiple ACP sessions, each with its own task and project directory
- Track via `sessions_list` or `subagents(action: "list")`
- Each session gets its own context — no interference
- After all complete, review outputs and record to memory

Example: fix 3 independent bugs simultaneously, each in its own session.

Limit: be mindful of API rate limits and system resources. 2-3 parallel sessions is usually safe.


## Smart Retry (max 3 attempts)

When a spawned Claude Code session fails, do NOT re-run with the same prompt. Instead:

1. **Analyze the failure**: read the session output, identify root cause
   - Context insufficient? → narrow scope: "focus only on these 3 files"
   - Wrong direction? → clarify: "the requirement is X, not Y"
   - Missing info? → add: include the missing type definitions, config, or docs
   - Environment issue? → fix the environment first, then retry
2. **Rewrite the prompt**: adjust based on analysis, add constraints or context
3. **Retry**: spawn a new session with the improved prompt
4. **Max 3 attempts**: if still failing after 3 tries, stop and report to the user with:
   - What was attempted
   - What failed each time
   - Your analysis of why
   - Suggested next steps (may need human intervention)

Never blindly retry. Each attempt should be meaningfully different from the last.

## Prompt Pattern Library

After each successful coding task, record what worked in memory:

```
## Prompt Pattern: [task type]
- What worked: [prompt structure that succeeded]
- Key ingredients: [what context was essential]
- Pitfalls: [what caused failures before success]
- Example: [brief prompt snippet]
```

Over time, this builds a library of proven patterns. Before spawning Claude Code, search memory for similar past tasks and reuse successful prompt structures.

Examples of patterns worth recording:
- "Billing features need full DB schema context upfront"
- "Refactors work better with explicit file list + dependency graph"
- "API endpoints need existing route patterns as reference"
- "Always include test file paths for test-related tasks"

This is cumulative knowledge that makes every future task faster and more reliable.

## Safety Rules

- **Never spawn coding tasks in ~/.openclaw/ or the agent workspace directory** — coding agents may read/modify config files, soul docs, or memory files
- **Never let coding agents modify files outside the specified project directory** without explicit approval
- **Always review output before committing** — especially for complex tasks
- **Kill runaway sessions** — if a session runs past timeout or produces nonsensical output, kill it and report

## See Also
- references/prompt-examples.md: real prompt examples for different task types