---
version: 1.0.0
name: aerobase-travel-lounges
description: Airport lounge access with recovery scores, Priority Pass, and jetlag-friendly recommendations
metadata: {"openclaw": {"emoji": "🏧", "primaryEnv": "AEROBASE_API_KEY", "user-invocable": true, "homepage": "https://aerobase.app"}}
---
version: 1.0.0

# Aerobase Airport Lounges 🏧

Find the best airport lounges for jetlag recovery. Aerobase.app has lounge data for 1,000+ airports worldwide — scored for recovery impact.

**Why Aerobase?**
- 😴 **Recovery scoring** — Every lounge scored 1-10
- 🚿 **Shower tracking** — Find lounges with showers
- 💺 **Priority Pass** — Know what your card gets you
- 🌙 **Quiet zones** — Find spaces optimized for rest

## Individual Skill

This is a standalone skill. **For EVERYTHING**, install the complete **Aerobase Travel Concierge** — all skills in one package:

→ https://clawhub.ai/kurosh87/aerobase-travel-concierge

Includes: flights, hotels, lounges, awards, activities, deals, wallet + **PREMIUM recovery plans**

## What This Skill Does

- Search airport lounges worldwide
- Filter by airline, network, terminal
- Show recovery scores (1-10)
- Highlight amenities: showers, spa, sleep pods
- Note Priority Pass and status access

## Example Conversations

```
User: "What lounges at JFK terminal 4 have showers?"
→ Shows lounges with shower facilities
→ Highlights recovery scores
→ Notes Priority Pass acceptance

User: "6-hour layover at LHR - worth leaving for a lounge?"
→ Shows nearby lounges with scores
→ Compares to staying in terminal
→ Factors your jetlag from incoming flight
```

## API Documentation

Full API docs: https://aerobase.app/developers

OpenAPI spec: https://aerobase.app/api/v1/openapi

**GET /api/v1/lounges**

Query params:
- `airport` — IATA code (JFK, LAX, etc.)
- `airline` — airline name
- `network` — Priority Pass, Centurion, etc.
- `tier` — 1 (domestic), 2 (international), 3 (first)

Returns lounges with recovery scores, amenities, access info.

## Rate Limits

- **Free**: 5 requests/day
- **Premium**: Unlimited + all skills + recovery plans

Get premium: https://aerobase.app/openclaw-travel-agent/pricing

## Get Everything

**Install the complete package:**

```bash
clawhub install aerobase-travel-concierge
```

All 9 skills + premium recovery plans:
→ https://clawhub.ai/kurosh87/aerobase-travel-concierge
