# CodeFlicker CLI Skill

AI programming assistant skill for OpenClaw. Integrates with CodeFlicker CLI by Kuaishou.

## Features

- Install and configure CodeFlicker CLI
- Execute coding tasks with flickcli
- Configure models (glm-5, claude-haiku-4.5, etc.)
- Set approval mode (default, autoEdit, yolo)
- Continue sessions

## Installation

```bash
# Install via ClawHub
clawhub install codeflicker
```

Or clone from GitHub:
```bash
git clone https://github.com/LeeGoDamn/codeflicker-skill.git
```

## Usage

### Check Installation

```bash
codeflicker/scripts/check.sh
```

### Run Task

```bash
codeflicker/scripts/run.sh "write a hello world program"
```

### Configure

```bash
# Set default model
codeflicker/scripts/config.sh model glm-5

# Set auto-execute mode
codeflicker/scripts/config.sh approvalMode yolo

# View all config
codeflicker/scripts/config.sh list
```

### Continue Conversation

```bash
codeflicker/scripts/continue.sh "add unit tests"
```

## Requirements

- Node.js >= 22
- npm or pnpm
- Kuaishou internal network access

## Installation Steps

### 1. Set npm registry (Kuaishou internal network)

```bash
export npm_config_registry="https://npm.corp.kuaishou.com"
```

### 2. Install CLI

```bash
npm install -g @ks-codeflicker/cli
```

### 3. Login with SSO

```bash
flickcli /login
```

## License

MIT
