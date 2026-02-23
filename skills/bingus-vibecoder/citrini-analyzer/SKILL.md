---
name: citrini-analyzer
description: Process and format Citrini Research thematic investment reports into structured Discord-ready summaries. Use when Bingus forwards Citrini Research emails (from Midas_Jaeger/Substack) for analysis. Produces executive summary, investment thesis breakdown, stock tables by mention count, conviction baskets, and risk assessment.
---

# Citrini Analyzer

Transforms Citrini Research thematic investment emails into structured, actionable reports for Discord delivery.

## Output Structure

Generate reports with this exact structure:

### 1. Header Block
```
**📧 Email Report: [THEME TITLE]**
**From:** Citrini Research (via Midas_Jaeger)
**Date:** [Article date if available, otherwise email received date]
**Source:** Substack article
```

### 2. Executive Summary
- Identify 3-5 core investment themes from the article
- For each theme, provide:
  - **Theme name in bold**
  - 2-3 sentence context/catalyst explanation
  - Key developments bullet list (3-6 items max)
  - Economic/strategic drivers

### 3. Investment Thesis (Per Theme)
For each major theme, create a dedicated section with:

**Key Developments:**
- Bullet list of catalysts, deployments, policy changes
- Focus on concrete events with dates when available
- Include economic comparison points (e.g., "$500 drone vs $50K interceptor")

**Investment Thesis - [Primary Stock Pick]:**
- **Why this stock** (unique positioning, pure-play status, vertical integration, etc.)
- Recent performance data (stock movement, revenue growth, margins)
- Key contracts/partnerships with dollar amounts
- Quarterly metrics if mentioned

**Valuation:**
- Current market cap and revenue multiple
- Bull case with specific upside target
- Bear case with downside estimate
- Risk/reward ratio

**Top Plays:** (for themes with multiple stocks)
- Stock ticker and name in bold
- 1-2 line summary of positioning
- Key metric (P/E, contract size, unique capability)

### 4. Stock Tables
Create two tables:

**TIER 1: PRIMARY FOCUS (10+ mentions)**

**Stock** | **Ticker** | **Mentions** | **Category** | **Key Points**

**TIER 2: STRONG CONVICTION (4-6 mentions)**

[Same structure]

**TIER 3: NOTABLE PLAYS (2-3 mentions)**

[Same structure]

**TIER 4: MENTIONED ONCE**

Comma-separated list with tickers in parentheses

### 5. Conviction Baskets
Extract author-curated baskets with exact stock lists:
```
**[Basket Name] Basket:** Stock1, Stock2, Stock3, etc.
```

### 6. Risk Factors
- Bullet list of key risks mentioned by author
- Include probability assessment if provided
- Note exposure types (regulatory, geopolitical, technical)

### 7. Conclusion
- 2-3 sentence synthesis of key takeaways
- Meta-commentary on investment approach if relevant

### 8. Footer
```
---
**Report complete. Original email forwarded from Midas_Jaeger, article by Citrini Research.**
```

## Formatting Rules

### Discord Compatibility
- **No markdown tables with pipes** — Discord renders them poorly
- Use simple text tables with column alignment via spaces
- Keep table column headers bold
- Separate tiers with blank lines

### Stock Mentions
- Count total mentions across entire article
- Include context mentions (e.g., "LASR customer" counts for both LASR and the customer)
- Tier by mention frequency for signal prioritization

### Emphasis
- Theme names: **Bold**
- Stock tickers: **Bold** on first mention in each section
- Key metrics: **Bold** (e.g., **PF 5.0**, **80% WR**)
- Emojis: Use sparingly for visual hierarchy (🏆🥈🥉🎯 for ranking, 📧📊📈🎯 for sections)

### Data Preservation
- Keep all dollar amounts, percentages, dates from source
- Preserve author's language for conviction signals ("just the start", "best proxy", "only true")
- Include ticker exchanges when provided (US/LN/CN/NO/FP/SW/SS/AU/KS)

## Analysis Guidelines

### Theme Extraction
- Look for section headers, repeated topics, or multi-paragraph deep dives
- Common Citrini themes: defense tech, geopolitics, commodities, infrastructure, asymmetric warfare

### Conviction Signals
- Author emphasis phrases ("most direct exposure", "only pure-play", "best proxy")
- Valuation frameworks (bull/bear cases, risk/reward ratios)
- Curated baskets = high conviction groupings
- Mention frequency = research depth

### Stock Categorization
- **Primary focus:** Deep dive with valuation, thesis, recent developments
- **Strong conviction:** Multiple paragraphs, specific catalysts
- **Notable:** Meaningful context but less detail
- **Mentioned once:** Name-dropped for completeness

## Edge Cases

### Missing Data
- If no date available: Use "Recent" or "2026"
- If no mention count: Estimate based on paragraphs dedicated
- If no valuation: Note "speculative" or "early-stage"

### Multiple Themes
- Separate with horizontal rules (`---`)
- Number themes if 4+
- Cross-reference stocks appearing in multiple themes

### Non-Standard Formats
- If article is interview/Q&A: Extract key points into thematic buckets first
- If article is portfolio update: Lead with performance data, then holdings breakdown
- If article is single-stock deep dive: Expand Investment Thesis section, condense others

## Reference Files

See `references/example-output.md` for the full Modern Warfare report template.
