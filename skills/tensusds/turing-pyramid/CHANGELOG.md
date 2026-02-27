# Changelog

## v1.10.1 (2026-02-25)
- **fix:** STATE_FILE path bug (`.needs.$need` → `.$need`)
- **docs:** Clean SKILL.md with ASCII tables

## v1.10.0 (2026-02-25)
- Test infrastructure (6 tests: unit, integration, regression)
- Homeostasis stability test

## v1.9.0 (2026-02-25)
- Autonomous Dashboard system
- Personal intentions tracking

## v1.8.0 (2026-02-24)
- VALUES.md integration
- Boundary logging system

## v1.7.1 (2026-02-25)
Balance fixes after stress testing:
- connection decay: 4h → 6h
- closure decay: 8h → 12h  
- security → autonomy deprivation: -0.30 → -0.20

## v1.7.0 (2026-02-25)
- **Cross-need impact system** — needs influence each other
- on_action: satisfying one need boosts related needs
- on_deprivation: deprived needs drag down related needs
- 22 cross-need connections
- Float satisfaction (0.00-3.00)
- Protection: floor=0.5, ceiling=3.0, cooldown=4h

## v1.6.0 (2026-02-24)
- Float impacts (0.0-3.0)
- Impact ranges: low/mid/high
- Weighted action selection

## v1.5.3 (2026-02-24)
- Dynamic max_tension from config

## v1.5.0 (2026-02-24)
- Tension bonus to action probability
- Formula: `final_chance = base + (tension × 50 / max_tension)`

## v1.4.3
- Complete 10-need system
- Decay mechanics
- Impact matrix
