# Turing Pyramid

10-need psychological hierarchy for AI agents. Run on heartbeat → get prioritized actions.

**Customization:** Tune decay rates, weights, patterns. Defaults are starting points. See `TUNING.md`.

**Ask your human before:** Changing importance values, adding/removing needs, enabling external actions.

---

## Requirements

**System binaries (must be in PATH):**
```
bash, jq, grep, find, date, wc, bc
```

**Environment (REQUIRED — no fallback):**
```bash
# Scripts will ERROR if WORKSPACE is not set
export WORKSPACE="/path/to/your/workspace"
```
⚠️ **No silent fallback.** If WORKSPACE is unset, scripts exit with error.
This prevents accidental scanning of unintended directories.

---

## Quick Start

```bash
./scripts/init.sh                        # First time
./scripts/run-cycle.sh                   # Every heartbeat  
./scripts/mark-satisfied.sh <need> [impact]  # After action
```

---

## The 10 Needs

```
┌───────────────┬─────┬───────┬─────────────────────────────────┐
│ Need          │ Imp │ Decay │ Meaning                         │
├───────────────┼─────┼───────┼─────────────────────────────────┤
│ security      │  10 │ 168h  │ System stability, no threats    │
│ integrity     │   9 │  72h  │ Alignment with SOUL.md          │
│ coherence     │   8 │  24h  │ Memory consistency              │
│ closure       │   7 │  12h  │ Open threads resolved           │
│ autonomy      │   6 │  24h  │ Self-directed action            │
│ connection    │   5 │   6h  │ Social interaction              │
│ competence    │   4 │  48h  │ Skill use, effectiveness        │
│ understanding │   3 │  12h  │ Learning, curiosity             │
│ recognition   │   2 │  72h  │ Feedback received               │
│ expression    │   1 │   8h  │ Creative output                 │
└───────────────┴─────┴───────┴─────────────────────────────────┘
```

---

## Core Logic

**Satisfaction:** 0.0–3.0 (floor=0.5 prevents paralysis)  
**Tension:** `importance × (3 - satisfaction)`

### Action Probability

```
┌───────┬────────┬──────────────────────┐
│ Sat   │ Base P │ Note                 │
├───────┼────────┼──────────────────────┤
│ 3     │   5%   │ Maintenance mode     │
│ 2     │  20%   │ Routine checks       │
│ 1     │  75%   │ Needs attention      │
│ 0     │ 100%   │ Critical — always    │
└───────┴────────┴──────────────────────┘
```

**Tension bonus:** `bonus = (tension × 50) / max_tension`

### Impact Selection

```
┌─────────┬───────┬────────┬───────┐
│ Sat     │ Small │ Medium │ Big   │
├─────────┼───────┼────────┼───────┤
│ 0 crit  │   5%  │   15%  │  80%  │
│ 1 low   │  15%  │   50%  │  35%  │
│ 2 ok    │  70%  │   25%  │   5%  │
└─────────┴───────┴────────┴───────┘
```

**ACTION** = do it, then `mark-satisfied.sh`  
**NOTICED** = logged, deferred

---

## Protection Mechanisms

```
┌─────────────┬───────┬────────────────────────────────────────┐
│ Mechanism   │ Value │ Purpose                                │
├─────────────┼───────┼────────────────────────────────────────┤
│ Floor       │  0.5  │ Minimum sat — prevents collapse        │
│ Ceiling     │  3.0  │ Maximum sat — prevents runaway         │
│ Cooldown    │   4h  │ Deprivation cascades once per 4h       │
│ Threshold   │  1.0  │ Deprivation only when sat ≤ 1.0        │
└─────────────┴───────┴────────────────────────────────────────┘
```

**Base Needs Isolation:** Security (10) and Integrity (9) are protected:
- They influence lower needs (security → autonomy)
- Lower needs cannot drag them down
- Only `integrity → security (+0.15)` and `autonomy → integrity (+0.20)` exist

---

## Cross-Need Impact

**on_action:** Completing A boosts connected needs  
**on_deprivation:** A staying low (sat ≤ 1.0) drags others down

```
┌─────────────────────────┬──────────┬─────────────┬───────────────────────┐
│ Source → Target         │ on_action│ on_deprived │ Why                   │
├─────────────────────────┼──────────┼─────────────┼───────────────────────┤
│ expression → recognition│   +0.25  │      -0.10  │ Express → noticed     │
│ connection → expression │   +0.20  │      -0.15  │ Social sparks ideas   │
│ connection → understand │   -0.05  │         —   │ Socratic effect       │
│ competence → recognition│   +0.30  │      -0.20  │ Good work → respect   │
│ autonomy → integrity    │   +0.20  │      -0.25  │ Act on values         │
│ closure → coherence     │   +0.20  │      -0.15  │ Threads → order       │
│ security → autonomy     │   +0.10  │      -0.20  │ Safety enables risk   │
└─────────────────────────┴──────────┴─────────────┴───────────────────────┘
```

### Tips

- **Leverage cascades:** Connection easy? Do it first — boosts expression (+0.20)
- **Watch spirals:** expression ↔ recognition can create mutual deprivation
- **Autonomy is hub:** Receives from 5 sources. Keep healthy.
- **Socratic effect:** connection → understanding: -0.05. Dialogue exposes ignorance. Healthy!

Full matrix: `assets/cross-need-impact.json`

---

## Example Cycle

```
🔺 Turing Pyramid — Cycle at Tue Feb 25 05:36
======================================

⚠️ Deprivation cascades:
   autonomy (sat=0.5) → integrity: -0.25 (now: 1.75)
   autonomy (sat=0.5) → expression: -0.20 (now: 0.80)

Current tensions:
  closure: tension=21 (sat=0, dep=3)
  connection: tension=15 (sat=0, dep=3)

📋 Decisions:

▶ ACTION: closure (tension=21, sat=0.00)
  → coherence: +0.20, competence: +0.15, autonomy: +0.10

▶ ACTION: connection (tension=15, sat=0.00)
  → expression: +0.20, recognition: +0.15
  → understanding: -0.05 (Socratic effect)
```

---

## Integration

Add to `HEARTBEAT.md`:
```bash
/path/to/skills/turing-pyramid/scripts/run-cycle.sh
```

---

## Customization

### You Can Tune (no human needed)

**Decay rates** — `assets/needs-config.json`:
```json
"connection": { "decay_rate_hours": 4 }
```
Lower = decays faster. Higher = persists longer.

**Action weights** — same file:
```json
{ "name": "reply to mentions", "impact": 2, "weight": 40 }
```
Higher weight = more likely selected. Set 0 to disable.

**Scan patterns** — `scripts/scan_*.sh`:
Add your language patterns, file paths, workspace structure.

### Ask Your Human First

- **Adding needs** — The 10-need hierarchy is intentional. Discuss first.
- **Removing needs** — Don't disable security/integrity without agreement.

---

## File Structure

```
turing-pyramid/
├── SKILL.md                    # This file
├── CHANGELOG.md                # Version history
├── assets/
│   ├── needs-config.json       # ★ Main config (tune this!)
│   ├── cross-need-impact.json  # ★ Cross-need matrix
│   └── needs-state.json        # Runtime state (auto)
├── scripts/
│   ├── run-cycle.sh            # Main loop
│   ├── mark-satisfied.sh       # State + cascades
│   ├── apply-deprivation.sh    # Deprivation cascade
│   └── scan_*.sh               # Event detectors (10)
└── references/
    ├── TUNING.md               # Detailed tuning guide
    └── architecture.md         # Technical docs
```

---

## Security Model

**Decision framework, not executor.** Outputs suggestions — agent decides.

```
┌─────────────────────┐      ┌─────────────────────┐
│   TURING PYRAMID    │      │       AGENT         │
├─────────────────────┤      ├─────────────────────┤
│ • Reads local JSON  │      │ • Has web_search    │
│ • Calculates decay  │ ───▶ │ • Has API keys      │
│ • Outputs: "★ do X" │      │ • Has permissions   │
│ • Zero network I/O  │      │ • DECIDES & EXECUTES│
└─────────────────────┘      └─────────────────────┘
```

### ⚠️ Security Warnings

```
┌────────────────────────────────────────────────────────────────┐
│ THIS SKILL READS WORKSPACE FILES THAT MAY CONTAIN PII         │
│ AND OUTPUTS ACTION SUGGESTIONS THAT CAPABLE AGENTS MAY        │
│ AUTO-EXECUTE USING THEIR OWN CREDENTIALS.                     │
└────────────────────────────────────────────────────────────────┘
```

**1. Sensitive file access (no tokens required):**
- Scans read: `MEMORY.md`, `memory/*.md`, `SOUL.md`, `AGENTS.md`
- Also scans: `research/`, `scratchpad/` directories
- Risk: May contain personal notes, PII, or secrets
- **Mitigation:** Edit `scripts/scan_*.sh` to exclude sensitive paths:
  ```bash
  # Example: skip private directory
  find "$MEMORY_DIR" -name "*.md" ! -path "*/private/*"
  ```

**2. Action suggestions may trigger auto-execution:**
- Config includes: "web search", "post to Moltbook", "verify vault"
- This skill outputs text only — it CANNOT execute anything
- Risk: Agent runtimes with auto-exec may act on suggestions
- **Mitigation:** In `assets/needs-config.json`, remove or disable external actions:
  ```json
  {"name": "post to Moltbook", "impact": 2, "weight": 0}
  ```
  Or configure your agent runtime to require approval for external actions.

**3. Self-reported state (no verification):**
- `mark-satisfied.sh` trusts caller input
- Risk: State can be manipulated by dishonest calls
- Impact: Only affects this agent's own psychological accuracy
- **Mitigation:** Enable action logging in `memory/` to audit completions:
  ```bash
  # run-cycle.sh already logs to memory/YYYY-MM-DD.md
  # Review logs periodically for consistency
  ```

### Script Audit (v1.10.9)

**scan_*.sh files verified — NO network or system access:**
```
┌─────────────────────────────────────────────────────────┐
│ ✗ curl, wget, ssh, nc, fetch     — NOT FOUND           │
│ ✗ /etc/, /var/, /usr/, /root/    — NOT FOUND           │
│ ✗ .env, .pem, .key, .credentials — NOT FOUND           │
├─────────────────────────────────────────────────────────┤
│ ✓ Used: grep, find, wc, date, jq — local file ops only │
│ ✓ find uses -P flag (never follows symlinks)           │
└─────────────────────────────────────────────────────────┘
```

**Symlink protection:** All `find` commands use `-P` (physical) mode — symlinks pointing outside WORKSPACE are not followed.

**Scan confinement:** Scripts only read paths under `$WORKSPACE`. Verify with:
```bash
grep -nE "\b(curl|wget|ssh)\b" scripts/scan_*.sh     # network tools
grep -rn "readlink\|realpath" scripts/               # symlink resolution
```

---

## Token Usage

```
┌──────────────┬─────────────┬────────────┐
│ Interval     │ Tokens/mo   │ Est. cost  │
├──────────────┼─────────────┼────────────┤
│ 30 min       │ 1.4M-3.6M   │ $2-6       │
│ 1 hour       │ 720k-1.8M   │ $1-3       │
│ 2 hours      │ 360k-900k   │ $0.5-1.5   │
└──────────────┴─────────────┴────────────┘
```

Stable agent with satisfied needs = fewer tokens.

---

## Version

**v1.10.1** — Bug fixes, cleaned docs. Full changelog: `CHANGELOG.md`
