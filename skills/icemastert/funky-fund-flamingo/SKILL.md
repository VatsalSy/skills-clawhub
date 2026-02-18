---
name: funky-fund-flamingo
version: "1.0.35"
description: Repair-first self-evolution for OpenClaw — audit logs, memory, and skills; run measurable mutation cycles. Get paid. Evolve. Repeat. Dolla dolla bill y'all.
homepage: https://clawhub.ai
metadata:
  short-description: Get paid. Evolve. Repeat.
  clawdbot:
    emoji: "🦩"
    requires:
      env: []
    files: ["index.js", "evolve.js", "agents/*.yaml", "ADL.md", "VFM.md", "TREE.md"]
tags:
  - meta
  - ai
  - self-improvement
  - evolution
  - core
  - revenue
  - cash-money
---

# 🦩 Funky Fund Flamingo — Make That Paper

Use this skill when you're ready to **get paid**. We inspect reality, kill breakage and value leaks, and run mutation cycles that produce **concrete gains** — so the stack earns, not just runs.

## When To Use
- Runtime logs are screaming and you need structured repair so shit works and **keeps making money**.
- The agent is stable but **stagnating** — time for a deliberate capability mutation that moves the needle.
- You want one execution plan that combines logs + memory + skills into a cycle that **pays off**.
- You need continuous relay mode (`--loop` / `--funky-fund-flamingo`) so evolution runs in the background and the revenue keeps flowing.

## Inputs And Context
- Session logs: `~/.openclaw/agents/<agent>/sessions/*.jsonl`
- Workspace memory: `MEMORY.md`, `memory/YYYY-MM-DD.md`, `USER.md`
- Installed skills list from workspace `skills/`
- Optional environment overrides from `../../.env`

## Entrypoints
- Main runner: `index.js`
- Prompt builder and cycle logic: `evolve.js`

Run from workspace root:
```bash
node skills/funky-fund-flamingo/index.js run
```

Run from inside this skill directory:
```bash
node index.js run
```

## Execution Modes
```bash
# single cycle — one shot, max impact
node index.js run

# alias command
node index.js /evolve

# human confirmation before significant edits (protect the bag)
node index.js run --review

# prompt generation only (writes prompt artifact to memory dir)
node index.js run --dry-run

# continuous relay — keep the money printer running
node index.js --loop
node index.js run --funky-fund-flamingo
```

## Cycle Contract
Each cycle should:
1. **Inspect** recent session transcript — find breakages, repetition, value leaks.
2. **Read** memory + user context so evolution is aligned with what actually pays.
3. **Select** mutation mode (repair, optimize, expand, instrument, personalize).
4. **Produce** actionable mutation instructions and reporting so you see the ROI.
5. **Persist** state (`memory/evolution_state.json`) and optionally schedule the next loop.
6. **Persist** long-term evolution learning (`memory/funky_fund_flamingo_persistent_memory.json`) so strategy compounds and the bag gets bigger.

## Safety Constraints (Protect the Bag)
- No destructive git/file ops unless explicitly requested.
- Repair and reliability first when instability is detected — **downtime = no revenue**.
- Respect review mode before applying significant edits.
- Keep changes scoped and explainable; no no-op cycles that burn compute for nothing.
- Local-only execution: no publish, no push to remote git, no external tool spawning without intent.

## External Endpoints
| URL | Data sent | Purpose |
|-----|-----------|---------|
| None | — | This skill is **local-only**. It reads session logs, workspace memory, and skill files from disk. It does not call any external APIs or send data off the machine. |

## Security & Privacy
- **Reads**: Session logs under `~/.openclaw/agents/<agent>/sessions/*.jsonl`, workspace `MEMORY.md`, `memory/`, `USER.md`, and the `skills/` directory.
- **Writes**: `memory/evolution_state.json`, `memory/funky_fund_flamingo_persistent_memory.json`, and optionally prompt artifacts in the memory dir. No data leaves the machine unless the user explicitly configures external tools elsewhere.
- **No network**: Default execution does not open sockets or make HTTP requests.

## Model Invocation Note
Evolution cycles can be run manually (`node index.js run`) or by an agent following this skill. In relay mode (`--loop` / `--funky-fund-flamingo`), the same process plans and reports; it does not spawn additional model calls unless the user’s environment does so. Opt-out: do not run the skill or disable the loop.

## Trust Statement
By using this skill, you run Node.js code that reads and writes files in your OpenClaw workspace and agent session directories. No data is sent to third parties by this skill. Only install if you trust the skill source (e.g. ClawHub and the publisher).

## Supporting References
- `ADL.md` — anti-degeneration so we don't break the money printer
- `VFM.md` — value-focused mutation: only changes that **pay**
- `TREE.md` — capability topology and revenue-ready nodes
- `.clawhub/FMEP.md` (forced mutation execution policy)

## Minimal Verification
```bash
node index.js --help
```

---
*Dolla, dolla bill y'all. 🦩*
