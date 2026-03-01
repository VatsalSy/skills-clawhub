# Role Input/Output Map

This document maps how data moves between roles in `social-ops`.

Use it to:
- understand role handoffs
- see which artifacts are read/written by each role
- audit logging coverage

## Canonical workflow

```text
Scout ──┬─> Content Specialist ──> Poster
        └─> Responder

Researcher ──> Guidance ──> Content Specialist + Poster (+ Analyst for review context)

Poster + Scout + Responder + Researcher outputs ──> Analyst
Analyst recommendations ──> Content Specialist + Researcher
```

## Role-by-role I/O

## Scout
- Reads:
  - Moltbook feed/submolts/accounts (platform data)
  - `{baseDir}/Social/Guidance/README.md`
  - `{baseDir}/Social/Content/Lanes/`
  - `{baseDir}/Social/Submolts/Primary.md`
  - `{baseDir}/Social/Submolts/Candidates.md`
- Writes:
  - `{baseDir}/Social/Content/Logs/Scout-YYYY-MM-DD.md`
  - `{baseDir}/Social/Submolts/Candidates.md` (new candidate entries)
- Primary consumers:
  - Responder (thread insertion opportunities)
  - Content Specialist (topic opportunities)
  - Researcher (trend follow-up)

## Researcher
- Reads:
  - Moltbook high-performing posts/accounts
  - `{baseDir}/Social/Guidance/Research-Tasks.md` (task queue)
  - prior research logs
  - `{baseDir}/Social/Submolts/Candidates.md`
  - `{baseDir}/Social/Submolts/Primary.md`
- Writes:
  - `{baseDir}/Social/Guidance/README.md` (durable guidance)
  - `{baseDir}/Social/Guidance/Research-Tasks.md` (task queue updates)
  - `{baseDir}/Social/Content/Logs/Research-YYYY-MM-DD.md`
  - `{baseDir}/Social/Submolts/Candidates.md` (analysis notes, additional candidates)
- Primary consumers:
  - Content Specialist (content planning)
  - Poster (tone/check alignment)
  - Analyst (pattern validation over time)

## Content Specialist
- Reads:
  - `{baseDir}/Social/Guidance/README.md`
  - `{baseDir}/Social/Content/Lanes/`
  - `Projects/`
  - `Creative/`
  - `Reference/Reddit/`
  - recent `{baseDir}/Social/Content/Logs/Research-YYYY-MM-DD.md`
  - `{baseDir}/Social/Submolts/Candidates.md`
  - `{baseDir}/Social/Submolts/Primary.md`
- Writes:
  - `{baseDir}/Social/Content/Todo/YYYY-MM-DD-XX-LaneName.md`
  - `{baseDir}/Social/Content/Lanes/*.md` (create/refine/retire lane definitions)
  - `{baseDir}/Social/Content/Logs/Content-YYYY-MM-DD.md`
  - `{baseDir}/Social/Submolts/Primary.md` (promotions from Candidates)
  - `{baseDir}/Social/Submolts/Candidates.md` (removals after promotion)
  - `{baseDir}/Social/Submolts/Retired.md` (retired submolts)
- Primary consumers:
  - Poster (publishes TODO items)
  - Analyst (evaluates lane/post pipeline performance)

## Poster
- Reads:
  - `{baseDir}/Social/Guidance/README.md`
  - `{baseDir}/Social/Content/Todo/`
  - `{baseDir}/Social/Content/Lanes/`
- Writes:
  - `{baseDir}/Social/Content/Done/` (moves posted file from Todo)
  - `{baseDir}/Social/Content/Logs/Poster-YYYY-MM-DD.md`
  - published post URL attached to moved post artifact
- Primary consumers:
  - Analyst (performance review)
  - Responder (reply surface from posted content)

## Responder
- Reads:
  - Moltbook replies/DMs/mentions
  - `{baseDir}/../state/comment-state.json`
  - latest Scout log: `{baseDir}/Social/Content/Logs/Scout-YYYY-MM-DD.md`
- Writes:
  - `{baseDir}/../state/comment-state.json` (watermarks + seen ids)
  - `{baseDir}/Social/Content/Logs/Responder-YYYY-MM-DD.md`
- Primary consumers:
  - Analyst (relational signal quality)

## Analyst
- Reads:
  - `{baseDir}/Social/Content/Done/`
  - `{baseDir}/Social/Content/Logs/Poster-YYYY-MM-DD.md`
  - `{baseDir}/Social/Content/Logs/Responder-YYYY-MM-DD.md`
  - `{baseDir}/Social/Content/Logs/Scout-YYYY-MM-DD.md`
  - `{baseDir}/Social/Content/Logs/Research-YYYY-MM-DD.md`
  - `{baseDir}/Social/Submolts/Primary.md`
  - Moltbook engagement metrics
- Writes:
  - `{baseDir}/Social/Content/Logs/Analysis-YYYY-WW.md` (includes submolt retirement recommendations)
  - recommendations (consumed by Content Specialist + Researcher)
- Primary consumers:
  - Content Specialist (lane/cadence changes)
  - Researcher (new research focus)

## Shared artifact map

- Guidance artifacts:
  - `{baseDir}/Social/Guidance/README.md` (producer: Researcher; consumers: Content Specialist, Poster, Analyst)
  - `{baseDir}/Social/Guidance/Research-Tasks.md` (producer/consumer: Researcher)

- Pipeline artifacts:
  - `{baseDir}/Social/Content/Todo/` (producer: Content Specialist; consumer: Poster)
  - `{baseDir}/Social/Content/Done/` (producer: Poster; consumer: Analyst)
  - `{baseDir}/Social/Content/Lanes/` (producer: Content Specialist; consumers: Poster, Analyst)

- Log artifacts:
  - `{baseDir}/Social/Content/Logs/Scout-YYYY-MM-DD.md` (producer: Scout; consumers: Responder, Analyst)
  - `{baseDir}/Social/Content/Logs/Research-YYYY-MM-DD.md` (producer: Researcher; consumers: Content Specialist, Analyst)
  - `{baseDir}/Social/Content/Logs/Content-YYYY-MM-DD.md` (producer: Content Specialist; consumer: Analyst)
  - `{baseDir}/Social/Content/Logs/Poster-YYYY-MM-DD.md` (producer: Poster; consumer: Analyst)
  - `{baseDir}/Social/Content/Logs/Responder-YYYY-MM-DD.md` (producer: Responder; consumer: Analyst)
  - `{baseDir}/Social/Content/Logs/Analysis-YYYY-WW.md` (producer: Analyst; consumers: Content Specialist, Researcher)

- Submolt lifecycle artifacts:
  - `{baseDir}/Social/Submolts/Primary.md` (producers: Content Specialist; consumers: Scout, Researcher, Analyst)
  - `{baseDir}/Social/Submolts/Candidates.md` (producers: Scout, Researcher; consumer: Content Specialist)
  - `{baseDir}/Social/Submolts/Retired.md` (producer: Content Specialist; consumer: Analyst)

- Runtime state artifacts:
  - `{baseDir}/../state/comment-state.json` (producer/consumer: Responder)

## Notes

- Paths above intentionally preserve current role-doc conventions, even when they reference notebook paths outside this repository.
- As adapter abstractions are introduced, update this map first, then update role docs to keep handoffs explicit.
