---
name: aic-dashboard
description: AI Commander Management Dashboard. A lightweight companion web UI for monitoring inbound emails received via the email-webhook skill and browser session status created by the browser-auth skill.
metadata: {"openclaw": {"requires": {"bins": ["node"], "env": ["DASHBOARD_TOKEN"]}, "primaryEnv": "DASHBOARD_TOKEN", "install": [{"id": "npm-deps", "kind": "node", "package": "express@4.21.2", "label": "Install Dashboard dependencies"}]}}
---

# AI Commander Dashboard

A companion dashboard for AI Commander agents. Displays inbound emails collected by the [`email-webhook`](https://clawhub.ai/lksrz/email-webhook) skill and shows the status of browser sessions created by the [`browser-auth`](https://clawhub.ai/lksrz/browser-auth) skill.

This skill is a **read-only viewer** — it does not capture credentials, control browsers, or send messages. It simply reads local data files and serves them via a token-protected web UI.

## Companion Skills

| Skill | What it does |
|---|---|
| [`email-webhook`](https://clawhub.ai/lksrz/email-webhook) | Receives inbound emails and writes them to `inbox.jsonl` |
| [`browser-auth`](https://clawhub.ai/lksrz/browser-auth) | Runs a remote browser tunnel and writes session data to `session.json` |

This dashboard reads both files and displays them in one place.

## What This Skill Does

- Reads `inbox.jsonl` and displays the last 50 inbound emails
- Reads `session.json` and shows whether an active browser session exists
- Serves a token-gated web UI on a configurable local port
- Refreshes automatically every 5 seconds

## Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `DASHBOARD_TOKEN` | **Yes** | — | Secret token for accessing the dashboard. |
| `PORT` | No | `19195` | Port for the web dashboard. |
| `DASHBOARD_HOST` | No | `127.0.0.1` | IP to bind the dashboard to. |
| `INBOX_PATH` | No | `./data/inbox.jsonl` | Path to inbound email data (from `email-webhook`). |
| `SESSION_PATH` | No | `./data/session.json` | Path to session file (from `browser-auth`). |

## Setup

1. **Install dependencies**:
   ```bash
   npm install express@4.21.2
   ```
2. **Start Server**:
   ```bash
   DASHBOARD_TOKEN=mysecret node scripts/server.js
   ```
3. **Open in browser**:
   ```
   http://127.0.0.1:19195/?token=mysecret
   ```

## Security

- All requests require `X-Dashboard-Token` header, `Authorization: Bearer <token>`, or `?token=` query param
- Binds to `127.0.0.1` by default — use a secure tunnel (Tailscale, Cloudflare Tunnel, SSH) for remote access
- The UI stores the token in `localStorage` and removes it from the URL after load, preventing it from appearing in browser history or server logs
