# Coding Team Setup v2.0

Flexible multi-agent development team wizard for OpenClaw.

## Features

- **2–10 agents** — pick from 10 preset roles or create custom ones
- **Multiple teams** — run parallel teams with `--team <name>`
- **4 workflow templates** — standard 9-step, quick 3-step, fullstack solo, or fully custom
- **Smart model assignment** — auto-detects registered models, maps by type
- **One command setup** — wizard handles openclaw.json + workspaces + manifests

## Usage

```bash
node wizard/setup.js                  # Default team
node wizard/setup.js --team alpha     # Named team
```

## Preset Roles

📋 PM · 🏗️ Architect · 🎨 Frontend · ⚙️ Backend · 🔍 QA · 🚀 DevOps · 🛠️ Code Artisan · 📊 Data Engineer · 🔒 Security · 📝 Tech Writer

Plus unlimited custom roles.

## Requirements

- OpenClaw installed with `openclaw.json` present
- Node.js 18+
- At least one model registered

See `SKILL.md` for full documentation.
