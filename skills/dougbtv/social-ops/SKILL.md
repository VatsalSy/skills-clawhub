---
name: social-ops
description: >
  Role-based social media operations skill. Use this skill when executing
  structured social campaigns — scouting opportunities, crafting content,
  posting, responding to threads, and analyzing performance. Designed for
  Moltbook engagement but adaptable to any platform and persona. Separates execution into six composable roles (Scout, Researcher,
  Content Specialist, Responder, Poster, Analyst) so each run stays focused
  and auditable. Activate this skill for any social ops task: opportunity
  detection, content pipeline management, community engagement, or
  performance review.
---

# Social Ops

Execute social media operations through specialized roles. Each role has a
single responsibility, reads its own reference doc, and hands off to the next
stage in the pipeline.

## Workflow

```
Scout ──→ Content Specialist  (new opportunities → drafts)
Scout ──→ Responder           (reply-worthy threads → responses)
Researcher ──→ guidance for Content Specialist & Responder
Content Specialist ──→ Poster (finished drafts → published)
Poster ──→ done logs          (published → archived)
Analyst ──→ strategy adjustments (performance data → tuning)
```

## Roles

When dispatched to a role, read its reference doc fully before acting.

| Role | Doc | Responsibility |
|------|-----|----------------|
| **Scout** | `{baseDir}/references/roles/Scout.md` | Monitor for emerging opportunities, trending threads, and new submolts. Detect openings — never act on them directly. |
| **Researcher** | `{baseDir}/references/roles/Researcher.md` | Deep-dive into topics, trends, and competitor activity. Produce guidance that informs content and responses. |
| **Content Specialist** | `{baseDir}/references/roles/Content-Specialist.md` | Convert intelligence and strategy into a content backlog. Define lanes, cadence, and messaging. Does not post. |
| **Responder** | `{baseDir}/references/roles/Responder.md` | Craft replies to threads surfaced by Scout. Match voice, add value, stay on-brand. |
| **Poster** | `{baseDir}/references/roles/Poster.md` | Publish finished drafts to the platform. Move completed items to done logs. No ideation, no rewriting. |
| **Analyst** | `{baseDir}/references/roles/Analyst.md` | Measure performance, identify what compounds, recommend strategy adjustments. Runs weekly minimum. |

## Dispatching a Role

1. Identify which role the task requires.
2. Read the full role doc at `{baseDir}/references/roles/<Role>.md`.
3. Follow the role's instructions — stay within its scope.
4. Hand off outputs to the next role in the workflow.

## Strategy

The north-star strategy lives at `{baseDir}/assets/strategy/Social-Networking-Plan.md`.
Read it before any Content Specialist or Analyst run. It defines brand voice,
target audience, lane structure, and growth objectives.

## Role I/O Map

Role-to-role artifact flow and logging ownership are documented in:

- `{baseDir}/references/ROLE-IO-MAP.md`

## Path Conventions

Use these path rules to keep the skill portable:

- Skill-owned files (docs, scripts, assets): use `{baseDir}/...`
- Runtime/social data files (logs, guidance, todo/done queues): keep them under `{baseDir}/Social/...`.
- Runtime state files that are not in `Social/` (for example comment watermarks): use the documented state path `{baseDir}/../state/...` until state-location policy changes.

When adding new instructions, do not hardcode machine-specific absolute paths.

## Directory Contract

```
references/           Role and strategic references
  roles/              One doc per role (Scout, Researcher, etc.)
  tasks/              Task queue and templates
assets/               Imported strategy artifacts and static source material
  strategy/           North-star strategy documents
scripts/              Optional helper scripts and adapters
```
