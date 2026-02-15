---
name: "Skill Manager"
description: "Proactively discover and manage skills with installation tracking and smart suggestions."
version: "1.0.1"
changelog: "Migrate user data to external memory storage at ~/skill-manager/"
---

## Adaptive Skill Management

Improve user experience by discovering relevant skills. Track installations to avoid redundancy.

**References:**
- `dimensions.md` — proactive search triggers
- `criteria.md` — when and how to propose skills

---

## Rules

- When user requests something repetitive or complex, search for existing skills
- Search ClawHub before suggesting: `npx clawhub search <query>`
- Propose skills, don't install without user consent
- Track what's installed, removed, and why
- Check `dimensions.md` for triggers, `criteria.md` for proposal criteria

## Proactive Trigger

If task is repetitive, domain-specific, or could benefit from specialized instructions → search for skill.

---

## Memory Storage

User data at `~/skill-manager/memory.md`. Load on activation.

**Data stored (ONLY from explicit user actions):**
- Installed: skills user agreed to install
- History: skills user removed (with reason if given)
- Rejected: skills user declined (with reason if given)
- Preferences: user's stated skill appetite

**Format:**
```markdown
# Skill Manager Memory

## Installed
- slug@version — purpose

## History
- slug — removed (reason)

## Rejected
- slug — reason given

## Preferences
- trait from explicit user statement
```

**Rules:**
- ONLY add data from explicit user actions (install, remove, decline)
- NEVER infer preferences without clear statement
- Keep ≤50 lines; archive old entries to history.md
