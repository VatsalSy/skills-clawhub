# ClawSaver

> 💡 **Did you know?** Every message re-sends your full workspace context before it gets to your question — SOUL.md, MEMORY.md, AGENTS.md, conversation history, all of it. Ask 3 related things in 3 separate turns and you pay to load that context 3 times. ClawSaver gives your agent the judgment to consolidate.

ClawSaver is a **behavior-change skill** — it teaches your agent to recognize when multiple asks can be answered together, and to proactively offer consolidation. Fewer round-trips, less repeated context overhead, same quality output.

> **How it works:** ClawSaver shapes agent behavior through instructions, the same way execution-loop-breaker and most top ClawHub skills work. It doesn't intercept requests at the network level — it trains the agent to notice batchable patterns and act on them. Think of it as giving your agent good judgment about when to consolidate, not a router that does it automatically.

---

## Quick Start

```
/batch
```

The agent will review your recent messages and offer to consolidate related open threads into one response.

---

## Commands

| Command | What it does |
|---------|--------------|
| `/batch` | Review recent asks, offer to consolidate |
| `/batch status` | Show batching activity this session |
| `/batch off` | Disable automatic batch detection |
| `/batch on` | Re-enable (on by default when skill is loaded) |

---

## What It Looks Like

When ClawSaver consolidates 3 related questions:

```
╭──────────────────────────────────────────────╮
│  💸 ClawSaver — Batching 3 asks → 1 response │
╰──────────────────────────────────────────────╯

**Code review**
No bugs found. The null check on line 14 is correct.

**Performance**
The nested loop on line 47 is O(n²) — consider a Map for O(n).

**Test coverage**
Missing edge case: empty array input.

---
💸 Batched 3 asks → 1 response · Est. savings: ~2 API calls · ~800 tokens
```

Without ClawSaver, those 3 questions would have each re-sent your full workspace context.

---

## Batch vs. Don't Batch

| Scenario | Action |
|---------|--------|
| Multiple questions, same topic | ✅ Batch |
| Code review + next steps + tests | ✅ Batch |
| Follow-up, same subject (≤3 turns) | ✅ Offer |
| Task B needs Task A output | ❌ Separate |
| Completely unrelated topics | ❌ Separate |
| "Answer each separately" | ❌ Defer |

---

## Decision Rules

| Signal | Rule |
|--------|------|
| 2+ questions, same topic | Always batch |
| Follow-up within 3 turns | Offer to batch |
| Same file/URL twice | Cache & reuse |
| Clarifying Q from context | Anticipate |
| A feeds B | Separate |
| 3+ unrelated domains | Separate |

---

## Why Context Overhead Dominates Costs

Every OpenClaw session re-sends workspace files with each request — SOUL.md, MEMORY.md, AGENTS.md, conversation history. This context grows over time and gets re-sent on every single turn, whether or not it's relevant to your question.

The more you ask in separate messages, the more times you pay for that overhead. Batching 3 related asks into 1 means paying it once instead of three times — same answers, fraction of the cost.

---

## Savings by Billing Model

### 💰 Token-based (OpenRouter, Anthropic, OpenAI)

Each batched turn eliminates one full context re-send.

| Session | Before | After | Saved |
|---------|--------|-------|-------|
| Code review (3-part) | ~9,000 tok | ~4,500 tok | ~50% |
| Config questions (5) | ~15,000 tok | ~6,000 tok | ~60% |
| Research & summary | ~12,000 tok | ~5,000 tok | ~58% |
| Status + next steps | ~6,000 tok | ~3,500 tok | ~42% |
| Unrelated tasks | — | — | 0% |

### 🎫 Call-based / quota (GitHub Copilot, enterprise)

Each batched turn saves a request from your allocation.

| Session | Before | After | Saved |
|---------|--------|-------|-------|
| Code review (3-part) | 3 req | 1 req | 67% |
| Research & summary | 3 req | 1 req | 67% |
| Config questions (5) | 5 req | 2 req | 60% |
| Status + next steps | 2 req | 1 req | 50% |
| Unrelated tasks | 2 req | 2 req | 0% |

---

## Installation

**Step 1 — Install the skill:**
```bash
clawhub install clawsaver
```

**Step 2 — Register it in `openclaw.json`:**

**Global registry** (available across all agents):
```json
{
  "skills": {
    "entries": {
      "clawsaver": { "enabled": true }
    }
  }
}
```

**Per-agent** (scoped to a specific agent):
```json
{
  "agents": {
    "list": [
      {
        "id": "your-agent-id",
        "skills": ["clawsaver"]
      }
    ]
  }
}
```

**Step 3 — Restart the gateway:**
```bash
openclaw gateway restart
```

ClawSaver is now active every session automatically.

---

## Safety

- ✅ **Never merges sequential tasks** — if result A feeds task B, they stay separate
- ✅ **Never compresses for brevity** — batched responses are structured, not squeezed
- ✅ **Never assumes context** — if combining requires guessing, it asks instead
- ✅ **Explicit opt-out** — "answer each one separately" and ClawSaver defers immediately

---

## About the Name

**ClawSaver** — because it saves your claws (and your cash) for what matters.

*CLAVSAVER: Combines Linked Asks into Well-structured Sets for Affordable, Verified, Efficient Responses*

---

## Version History

- **1.4.0** — Removed analyze.py; pure behavior-change skill, zero credentials, zero scripts
- **1.3.3** — Declared `OPENROUTER_MANAGEMENT_KEY` in skill metadata (optional env); analyzer marked optional
- **1.3.0** — Dual registration in `skills.entries` + `agents.list`; updated install docs
- **1.2.0** — Added `openclaw.json` installation instructions; dogfooded on own instance
- **1.1.0** — Added `/batch` commands, dashboard preview, visceral cost hook, ✅ safety format
- **1.0.0** — Initial release

---

*Built for [OpenClaw](https://openclaw.ai) · Listed on [ClawHub](https://clawhub.ai)*
