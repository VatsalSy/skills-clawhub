---
name: crash-fixer
description: "Autonomous crash analysis and bug fixing. Monitors crash reports from Cloudflare D1, deduplicates, analyzes with Codex 5.3 High, generates fixes, and creates PRs. Usage: /crash-fixer [--hours 24] [--limit 5] [--dry-run]"
user-invocable: true
metadata:
  { "openclaw": { "requires": { "env": ["GH_TOKEN", "OPENAI_API_KEY", "CRASH_REPORTER_API_KEY", "CRASH_REPORTER_URL"] } } }
---

# crash-fixer

Full autonomous crash-fixing loop. Fetches crashes, deduplicates, analyzes with AI, generates fixes, and creates PRs.

## Trigger

```
/crash-fixer [--hours 24] [--limit 5] [--dry-run]
```

## How It Works

### 1. Fetch
Query D1 for crashes with status='new' since last N hours

### 2. Deduplicate
For each crash, check if a fix was already attempted:
- Query D1 for existing crashes with same error_name + message fingerprint
- Skip if PR already exists (status='fixing' or fix_pr_url is set)
- Track processed crashes in D1 (update status field)

### 3. Analyze (GPT Codex 5.3 High)
- Parse stack trace for file/line info
- Search codebase for relevant files
- Identify root cause

### 4. Fix
- Read affected source files
- Generate minimal fix code

### 5. Create PR
- Create branch: `fix/crash-{id}-{error-hash}`
- Commit fix with description
- Open PR with crash details
- Update D1 with PR URL

## Options

| Flag | Default | Description |
|------|---------|-------------|
| `--hours N` | 24 | Only fetch crashes from last N hours |
| `--limit N` | 3 | Max crashes to process per run |
| `--dry-run` | false | Analyze but don't create PRs |

## Environment

- `GH_TOKEN` - GitHub API token
- `OPENAI_API_KEY` - OpenAI API key for Codex 5.3 High
- `CRASH_REPORTER_API_KEY` - API key for crash reporter worker
- `CRASH_REPORTER_URL` - URL for crash reporter worker (optional)

## Deduplication Logic

Fingerprint = hash(error_name + first 100 chars of message)

Before processing crash:
```sql
SELECT * FROM crashes WHERE 
  fingerprint = ? 
  AND (status = 'fixing' OR fix_pr_url IS NOT NULL)
```

If match found → skip with note "Already fixed"
