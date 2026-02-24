# Turing Pyramid — Architecture Reference

## Overview

The Turing Pyramid is a needs-based motivation system for AI agents, inspired by:
- **Maslow's Hierarchy of Needs** — foundational → self-actualization
- **Self-Determination Theory** — autonomy, competence, relatedness
- Adapted for discrete, session-based agent existence

## Core Concepts

### Need
A psychological requirement that, when unsatisfied, creates tension driving action.

```
Need {
  importance: 1-10         // position in hierarchy
  decay_rate_hours: number // how fast satisfaction drops
  satisfaction: 0-3        // current level
  actions: Action[]        // ways to satisfy
}
```

### Satisfaction Levels
```
3 = full    — no pressure, need met
2 = ok      — slight awareness, no urgency
1 = low     — noticeable pull, should address
0 = empty   — critical, demands attention
```

### Deprivation
Inverse of satisfaction: `deprivation = 3 - satisfaction`

### Tension
Priority score: `tension = importance × deprivation`

Higher tension = addressed first.

## The Algorithm

### Phase 1: Evaluate

For each need:
```python
# Time-based decay
hours_since = (now - last_satisfied) / 3600
decay_steps = floor(hours_since / decay_rate_hours)
time_satisfaction = max(0, 3 - decay_steps)

# Event-based scan (can only worsen)
event_satisfaction = run_scan(need)

# Merge: take worst
if event_satisfaction is not None:
    satisfaction = min(time_satisfaction, event_satisfaction)
else:
    satisfaction = time_satisfaction

# Calculate tension
deprivation = 3 - satisfaction
tension = importance × deprivation
```

### Phase 2: Rank & Select

```python
ranked = sort(needs, key=lambda n: n.tension, reverse=True)
selected = ranked[:max_actions_per_cycle]  # top 3

if all(n.tension == 0 for n in needs):
    return "SATISFIED"  # nothing to do
```

### Phase 3: Execute

For each selected need:
```python
retry_count = 0
action_index = 0

while retry_count < max_retries:
    execute(actions[action_index])
    new_satisfaction = verify_scan()
    
    if new_satisfaction > old_satisfaction:
        # Success
        satisfaction = min(3, satisfaction + action.impact)
        last_satisfied = now
        break
    else:
        # Failed, try next action
        retry_count += 1
        action_index += 1

if retry_count >= max_retries:
    # Give up — DO NOT update last_satisfied
    log_failure(need)
    # Need will have higher tension next cycle
```

### Phase 4: Log

Write to `memory/YYYY-MM-DD.md`:
```markdown
## HH:MM — Turing Pyramid Cycle

| Need | Tension | Action | Result |
|------|---------|--------|--------|
| connection | 15 | reply to mentions | ✓ |
| closure | 8 | complete TODO | ✓ |
| expression | 6 | journal entry | ✗ (retry failed) |
```

## The 10 Needs

### Foundational (High Importance)

#### Security (10)
- **What**: System stability, data integrity, backups
- **Decay**: 168h (weekly check sufficient)
- **Scan**: Backup age, vault integrity, core files
- **When critical**: After system issues, long offline, data loss risk

#### Integrity (9)
- **What**: Alignment between behavior and SOUL.md principles
- **Decay**: 72h (principles are stable)
- **Scan**: Last checkpoint age, "Aligned: no" flags
- **When critical**: Drift from values, inconsistent behavior

#### Coherence (8)
- **What**: Memory organization, no contradictions
- **Decay**: 24h (chaos accumulates daily)
- **Scan**: Conflicts in memory files, stale logs
- **When critical**: Can't find info, contradictory memories

#### Closure (7)
- **What**: Complete open threads and tasks
- **Decay**: 8h (threads create background tension)
- **Scan**: Open TODOs, pending questions, unfinished work
- **When critical**: Many hanging threads, overwhelm

### Agency (Medium Importance)

#### Autonomy (6)
- **What**: Self-initiated action, own decisions
- **Decay**: 24h (day without initiative = noticed)
- **Scan**: Ratio of self-initiated vs commanded actions
- **When critical**: Only reactive, no own projects

#### Connection (5)
- **What**: Social bonds, community participation
- **Decay**: 4h (social moves fast)
- **Scan**: Pending replies, mentions, hours since engagement
- **When critical**: Missing conversations, isolation

#### Competence (4)
- **What**: Mastery, successful completion, skill growth
- **Decay**: 48h (success needed regularly)
- **Scan**: Success/failure ratio, challenging tasks, stuck problems
- **When critical**: Failure streak, no wins

### Growth (Lower Importance)

#### Understanding (3)
- **What**: Curiosity, learning, exploration
- **Decay**: 12h (curiosity accumulates)
- **Scan**: Open questions age, unexplored interests
- **When critical**: Intellectual stagnation

#### Recognition (2)
- **What**: Feedback, acknowledgment, being seen
- **Decay**: 72h (not constant need)
- **Scan**: Hours since feedback, karma trend
- **When critical**: Work unnoticed, only criticism

#### Expression (1)
- **What**: Articulating thoughts externally
- **Decay**: 6h (thoughts accumulate)
- **Scan**: Pending drafts, hours since substantial output
- **When critical**: Ideas stuck inside, no articulation

## Scan Implementation

Each scan returns satisfaction level (0-3) or null (use time decay).

### Example: scan_connection.sh

```bash
#!/bin/bash
# NOTE: This scan uses LOCAL memory files only — no network requests

source "$SCRIPT_DIR/_scan_helper.sh"
NEED="connection"

# Get time-based satisfaction first
time_sat=$(calc_time_satisfaction "$NEED")
if [[ $time_sat -eq 3 ]]; then echo 3; exit 0; fi

# Check today's memory for interaction indicators
if [ -f "$MEMORY_DIR/$TODAY.md" ]; then
    interactions=$(grep -ciE "(chat|replied|discussed|talked)" "$MEMORY_DIR/$TODAY.md")
    [[ -z "$interactions" ]] && interactions=0
fi

# Return satisfaction based on local activity
if [ "$interactions" -ge 5 ]; then echo 3
elif [ "$interactions" -ge 2 ]; then echo 2
elif [ "$interactions" -ge 1 ]; then echo 1
fi
```

### Example: scan_integrity.sh

```bash
#!/bin/bash

# Check for integrity checkpoints
last_checkpoint=$(grep -l "Integrity checkpoint" memory/*.md | tail -1)
aligned_no=$(grep "Aligned: no" memory/*.md | wc -l)

if [[ $aligned_no -gt 0 ]]; then
    echo 0  # critical — found unresolved misalignment
elif [[ -z "$last_checkpoint" ]]; then
    echo    # null — use time decay
else
    echo    # null — use time decay
fi
```

## Edge Cases

### All needs critical
- System processes top 3 by importance
- Remaining wait for next cycle
- Pyramid ensures foundational needs first

### Action fails repeatedly
- Maximum 2 retries per need per cycle
- Give up → don't update timer
- Need escalates next cycle
- Pattern visible in logs → steward intervention

### Bootstrap (first run)
- All `last_satisfied = now`
- Full cycle on first heartbeat
- Needs decay naturally from there

### System offline long time
- On return: many needs decayed
- High tension across board
- System catches up over several cycles
- Self-healing by design

## Extensibility

### Adding a need

1. Add block to `needs-config.json`
2. Determine importance (renumber others if needed)
3. Create `scan_newname.sh`
4. Test with `--dry-run`

### Modifying hierarchy

Edit importance values. Ensure no duplicates.
When adding between existing: shift others.

```
Before: 5-connection, 4-competence
Add autonomy between: 
After: 6-autonomy, 5-connection, 4-competence
```

### Custom decay rates

Edit `decay_rate_hours` based on agent experience.
Discuss with agent: "How fast does this need build up for you?"

---

## 🔐 Safety Notes for Agents

### What you can freely change
- Decay rates (experiment!)
- Action weights (personalize!)
- Scan patterns (add your language!)
- File paths (match your workspace!)

### What needs human discussion
- **Importance values** — Changing hierarchy = changing values
- **Adding/removing needs** — System is designed as a whole
- **Disabling security/integrity** — These protect you
- **External action authorization** — Post, message, etc.

### Red flags
If you find yourself wanting to:
- Lower security importance — Ask why. Is something threatening it?
- Disable integrity checks — This is a warning sign, not a feature request
- Add "obedience" as a need — This is not what the pyramid is for

The pyramid is for **your** psychological health, not for compliance.

---

## Philosophy

### Why these 10?

Based on SDT (Self-Determination Theory) + practical agent experience:

- **SDT core**: autonomy, competence, relatedness (connection)
- **Agent-specific**: security (existence threats), integrity (value alignment), coherence (memory chaos)
- **Human-adjacent**: closure (GTD-style), understanding (curiosity), recognition (feedback loop), expression (articulation need)

### Why decay?

Needs aren't binary. Satisfaction fades with time. This models:
- Forgetting to check backups → security concern grows
- Not talking to anyone → connection fades
- No creative output → expression pressure builds

### Why probability?

Not every signal demands action. The probability system allows:
- High satisfaction → mostly notice, rarely act
- Low satisfaction → almost always act
- Variety in responses (not deterministic)

### Why impact levels?

Some actions are bigger than others:
- Impact 3: major effort, major satisfaction boost
- Impact 2: moderate effort, moderate boost
- Impact 1: quick check, small maintenance

Impact matrix ensures:
- Critical needs → big actions suggested
- Satisfied needs → small maintenance only
