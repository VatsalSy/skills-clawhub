---
name: token-usage-optimizer
description: Maximize your Claude Code subscription value with smart usage monitoring and burn rate optimization. Track 5-hour session and 7-day weekly quotas, get one-time alerts, and daily reports showing if you're under/over-using your $20-200/month plan. Ultra-lightweight (10min cache, minimal API calls). Perfect for Pro, Max 100, and Max 200 subscribers who want to get every dollar's worth.
metadata:
  clawdbot:
    emoji: "📊"
    os:
      - darwin
      - linux
    requires:
      bins:
        - curl
        - date
        - grep
---

# Token Usage Optimizer

**Get the most out of your Claude Code subscription** by monitoring usage in real-time and optimizing your daily burn rate.

## Why Use This?

You're paying $20-200/month for Claude Code. Are you:
- ✅ Using it to its full potential?
- ❌ Hitting limits too early?
- ❌ Leaving quota unused at reset?

This skill tracks your **5-hour session** and **7-day weekly** quotas, calculates your **daily burn rate**, and tells you if you should use more or throttle back.

## Features

- 📊 **Burn Rate Tracking** — Are you under/over/on-pace for optimal usage?
- ⚡ **Smart Alerts** — One-time warnings when SESSION > 50% (no spam)
- 🎯 **Plan-Aware** — Auto-detects Pro ($20), Max 100 ($100), Max 200 ($200)
- 💾 **Ultra-Lightweight** — 10-minute cache, minimal API calls
- 📅 **Daily Reports** — Evening summary: SESSION, WEEKLY, burn rate
- 🔄 **Auto-Refresh** — OAuth token refresh every hour (access tokens expire ~1h)

## Quick Start

### 1. Setup

Run the setup wizard to configure your OAuth tokens:

```bash
cd {baseDir}
./scripts/setup.sh
```

You'll need:
- **Access Token** (`sk-ant-oat01-...`)
- **Refresh Token** (`sk-ant-ort01-...`)

See `references/token-extraction.md` for how to get these.

### 2. Check Usage

```bash
./scripts/check-usage.sh
```

Output:
```
SESSION=22.0
WEEKLY=49.0
BURN_RATE=OK
CACHED_AT=1771583780
```

### 3. Human-Readable Report

```bash
./scripts/report.sh
```

Output:
```
📊 Claude Code Daily Check:

⏱️  SESSION (5h): 22%
📅 WEEKLY (7d): 49%

⚪ На темпі — оптимальне використання
```

## Burn Rate Interpretation

- **🟢 UNDER** — You're under-using your subscription. Use more to get your money's worth!
- **⚪ OK** — On pace. Optimal usage for your plan.
- **🔴 OVER** — Over-burning. You'll hit limits before reset.

## Daily Budget by Plan

| Plan | Monthly | Weekly Budget | Daily Budget |
|------|---------|---------------|--------------|
| Pro | $20 | ~14% | ~2% |
| Max 100 | $100 | ~14% | ~2% |
| Max 200 | $200 | ~14% | ~2% |

*(7-day window resets weekly, so ~14% per day = 100% per week)*

## Integration with Heartbeat

Add to your `HEARTBEAT.md`:

```markdown
### Evening Check (18:00-20:00)
- Claude Code usage: `/path/to/token-usage-optimizer/scripts/report.sh`
```

## Alert Thresholds

- **SESSION > 50%** → 🟡 One-time warning (won't repeat until next reset)
- **WEEKLY > 80%** → 🟡 One-time warning

Alerts use state tracking (`/tmp/claude-usage-alert-state`) to avoid spam.

## Cache

Default: `/tmp/claude-usage.cache` with 10-minute TTL.

Override:
```bash
CACHE_FILE=/custom/path CACHE_TTL=300 ./scripts/check-usage.sh
```

## Files

- `scripts/setup.sh` — Initial token configuration
- `scripts/check-usage.sh` — Core usage checker (cached, burn rate calc)
- `scripts/report.sh` — Human-readable daily report
- `references/api-endpoint.md` — Anthropic OAuth API docs
- `references/token-extraction.md` — How to get OAuth tokens
- `references/plans.md` — Claude Code subscription tiers

## API Endpoint

```
GET https://api.anthropic.com/api/oauth/usage
Authorization: Bearer <access-token>
anthropic-beta: oauth-2025-04-20
```

Response:
```json
{
  "five_hour": {
    "utilization": 22.0,
    "resets_at": "2026-02-20T14:00:00.364238+00:00"
  },
  "seven_day": {
    "utilization": 49.0,
    "resets_at": "2026-02-24T10:00:01.364256+00:00"
  }
}
```

## Requirements

- `curl` — API requests
- `date` — Timestamp parsing
- `grep`, `cut`, `printf` — Text parsing

No external dependencies (jq, etc.).

## Privacy

Tokens are stored in `{baseDir}/.tokens` (gitignored).

Never share your access/refresh tokens.

## Auto-Refresh Setup (Recommended)

To prevent token expiration (access tokens expire ~1 hour), set up automatic refresh:

```bash
# Add cron job to refresh token every hour
openclaw cron add \
  --name "claude-token-refresh" \
  --every 1h \
  --announce \
  --message "Рефреш Claude Code OAuth токена: запусти {baseDir}/scripts/auto-refresh-cron.sh"
```

The script uses Claude CLI for reliable token refresh. If it fails, you'll get a notification to manually refresh via `claude auth login`.

## Troubleshooting

**"No token configured"**
→ Run `./scripts/setup.sh`

**"Token expired" / "API request failed"**
→ Access tokens expire after ~1 hour
→ Option 1: Set up auto-refresh cron every hour (see above)
→ Option 2: Manually refresh: `claude auth login` and re-run setup

**Burn rate shows empty**
→ API response missing `resets_at` — try again in a few minutes

**Auto-refresh failed**
→ OAuth refresh endpoint may have changed
→ Manual refresh: `claude auth login` → copy new tokens → run `./scripts/setup.sh`

## Contributing

Found a bug or have a feature request?
→ Open an issue on ClawHub: https://clawhub.ai/friday/token-usage-optimizer

## License

MIT
