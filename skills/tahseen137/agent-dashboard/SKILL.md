---
name: agent-dashboard
description: >
  Real-time agent dashboard for OpenClaw. Monitor active tasks, cron job health,
  issues, and action items from anywhere. Three setup tiers: (1) Zero-config canvas
  rendering inside OpenClaw, (2) GitHub Pages with 30-second polling — free, 2-minute
  setup, (3) Supabase Realtime + Vercel for instant websocket updates. All data stays
  on your machine. PIN-protected. No external services required for Tier 1.
---

# Mission Control 🚀

A real-time dashboard showing what your OpenClaw agent is doing, cron job health, issues requiring attention, and recent activity. Check it from anywhere — your phone, your laptop, wherever.

## Quick Start

### Tier 1 — Canvas (Zero Setup) ⚡

No external services. The agent renders the dashboard directly in your OpenClaw session.

**How to use:**
```
Show me the mission control dashboard
```

The agent will:
1. Gather current state (active tasks, crons, etc.)
2. Generate a dashboard using the canvas tool
3. Present it inline in your session

That's it. No deploy, no accounts, nothing to configure.

---

### Tier 2 — GitHub Pages + Polling (Recommended) 🌐

Free hosting with 30-second auto-refresh. Takes 2 minutes to set up.

**Setup:**

1. **Create a repo:**
   ```bash
   gh repo create mission-control --public --clone
   cd mission-control
   ```

2. **Copy the dashboard:**
   ```bash
   mkdir -p data
   # Copy tier2-github.html to index.html
   # Copy assets/templates/dashboard-data.json to data/
   ```

3. **Edit `index.html`:**
   - Change `YOUR_PIN_HERE` to your chosen PIN
   - Update `YOUR_GITHUB_USERNAME` to your GitHub username

4. **Enable GitHub Pages:**
   - Go to repo Settings → Pages
   - Source: Deploy from branch `main`
   - Folder: `/ (root)`

5. **Deploy:**
   ```bash
   git add -A && git commit -m "Initial deploy" && git push
   ```

Your dashboard is now live at `https://YOUR_USERNAME.github.io/mission-control/`

**How the agent updates it:**

The agent runs this command to push updates:
```bash
cd ~/mission-control
# Update data/dashboard-data.json with new data
git add data/dashboard-data.json
git commit -m "Dashboard update"
git push
```

The page auto-refreshes every 30 seconds, fetching the latest JSON.

---

### Tier 3 — Supabase Realtime + Vercel (Premium) ⚡🔥

True websocket realtime — updates appear in under 1 second.

**Prerequisites:**
- Supabase account (free tier works)
- Vercel account (free tier works)

**Step 1: Create Supabase Table**

In your Supabase SQL Editor, run `assets/templates/setup-supabase.sql`:

```sql
-- Creates the dashboard_state table with proper RLS
CREATE TABLE IF NOT EXISTS dashboard_state (
    id TEXT PRIMARY KEY DEFAULT 'main',
    data JSONB NOT NULL DEFAULT '{}',
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable RLS
ALTER TABLE dashboard_state ENABLE ROW LEVEL SECURITY;

-- Allow public read (for dashboard)
CREATE POLICY "Public read" ON dashboard_state
    FOR SELECT USING (true);

-- Only service role can write (push script)
CREATE POLICY "Service role write" ON dashboard_state
    FOR ALL USING (auth.role() = 'service_role');

-- Enable realtime
ALTER PUBLICATION supabase_realtime ADD TABLE dashboard_state;

-- Insert initial row
INSERT INTO dashboard_state (id, data) VALUES ('main', '{}')
ON CONFLICT (id) DO NOTHING;
```

**Step 2: Get Your Keys**

From Supabase Dashboard → Settings → API:
- Copy `SUPABASE_URL` (Project URL)
- Copy `SUPABASE_ANON_KEY` (anon public key — safe for client)
- Copy `SUPABASE_SERVICE_KEY` (service_role key — keep secret!)

**Step 3: Edit the Dashboard**

In `tier3-realtime.html`:
1. Replace `YOUR_SUPABASE_URL` with your project URL
2. Replace `YOUR_SUPABASE_ANON_KEY` with your anon key
3. Replace `YOUR_PIN_HERE` with your chosen PIN

**Step 4: Deploy to Vercel**

```bash
# Create project directory
mkdir mission-control && cd mission-control
# Copy tier3-realtime.html as index.html
vercel deploy --prod
```

**Step 5: Configure Push Script**

Set these environment variables on your OpenClaw machine:
```bash
export SUPABASE_URL="https://YOUR_PROJECT.supabase.co"
export SUPABASE_SERVICE_KEY="eyJ..."  # service_role key, NOT anon
```

The agent uses `assets/push-dashboard.sh` to push updates.

---

## Dashboard Features

### 🚨 Action Required
Urgent items that need your attention. Highlighted at the top with priority badges (high/medium/low).

### ⚡ Active Now
What the agent is currently working on, with model name and duration.

### 📊 Products
Your product cards with live/testing/down status badges.

### ⏰ Cron Jobs
Table showing all scheduled jobs with status, last run time, and error counts. Click to expand error details.

### 📋 Recent Activity
Timeline of recent events and accomplishments.

### 🔄 Force Update Button
Manual refresh button in the header — click to re-fetch latest data on demand. Resets the "Updated X ago" timer.

### 🔴 Live Indicator (Tier 3 only)
Green pulsing dot shows websocket is connected. Flash animation when data updates.

---

## Environment Variables

| Variable | Required | Tier | Purpose |
|----------|----------|------|---------|
| `DASHBOARD_PIN` | Yes | All | PIN code for dashboard access |
| `GITHUB_REPO` | Yes | Tier 2 | GitHub repo for Pages hosting (e.g., `username/mission-control`) |
| `SUPABASE_URL` | Yes | Tier 3 | Supabase project URL |
| `SUPABASE_ANON_KEY` | Yes | Tier 3 | Supabase anon key (read-only, safe for client-side) |
| `SUPABASE_SERVICE_KEY` | Yes | Tier 3 | Service role key (server-side push script ONLY — never expose!) |
| `VERCEL_PROJECT` | No | Tier 3 | Vercel project name for deploy |

---

## Permissions Required

| Tier | Permissions | Why |
|------|-------------|-----|
| Tier 1 | None | Canvas is built into OpenClaw |
| Tier 2 | `exec` | To run `git push` to YOUR repo |
| Tier 3 | None | Uses `curl` to YOUR Supabase (no special permissions) |

---

## Data Schema

The dashboard expects JSON in this format:

```json
{
  "lastUpdated": "2024-01-15T12:00:00Z",
  "pin": "your-pin-here",
  "actionRequired": [
    {
      "title": "Review PR #42",
      "url": "https://github.com/you/repo/pull/42",
      "priority": "high"
    }
  ],
  "activeNow": [
    {
      "task": "Deploying new feature",
      "model": "opus",
      "startedAt": "2024-01-15T11:45:00Z"
    }
  ],
  "products": [
    {
      "name": "My App",
      "url": "https://myapp.example.com",
      "status": "live",
      "lastChecked": "2024-01-15T12:00:00Z"
    }
  ],
  "crons": [
    {
      "name": "Daily Report",
      "schedule": "9:00 AM daily",
      "lastRun": "2024-01-15T09:00:00Z",
      "status": "ok",
      "errors": 0,
      "lastError": null
    }
  ],
  "recentActivity": [
    {
      "time": "2024-01-15T11:30:00Z",
      "event": "✅ Deployed v2.1.0 to production"
    }
  ],
}
```

### Field Reference

| Field | Type | Description |
|-------|------|-------------|
| `lastUpdated` | ISO-8601 | When data was last refreshed |
| `pin` | string | Dashboard access PIN |
| `actionRequired[].priority` | `high\|medium\|low` | Urgency level |
| `products[].status` | `live\|testing\|down` | Product health |
| `crons[].status` | `ok\|error\|paused` | Job status |

---

## Security & Privacy

✅ **All data stays on your machine** — Nothing is sent to third parties

✅ **PIN-protected** — Simple client-side access control

✅ **No install scripts** — This is an instruction-only skill; no executable code runs on install

✅ **Credentials use env vars** — No hardcoded secrets; all sensitive values come from environment variables

### Important Security Notes

⚠️ **PIN protection is client-side only** — It prevents casual access but isn't cryptographically secure. For sensitive dashboards:
- Keep your GitHub Pages repo private and use GitHub's authentication
- Use Vercel's password protection feature (paid plan)
- Don't put highly sensitive data in the dashboard

⚠️ **Supabase service key is secret** — Never put your `SUPABASE_SERVICE_KEY` in client-side code. The push script runs server-side on your OpenClaw machine.

⚠️ **RLS policies matter** — The provided SQL uses restrictive RLS: public can read, only service_role can write. Review and adjust if needed.

---

## Files Included

```
mission-control/
├── SKILL.md                      # This file
├── assets/
│   ├── tier1-canvas.html         # Lightweight canvas version
│   ├── tier2-github.html         # GitHub Pages + polling
│   ├── tier3-realtime.html       # Supabase Realtime version
│   └── push-dashboard.sh         # Push script for Tier 3
├── assets/templates/
│   ├── dashboard-data.json       # Sample data structure
│   └── setup-supabase.sql        # Supabase table setup
└── references/
    └── customization.md          # Theme and layout customization
```

---

## Updating the Dashboard

### Manual Update
```
Update my mission control dashboard with:
- Action required: [your items]
- Currently working on: [current task]
```

### Automatic Updates (Recommended)

The dashboard stays fresh through two mechanisms:

**1. Periodic cron job (every 30 min):**
```
Set up a cron that updates my mission control dashboard every 30 minutes.
It should: collect cron status (via `cron list`), check active sub-agents
(via `sessions_list`), read HEARTBEAT.md for action items, read today's
memory file for recent activity, then push the data to Supabase/GitHub.
```

The agent will:
1. Use `cron list` to get all job statuses, error counts, last run times
2. Use `sessions_list` to find active sub-agents and their tasks
3. Read `HEARTBEAT.md` for action items needing human attention
4. Read today's `memory/YYYY-MM-DD.md` for recent activity
5. Build the JSON payload and push to GitHub (Tier 2) or Supabase (Tier 3)

**2. Real-time event pushes:**
The agent can also push updates immediately when significant events happen — task starts, task completes, errors, deploys. This means the dashboard reflects changes within seconds, not just every 30 minutes.

**3. Force Update button:**
The dashboard includes a manual "🔄 Force Update" button that re-fetches the latest data on demand and resets the "Updated X ago" timer.

The combination of periodic cron + real-time pushes + manual refresh keeps the dashboard accurate at all times.

---

## Troubleshooting

### Dashboard shows "Disconnected" (Tier 3)
- Check Supabase project is running
- Verify anon key is correct
- Ensure realtime is enabled on the table

### Data not updating (Tier 2)
- Check GitHub Pages is enabled
- Verify `data/dashboard-data.json` was pushed
- Hard refresh the page (Ctrl+Shift+R)

### PIN not working
- PINs are case-sensitive
- Check you're using the same PIN in both data JSON and HTML config

---

## Credits

Built for the OpenClaw community. MIT License.
