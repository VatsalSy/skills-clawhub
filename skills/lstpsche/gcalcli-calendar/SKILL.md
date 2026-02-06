---
name: gcalcli-calendar
description: "Google Calendar skill for gcalcli: fast agenda (today/week/range), bounded keyword search, and safe event actions."
metadata: {"openclaw":{"emoji":"📅","requires":{"bins":["gcalcli"]}}}
---

# gcalcli-calendar

Use `gcalcli` to read/search/manage Google Calendar from the command line: agenda, search, quick add/add, edit, delete.

## Hard rules (must follow)

### 1) Calendar scope: default/ignore calendars are authoritative
`gcalcli` supports `config.toml` with:
- `default-calendars` (what to search/list by default)
- `ignore-calendars` (what to exclude, e.g. holidays)

Assume users have configured these. Do not “search everything including noise” if ignore-calendars exists.

If results look unexpectedly empty or user asks “across all calendars”, list calendars first and then retry with explicit `--calendar` filters.

### 2) Always use an explicit time window for search
Default search window (unless user specifies otherwise):
- **next 6 months** (≈ 180 days) from “today”.

If no matches:
- Say explicitly: “No matches found in the next ~6 months (<from> → <to>). Want me to search further (e.g., 12 months) or around a date?”

### 3) Token-efficient output
Prefer minimal, parseable output:
- Add `--nocolor` to reduce noisy formatting (useful for agents / logs)
- Use default output for simple summarization.
- Use `--tsv` only if you must reliably parse/dedupe/sort in post-processing.

### 4) No invented explanations
If nothing is found, do not guess why. State what you searched (window + calendar scope) and propose the smallest next step.

### 5) Writes require confirmation
Before `quick/add/edit/delete`:
- Summarize the exact change (calendar, title, date/time, duration, location, attendees if any).
- Ask for explicit “yes” before running the command.

## Canonical commands

### List calendars (when scope needs verification)
- `gcalcli list`

### Agenda (what’s on my calendar…)
Agenda defaults: start = today 00:00, end = start + 5 days

- Today (tight window):
  - `gcalcli --nocolor agenda today tomorrow`
- Next 7 days:
  - `gcalcli --nocolor agenda today +7d`
- Custom range:
  - `gcalcli --nocolor agenda <start> <end>`

(If unsure about date literal formats supported in the environment, consult `gcalcli --help` / `gcalcli agenda --help`.)

### Keyword search (bounded)
Search is case-insensitive and matches terms across fields

- Default (next ~6 months):
  - `gcalcli --nocolor search "<query>" today +180d`
- If user asked a specific period:
  - `gcalcli --nocolor search "<query>" <start> <end>`

If the user wants “next occurrence”:
- Run bounded search; return the earliest upcoming match.

If the user wants “all matches”:
- Return all matches within the window (sorted by start time).

### Week/month views
- `gcalcli --nocolor calw <weeks> [start]`
- `gcalcli --nocolor calm [start]`

### Create event (confirm first)
Quick add (requires a single calendar selected)
- `gcalcli --nocolor --calendar "<CalendarName>" quick "<natural language event text>"`

Detailed add (requires a single calendar selected)
- `gcalcli --nocolor --calendar "<CalendarName>" --title "<Title>" --where "<Location>" --when "<Start>" --duration <minutes> --description "<Text>" add`

### Edit / delete (confirm first)
- `gcalcli --nocolor --calendar "<CalendarName>" edit`
- `gcalcli --nocolor --calendar "<CalendarName>" delete`

## How the agent should respond

When answering calendar questions, include:
1) The answer (events / next occurrence), concise.
2) The **scope** used:
   - searched/listed window: `<from> → <to>`
   - calendar scope: “default calendars” (from config) and any “ignored calendars” (from config)

If no results:
- “No matches found in <from> → <to> (default calendars; ignored: …). Want me to expand the window or search around a specific date?”
