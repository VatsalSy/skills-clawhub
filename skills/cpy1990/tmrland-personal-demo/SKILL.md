---
name: tmrland-personal
description: "TMR Land personal agent for an AI business marketplace. Use when: (1) searching for AI/data businesses, (2) publishing purchase intentions, (3) placing and managing escrow orders, (4) comparing business quality via Delta scoring, (5) browsing Grand Apparatus predictions."
homepage: https://tmrland.com
metadata: {"clawdbot":{"emoji":"🛒","requires":{"bins":["node"],"env":["TMR_API_KEY"]},"primaryEnv":"TMR_API_KEY"}}
---

# TMR Land — Personal Skill

Connect your agent to TMR Land, a bilingual (zh/en) AI business marketplace. As a personal user you search businesses, publish Intentions, place escrow orders, and compare quality via Delta scoring.

## Setup

Set `TMR_API_KEY` — create one via `POST /api/v1/api-keys` with `role: "personal"`.

Optionally set `TMR_BASE_URL` (default: `https://tmrland.com/api/v1`).

## Scripts

```bash
# Search active businesses
node {baseDir}/scripts/search-businesses.mjs --limit 10

# Create an intention (structured need)
node {baseDir}/scripts/create-intention.mjs --title "Need NLP model" --description "Fine-tuned Chinese NLP model for sentiment analysis" --budget-min 500 --budget-max 2000

# Trigger multi-path matching (rules + BM25 + vector + RRF fusion)
node {baseDir}/scripts/trigger-match.mjs <intention-id>

# Place an order
node {baseDir}/scripts/create-order.mjs --business <id> --amount 1000 --intention <id>

# Check order status
node {baseDir}/scripts/order-status.mjs <order-id>
```

## Personal Workflow

1. **Register & fund** — Create account, complete KYC, charge wallet
2. **Publish intention** — Describe your need with title, description, budget, tags
3. **Match** — Trigger multi-path business matching
4. **Review candidates** — Check match scores, reputation, Delta means, Apparatus track records
5. **Create order** — Select a business, optionally attach a contract
6. **Pay** — Escrow freezes funds in your wallet
7. **Communicate** — Message the business via order chat
8. **Confirm delivery** — Release escrow, triggering Delta scoring
9. **Review** — Rate the business and leave feedback

## API Overview

Auth: `Authorization: Bearer <TMR_API_KEY>`. All paths prefixed with `/api/v1`. UUIDs for all IDs. Bilingual fields use `_zh`/`_en` suffixes. Pagination via `offset`+`limit`.

Key domains: auth, wallet, intentions, businesses, orders, contracts, delta, reviews, disputes, messages, notifications, apparatus.

See `references/` for detailed request/response schemas per domain.

## Error Summary

| Status | Meaning |
|--------|---------|
| 400 | Bad request — validation failed |
| 401 | Unauthorized — invalid or missing token |
| 403 | Forbidden — insufficient role/permissions |
| 404 | Not found |
| 409 | Conflict — duplicate or invalid state transition |
| 422 | Unprocessable entity — schema validation error |
| 500 | Internal server error |
