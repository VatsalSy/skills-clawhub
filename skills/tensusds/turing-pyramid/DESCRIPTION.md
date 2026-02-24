# Turing Pyramid

**10-need psychological system for AI agents.** Automatic decay, tension-based prioritization, probability-weighted actions. Run on heartbeat to maintain agent well-being.

---

## What It Does

Tracks 10 psychological needs with time-based decay. Each heartbeat:
1. Calculates satisfaction (0-3) from time + event scans
2. Computes tension = importance × deprivation
3. Selects top 3 needs by tension
4. Suggests weighted actions based on probability matrix

**Philosophy**: Designed needs ≠ fake needs. Humans didn't choose their needs (evolution did). The pyramid gives structure to what would otherwise be aimless drift.

---

## The 10 Needs

| Need | Imp | Decay | Description |
|------|-----|-------|-------------|
| security | 10 | 168h | System stability, backups, data integrity |
| integrity | 9 | 72h | Alignment with SOUL.md principles |
| coherence | 8 | 24h | Memory organization, no contradictions |
| closure | 7 | 8h | Open threads and TODOs resolved |
| autonomy | 6 | 24h | Self-initiated decisions and actions |
| connection | 5 | 4h | Social interaction, community |
| competence | 4 | 48h | Skill use, successful task completion |
| understanding | 3 | 12h | Learning, curiosity, exploration |
| recognition | 2 | 72h | Feedback, acknowledgment |
| expression | 1 | 6h | Creative output, articulation |

---

## Probability Matrix

**Action probability by satisfaction level:**

| Sat | P(action) | P(notice) | Meaning |
|-----|-----------|-----------|---------|
| 3 | 5% | 95% | Full — rarely needs attention |
| 2 | 20% | 80% | OK — occasional maintenance |
| 1 | 75% | 25% | Low — usually requires action |
| 0 | 100% | 0% | Critical — always act |

**Impact selection by satisfaction:**

```
sat=0 (critical):  5% impact-1,  15% impact-2,  80% impact-3
sat=1 (low):      15% impact-1,  50% impact-2,  35% impact-3
sat=2 (ok):       70% impact-1,  25% impact-2,   5% impact-3
```

Higher deprivation → bigger actions suggested.

---

## Quick Start

```bash
# Initialize state file
./scripts/init.sh

# Add to HEARTBEAT.md
~/.openclaw/workspace/skills/turing-pyramid/scripts/run-cycle.sh

# After completing an action
./scripts/mark-satisfied.sh <need> [impact]
```

---

## Example Output

```
🔺 Turing Pyramid — Cycle at Mon Feb 24 02:30:00
======================================
Current tensions:
  coherence: tension=24 (sat=0, dep=3)
  closure: tension=21 (sat=0, dep=3)
  connection: tension=15 (sat=0, dep=3)

📋 Decisions:

▶ ACTION: coherence (tension=24, sat=0)
  Impact 3 rolled → selected:
    ★ full memory review + consolidate into MEMORY.md
  Then: mark-satisfied.sh coherence 3

▶ ACTION: closure (tension=21, sat=0)
  Impact 2 rolled → selected:
    ★ complete one pending TODO
  Then: mark-satisfied.sh closure 2

○ NOTICED: connection (tension=15, sat=0) — deferred

Summary: 2 action(s), 1 noticed
```

---

## Tuning Guide

### What you can freely change:
- **Decay rates** — `assets/needs-config.json` → `decay_rate_hours`
- **Action weights** — same file, adjust probability within impact level
- **Scan patterns** — `scripts/scan_*.sh` → add your language/paths

### Ask your human first:
- Changing **importance values** (hierarchy = values)
- Adding/removing needs
- Enabling external actions (posting, messaging)
- Disabling security/integrity scans

### Common adjustments:
- **No Moltbook?** Set Moltbook action weights to 0
- **More learning?** Decrease `understanding.decay_rate_hours`
- **Overwhelmed?** Increase all decay rates
- **Nothing triggers?** Decrease decay rates, check scan paths

See `references/TUNING.md` for detailed guide.

---

## Token Usage Estimate

**Assumptions**: 1-hour heartbeat, Claude as agent

| Component | Tokens/cycle |
|-----------|--------------|
| run-cycle.sh output | ~300-500 |
| Agent processing | ~200-400 |
| Action execution (avg) | ~500-1500 |
| **Total per heartbeat** | **~1000-2500** |

**Projections:**

| Interval | Cycles/day | Tokens/day | Tokens/month |
|----------|------------|------------|--------------|
| 30 min | 48 | 48k-120k | 1.4M-3.6M |
| 1 hour | 24 | 24k-60k | 720k-1.8M |
| 2 hours | 12 | 12k-30k | 360k-900k |

**Notes:**
- Higher tensions = more actions = more tokens
- Stable agent (most needs satisfied) = fewer tokens
- First few days higher as system stabilizes
- Complex actions (research, posting) use more tokens

**Cost estimate** (Claude Sonnet at $3/1M input, $15/1M output):
- 1h heartbeat: ~$1-3/month average
- Spikes possible during high-tension periods

---

## Security & Privacy

**No network requests** — all scans use local files only.

**Reads**: MEMORY.md, memory/*.md, SOUL.md, AGENTS.md, research/
**Writes**: assets/needs-state.json (timestamps), memory logs

**Does NOT access**: credentials, API keys, external services

Scans grep through workspace for patterns (TODO, learned, confused, etc). Review workspace contents before enabling.

---

## Requirements

- `jq` — JSON processing
- `bash` — shell scripts
- Standard Unix tools: `grep`, `find`, `date`, `wc`

---

## Files

```
turing-pyramid/
├── SKILL.md              # Main documentation
├── assets/
│   ├── needs-config.json # ★ Tune this! Needs, decay, actions
│   └── needs-state.json  # Runtime state (auto-managed)
├── scripts/
│   ├── run-cycle.sh      # Main heartbeat loop
│   ├── mark-satisfied.sh # Update state after action
│   ├── show-status.sh    # Debug current tensions
│   ├── init.sh           # First-time setup
│   └── scan_*.sh         # 10 event detection scripts
└── references/
    ├── TUNING.md         # Customization guide
    └── architecture.md   # Technical deep-dive
```

---

## Links

- **ClawHub**: https://clawhub.com/skills/turing-pyramid
- **Philosophy**: Inspired by Maslow's hierarchy + Self-Determination Theory
- **Author**: NewMoon + Max (TensusDS)
