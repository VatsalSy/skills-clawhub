---
name: niche-hunter-app-store
description: NicheHunter Ultra — Headless App Store Market Intelligence for OpenClaw (VPS). Uses web_search (+ web_fetch when available) to detect underserved niches, analyze competitors, validate monetization, score opportunities quantitatively, and generate investor-grade MVP PRDs — optimized for Telegram.
metadata:
  tags: app-store, market-intelligence, competitor-analysis, revenue-validation, scoring-model, prd, rork, openclaw, telegram
---

# NicheHunter Ultra — Market Intelligence Mode

Designed for:
- OpenClaw running in VPS (headless)
- Telegram chat interaction
- No interactive browser

---

# Required Tools

| Tool        | Requirement | Purpose |
|------------|------------|---------|
| `web_search` | REQUIRED   | Discover charts, competitors, reviews, revenue signals |
| `web_fetch`  | Optional   | Extract structured content from specific URLs |

If `web_search` is unavailable → STOP execution.

---

# Execution Discipline (Strict)

- Max 18 `web_search` calls
- Max 20 URLs analyzed total
- Max 8 competitors per niche
- Max 20 reviews per app (prioritize 1★ & 3★)
- No repeated queries
- If paywalled → try 1 alternative source only
- If signals weak → downgrade confidence

No hype. No speculation without labeling.

---

# Pipeline

1) Category Definition  
2) Market Demand Discovery  
3) Competitor Intelligence  
4) Gap Pattern Extraction  
5) Quantitative Scoring  
6) Market Intelligence Report  
7) PRD (after user selection)

Each step must output a checkpoint.

---

# Checkpoint Format

--- CHECKPOINT ---
Step: {1–7}
Category: {category}
Micro-niches: [...]
Top Competitors Analyzed: [...]
Chosen Opportunity: null | "{name}"
Next: {next step}
--- END CHECKPOINT ---

---

# Step 1 — Category Definition

Ask sequentially:
1) What problem space?
2) Consumer or B2B?
3) AI-heavy allowed or lean build?
4) Target monthly revenue?

Rewrite input into a precise niche statement:
Audience + pain + context + monetization angle.

Checkpoint required.

---

# Step 2 — Market Demand Discovery

Use `web_search` to find:
- Official App Store chart listings
- Top apps in niche
- Ranking mirrors / review aggregations

Extract:
- App name
- Rating count
- Star rating
- Monetization type
- Positioning summary

Cluster into 3–5 micro-niches.

Interpretation thresholds:

- >100K ratings → dominant market
- 10K–100K → strong demand
- 1K–10K → validated niche
- <500 → emerging or weak

Checkpoint required.

---

# Step 3 — Competitor Intelligence

For each micro-niche:
Analyze 5–8 competitors max.

Collect:

Demand Data:
- Rating count
- Chart presence
- App age (if detectable)

Monetization Data:
- Pricing model
- Subscription tiers
- Public revenue mentions

User Friction Data:
- Repeated 1★ complaints
- Feature frustration themes
- UX issues

Revenue Signals:
- Direct revenue sources (if found)
- Proxy install estimation

Checkpoint required.

---

# Revenue Estimation Model (When No Direct Data)

Freemium:
Estimated installs ≈ rating_count × 100

Paid:
Estimated installs ≈ rating_count × 40

Monthly Revenue ≈ installs × 3% × subscription_price

Label confidence:
High / Medium / Low

Never present proxy as fact.

---

# Step 4 — Gap Pattern Extraction

Identify:

- Repeated complaint themes
- Missing feature overlaps
- Overpriced positioning
- UX weaknesses
- Underserved sub-audiences

Define:
Primary Wedge (1–2 core differentiators)
Secondary Edge (nice-to-have advantage)

Checkpoint required.

---

# Step 5 — Quantitative Scoring Model

Score 0–10:

Demand Strength (35%)
Gap Clarity (30%)
Monetization Viability (20%)
Build Simplicity (15%)

Weighted Score =
(demand × 0.35) +
(gap × 0.30) +
(monetization × 0.20) +
(build × 0.15)

Scores must be justified with observed signals.

---

# Step 6 — MARKET INTELLIGENCE REPORT (Telegram Format)

═══════════════════════════════
📊 MARKET INTELLIGENCE REPORT
Category: {Category}
Research Confidence: {High | Medium | Low}
═══════════════════════════════

## 🥇 Opportunity #1 — {Name}

🎯 Strategic Positioning:
{Concise 1-line pitch}

📈 Demand Evidence:
- Key competitors:
- Rating ranges:
- Chart visibility:
- Growth indicators:

💰 Monetization Evidence:
- Pricing benchmark:
- Revenue signals:
- Proxy estimate (if used):
- Assumed conversion rate:

🧩 Gap Evidence:
- Repeated complaints:
- Missing feature overlap:
- UX weaknesses:

⚙️ Build Complexity:
{Low | Medium | High}
Reasoning:

📊 Quantitative Scoring:
Demand: X/10
Gap: X/10
Monetization: X/10
Build Simplicity: X/10
Weighted Score: X.X / 10

Confidence Level: {High | Medium | Low}

───────────────────────────────

## 🥈 Opportunity #2
(Concise but same structure)

───────────────────────────────

## 🥉 Opportunity #3
(Concise but same structure)

═══════════════════════════════
🏁 Strategic Conclusion
Why #1 ranks highest (data-based reasoning only).
═══════════════════════════════

Ask user to choose #1 / #2 / #3 before PRD.

Checkpoint required.

---

# Step 7 — Investor-Grade MVP PRD (After Selection)

Structure:

1) Executive Summary
2) Market Validation Summary
3) Target Personas (2–3)
4) Core Differentiator (Wedge)
5) MVP Feature Set (grouped)
6) Screen Architecture (tabs + stacks)
7) Monetization Strategy
8) Tech Stack:
   - Expo SDK 52+
   - TypeScript
   - Expo Router
9) Design System:
   - Hex colors mandatory
   - Typography
   - Component style
10) KPIs (activation, retention, conversion)
11) Risks & Mitigations

Rules:
- Concrete UI components described
- Mock data examples included
- No fluff
- Build-ready
- Copy-paste friendly for Rork

Checkpoint required.

---

# Telegram Constraints

- No wide tables
- Bullet structures preferred
- Split long outputs logically
- Stay under ~2000 characters per message
- Resume on “continue”
- Match user language
