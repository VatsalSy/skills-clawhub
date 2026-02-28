# NicheHunter Ultra — App Store Market Intelligence

Investor-grade App Store opportunity intelligence skill for OpenClaw (VPS).  
Discovers underserved niches, analyzes competitors, validates monetization signals, scores opportunities quantitatively, and generates build-ready MVP PRDs.

Designed for headless execution and Telegram interaction.

---

## What This Skill Does

Category Definition  
→ Market Demand Discovery  
→ Competitor Intelligence  
→ Gap Pattern Extraction  
→ Quantitative Scoring  
→ Market Intelligence Report  
→ MVP PRD (Rork-ready)

It does not guess ideas.  
It analyzes markets.

---

## Core Capabilities

- Detect validated demand clusters in any App Store category
- Analyze 5–8 competitors per niche
- Extract rating counts, pricing, complaint patterns
- Validate monetization (direct or proxy revenue estimation)
- Score opportunities using a weighted quantitative model
- Produce a structured Market Intelligence Report
- Generate an investor-grade MVP PRD optimized for Rork

---

## Quick Install

```bash
npx clawhub@latest install niche-hunter-app-store
```

---

## Runtime Requirements

Built for:

- OpenClaw running in a VPS (headless)
- Telegram chat-based execution

### Required Tool

- `web_search` — **mandatory**

If `web_search` is not available, the skill cannot operate.

### Optional Tool

- `web_fetch` — improves structured extraction but not required

No interactive browser needed.

---

## Execution Discipline

To ensure deterministic and professional output:

- Max 18 web_search calls per session
- Max 20 URLs analyzed
- Max 8 competitors per niche
- Max 20 reviews per app (prioritize 1★ and 3★)
- No duplicate queries
- Proxy revenue always labeled with confidence level

No speculation presented as fact.

---

## Quantitative Scoring Model

Each opportunity is scored 0–10 across four dimensions:

- Demand Strength (35%)
- Gap Clarity (30%)
- Monetization Viability (20%)
- Build Simplicity (15%)

Weighted Score:

```
(demand × 0.35) +
(gap × 0.30) +
(monetization × 0.20) +
(build × 0.15)
```

Every score must be justified with observed signals.

---

## Example Output (Telegram Format)

```
📊 MARKET INTELLIGENCE REPORT
Category: Health & Fitness
Research Confidence: Medium
```

### 🥇 Opportunity #1 — AI Companion + Pet Fitness

Strategic Positioning:  
Emotional AI fitness coach with gamified pet mechanics

Demand Evidence:
- Finch: 300K+ ratings
- Tolan: Top 10 Health category
- Strong emotional wellness demand

Monetization Evidence:
- $6.99/mo pricing benchmark
- Subscription standard across category
- Proxy revenue estimate based on rating conversion

Gap Evidence:
- No AI + pet mechanics combined
- Repeated personalization complaints
- Weak emotional engagement layer

Quantitative Scoring:
- Demand: 9/10  
- Gap: 8/10  
- Monetization: 8/10  
- Build Simplicity: 6/10  
- Weighted Score: 8.2 / 10  

Confidence: Medium–High

---

## Revenue Estimation Model

If direct revenue data is found → use it.

If not:

Freemium:
```
Estimated installs ≈ ratings × 100
```

Paid:
```
Estimated installs ≈ ratings × 40
```

Revenue:
```
installs × 3% conversion × subscription price
```

All proxy estimates labeled:
High / Medium / Low confidence.

---

## Output Structure

Each complete session produces:

1. Market Intelligence Report (ranked top 3 opportunities)
2. Quantitative scoring breakdown
3. Revenue validation logic
4. Strategic recommendation
5. Investor-grade MVP PRD (after user selection)

---

## PRD Output

After selecting an opportunity, the skill generates:

- Executive Summary
- Market Validation
- Target Personas
- Core Wedge Strategy
- MVP Feature Groups
- Screen Architecture (Expo Router structure)
- Monetization Strategy
- Tech Stack (Expo SDK 52+, TypeScript)
- Design System (hex colors included)
- KPIs
- Risk Analysis

PRD is copy-paste ready for:
https://rork.com/

---

## Categories Supported

Any iOS category, including:

- Health & Fitness  
- Productivity  
- Education  
- Finance  
- Lifestyle  
- Photo & Video  
- Entertainment  
- Food & Drink  
- Social Networking  
- Travel  
- Utilities  

---

## Ideal Use Cases

- Indie founders validating app ideas
- Product builders seeking underserved niches
- AI builders searching monetizable verticals
- Telegram-based research workflows
- OpenClaw autonomous market analysis

---

## Design Philosophy

NicheHunter Ultra is not an idea generator.  
It is a structured market analysis engine.

Every recommendation must show:

- Demand evidence
- Gap evidence
- Monetization logic
- Quantitative scoring
- Confidence level

No hype. Only signals.

---

## License

MIT
