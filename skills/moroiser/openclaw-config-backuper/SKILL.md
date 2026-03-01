---
name: openclaw-config-backuper
description: Backup OpenClaw config files, Skills, Workspace files, and Memory records for migration or disaster recovery. Triggers: 备份配置、配置备份、迁移配置、恢复配置、导出配置、backup config、backup openclaw.
---

# OpenClaw Configuration Backup

Backup all OpenClaw configurations for migration or disaster recovery.

## Usage

Run `{baseDir}/scripts/backup.sh` to create a timestamped backup folder.

## Backup Contents

| Source | Target |
|--------|--------|
| `~/.openclaw/*.json` | `config/` |
| `~/.openclaw/skills/*` | `skills/` |
| `~/.openclaw/workspace/*.md` | `workspace/` |
| `~/.openclaw/workspace/memory/*` | `memory/` |

## Backup Location

`~/.openclaw/workspace/backup/YYYYMMDD_HHMMSS/`

## Workflow

1. Create backup directory with timestamp
2. Copy JSON configs (openclaw.json, exec-approvals.json, etc.)
3. Copy all local Skills from `~/.openclaw/skills/`
4. Copy workspace MD files (AGENTS.md, MEMORY.md, etc.)
5. Copy memory logs
6. Report file count and location

## Notes

- Does NOT backup built-in skills (only `~/.openclaw/skills/`)
- Does NOT create compressed archive
