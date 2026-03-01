---
name: vitavault
description: VitaVault iOS app integration - analyze Apple Health exports (JSON, CSV, AI-ready text) with your AI agent. Works with any iPhone, no Mac required. Scan lab results, track medications, view health trends, and get AI-powered insights.
license: Apache-2.0
compatibility: Any OpenClaw agent. Pairs with VitaVault iOS app (free on App Store).
metadata:
  category: health
  platforms: ios
  author: BrandonS7
---

# VitaVault - Your Health, Decoded

AI agent skill for working with [VitaVault](https://vitavault.io) health data exports from iOS.

> **No Mac required.** VitaVault is a free iOS app that syncs your Apple Health data to your AI agent automatically. Install it from [TestFlight](https://testflight.apple.com/join/A4G27HBt) (beta) or the App Store (coming soon).

## Auto-Sync with OpenClaw

VitaVault automatically syncs health data to the cloud every time you open the app. Your OpenClaw agent can query it anytime.

### Setup

Set your sync token as an environment variable:
```bash
export VITAVAULT_SYNC_TOKEN="your-token-here"
```

### Query Scripts

```bash
# Get latest health snapshot
python3 scripts/query.py summary

# Get raw JSON
python3 scripts/query.py latest

# Get past week
python3 scripts/query.py week

# Get specific date range
python3 scripts/query.py range 2026-02-01 2026-02-28
```

### API Endpoints (for custom integrations)

All endpoints require `Authorization: Bearer <token>` header.

| Method | Path | Description |
|--------|------|-------------|
| GET | `/v1/health/latest` | Most recent health snapshot |
| GET | `/v1/health/range?start=YYYY-MM-DD&end=YYYY-MM-DD` | Health data for date range |
| GET | `/v1/status` | API health check (no auth) |

Base URL: `https://vitavault-api.brandon-f00.workers.dev`

## What is VitaVault?

VitaVault is a privacy-first iOS health app that:
- Reads 48+ health data types from Apple Health (steps, sleep, heart rate, HRV, blood oxygen, weight, and more)
- Scans lab results with AI and explains them in plain English
- Tracks medications with smart reminders
- Generates doctor visit prep reports
- Exports data in 3 formats: JSON, CSV, and AI-ready text
- All data stays on-device - nothing is uploaded to any server

## When to Use This Skill

- User shares a VitaVault health export (JSON, CSV, or AI-ready text)
- User asks about their Apple Health data
- User wants health trend analysis or recommendations
- User asks about lab results or medication tracking
- User wants to prepare for a doctor visit

## Working with VitaVault Exports

### AI-Ready Format (Plain Text)
The easiest format - pre-formatted for AI analysis. Users export from VitaVault and paste directly.

Example:
```
HEALTH SUMMARY - Last 7 Days

Steps: 43,133 total (6,162/day avg)
Sleep: 6h 42m last night, 7.1h weekly avg
Heart Rate: 72 bpm avg, 62 bpm resting
HRV: 30ms avg
Blood Oxygen: 97% avg
Weight: 185.4 lbs
Active Calories: 4,645 total (616/day avg)
Exercise: 142 min total
```

### JSON Format
Structured data for programmatic analysis:
```json
{
  "exportDate": "2026-02-17T12:00:00Z",
  "period": "7d",
  "metrics": {
    "steps": { "total": 43133, "dailyAverage": 5719, "unit": "steps" },
    "sleep": { "lastNight": 6.7, "weeklyAverage": 7.1, "unit": "hours" },
    "heartRate": { "average": 72, "resting": 62, "unit": "bpm" },
    "hrv": { "average": 30, "unit": "ms" },
    "bloodOxygen": { "average": 97, "unit": "%" },
    "weight": { "latest": 185.4, "unit": "lbs" },
    "activeCalories": { "dailyAverage": 542, "unit": "kcal" }
  }
}
```

### CSV Format
One row per day, opens in Excel/Sheets:
```csv
date,steps,sleep_hours,resting_hr,hrv_ms,weight_lbs,calories
2026-02-17,8012,6.7,62,28,185.4,642
2026-02-16,5891,7.2,61,33,185.2,589
```

## Analysis Prompts

When a user shares VitaVault data, you can:

1. **Trend Analysis** - Identify patterns in sleep, activity, heart rate
2. **Risk Flags** - Flag concerning metrics (low HRV, poor sleep consistency, elevated resting HR)
3. **Recommendations** - Actionable health suggestions based on data
4. **Doctor Prep** - Generate a summary report for medical appointments
5. **Lab Interpretation** - Explain lab values in context with health metrics
6. **Goal Tracking** - Compare current metrics against user goals

## Example Interaction

User: "Here's my VitaVault export, what should I focus on?"

Good response pattern:
1. Acknowledge the data received
2. Highlight 2-3 key observations (positive and concerning)
3. Give 3 specific, actionable recommendations
4. Offer to dig deeper into any metric

## Privacy Note

VitaVault processes all health data on-device. Exports are user-initiated only. When users share exports with their AI agent, remind them this is their choice and the data is being processed by the AI provider.

## Links

- **App**: [VitaVault on TestFlight](https://testflight.apple.com/join/A4G27HBt) (beta)
- **Website**: [vitavault.io](https://vitavault.io)
- **Developers**: [vitavault.io/developers](https://vitavault.io/developers/)
- **Privacy**: [vitavault.io/privacy](https://vitavault.io/privacy/)
