---
name: codeflicker
description: CodeFlicker CLI programming assistant. Use when user mentions flickcli, codeflicker, install codeflicker, or use codeflicker to write code.
---

# CodeFlicker CLI Skill

AI programming assistant CLI by Kuaishou. Similar to Claude Code or Codex CLI.

## Install

### Step 1: Set npm registry (for Kuaishou internal network)

```bash
export npm_config_registry="https://npm.corp.kuaishou.com"
```

### Step 2: Install CLI

```bash
npm install -g @ks-codeflicker/cli
```

### Step 3: Login with SSO

```bash
flickcli /login
```

Check installation:
```bash
flickcli --version
```

## Config

View config:
```bash
flickcli config list -g
```

Set config (global):
```bash
flickcli config set -g model glm-5
flickcli config set -g smallModel claude-haiku-4.5
flickcli config set -g planModel claude-4.5-sonnet
flickcli config set -g visionModel claude-4.5-sonnet
flickcli config set -g approvalMode yolo
```

Available models (wanqing provider):
- `glm-5` - default
- `glm-4.7`, `claude-haiku-4.5` - lightweight
- `claude-4.5-sonnet` - planning/vision

Approval modes:
- `default` - require confirmation
- `autoEdit` - auto edit
- `yolo` - auto execute (use with caution)

## Usage

Interactive mode:
```bash
flickcli "write a hello world"
```

Quiet mode (non-interactive):
```bash
flickcli -q "implement fibonacci"
```

Continue last session:
```bash
flickcli -q -c "add unit tests"
```

Specify model:
```bash
flickcli -m glm-5 "task"
```

Specify working directory:
```bash
flickcli --cwd /path/to/project "task"
```

## Quick Reference

| Command | Description |
|---------|-------------|
| `flickcli "task"` | Interactive mode |
| `flickcli -q "task"` | Quiet mode |
| `flickcli -q -c "task"` | Continue session |
| `flickcli -q -r <id> "task"` | Resume session |
| `flickcli config set -g approvalMode yolo` | Auto-execute mode |

## Notes

- Install requires Kuaishou internal npm registry
- **Must login with SSO before first use:** `flickcli /login`
- yolo mode auto-executes all operations