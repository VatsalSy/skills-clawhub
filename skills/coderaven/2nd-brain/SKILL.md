---
name: brain
version: 1.2.1
description: |
  Personal knowledge base for capturing and retrieving information about people,
  places, restaurants, games, tech, events, media, ideas, and organizations.
  Use when: user mentions a person, place, restaurant, landmark, game, device,
  event, book/show, idea, or company. Trigger phrases: "remember", "note that",
  "met this person", "visited", "played", "what do I know about", etc.
  Brain entries take precedence over daily logs for named entities.
---

# Brain Skill — 2nd Brain Knowledge Base

A personal knowledge management system for capturing and retrieving information about people, places, things, and ideas.

## When to Use This Skill

**Brain takes precedence over daily logs for named entities.**

Trigger this skill when:
- User asks you to remember someone, something, or somewhere
- User shares information about a person, place, game, tech, event, media, idea, or organization
- User expresses a preference about an entity ("I like X at Y restaurant" → update Y's file)
- User asks about something that might be in the brain ("Who was that guy from...", "What did I think about...")
- User updates existing knowledge ("Actually, he's 27 now", "I finished that game")

**Keywords that trigger:** "remember", "note that", "met this person", "visited", "played", "watched", "read", "idea:", "what do I know about", "who is", "where was"

**⚠️ Do NOT put brain-eligible content in daily logs.** If it's a named entity (person, place, restaurant, product, game, etc.), it belongs in `brain/`, not `memory/YYYY-MM-DD.md`. Daily logs are for session context and ephemeral notes only.

**🚨 MEDIA FILES MUST BE SAVED.** When user sends photos/audio/video/PDFs about a brain entry, you MUST save the actual file to `attachments/`. Transcribing content is NOT the same as saving the file. Do BOTH.

## Data Location

All brain data lives in: `~/.openclaw/workspace/brain/`

```
brain/
  people/       # Contacts, people you've met
  places/       # Restaurants, landmarks, venues
  games/        # Video games and interactions
  tech/         # Devices, products, specs, gotchas
  events/       # Conferences, meetups, gatherings
  media/        # Books, shows, films, podcasts
  ideas/        # Business ideas, concepts, thoughts
  orgs/         # Companies, communities, groups
```

## File Naming Convention

- Slugified lowercase: `raven-duran.md`, `house-of-lechon-cebu.md`
- For disambiguation: `john-smith-symph.md` vs `john-smith-ateneo.md`
- Always propose disambiguator to user before creating if name clash is possible

## Operational Rules

### Creating a New Entry

1. **Search first** — Run `qmd search "<name or topic>"` to check for existing entries
2. **No match** — Create new file using the appropriate template from `skills/brain/templates/`
3. **Possible clash** — List all potential matches and ask user to confirm before creating

### Updating an Existing Entry

1. **Find the file** — Use `qmd search` or direct path if known
2. **Surgical edit** — Update only the relevant section, don't rewrite the whole file
3. **Log the date** — Add timestamp to Notes or Interactions section
4. **Update frontmatter** — Bump `last_updated` field

### Searching / Retrieving

1. **Query QMD** — `qmd query "<natural language question>"` for semantic search
2. **Ambiguous results** — Surface all candidates to user, ask which one
3. **No results** — Tell user nothing found, offer to create entry

## Disambiguation Protocol

When user references something ambiguous (e.g., "John"):

1. Search brain for all matches
2. If multiple results: list them with context
   ```
   Found 2 matches for "John":
   1. John Smith (Symph colleague, met 2024)
   2. John Doe (GeeksOnABeach speaker, met 2026)
   Which one?
   ```
3. Wait for confirmation before updating

## Templates

Templates live in `skills/brain/templates/`. Each has:
- YAML frontmatter with structured fields
- Markdown body with standard sections

When creating a new entry:
1. Read the appropriate template
2. Fill in known fields
3. Leave unknown fields empty or with placeholder
4. Write to `brain/<category>/<slug>.md`

## Categories Reference

| Category | Folder | Use For |
|----------|--------|---------|
| People | `brain/people/` | Anyone user has met or wants to remember |
| Places | `brain/places/` | Restaurants, landmarks, venues, locations |
| Games | `brain/games/` | Video games — status, opinions, notes |
| Tech | `brain/tech/` | Devices, products, specs, quirks |
| Events | `brain/events/` | Conferences, meetups, gatherings |
| Media | `brain/media/` | Books, shows, films, podcasts |
| Ideas | `brain/ideas/` | Business ideas, concepts, random thoughts |
| Orgs | `brain/orgs/` | Companies, communities, groups |

## Linking Entities

Use wikilink-style references to connect entities:
- `[[people/raven-duran]]` — link to a person
- `[[events/geeksonabeach-2026]]` — link to an event
- `[[orgs/symph]]` — link to an org

This makes relationships explicit and searchable.

## Example Workflow

**User says:** "Hey, I just met this guy called Raven Duran. He's positioning himself as an Agentic coder, met him at GeeksOnABeach PH last February."

**Agent does:**
1. `qmd search "Raven Duran"` → no results
2. Read `skills/brain/templates/person.md`
3. Create `brain/people/raven-duran.md` with filled template
4. Optionally check/create `brain/events/geeksonabeach-ph-2026.md` and link

**User says:** "The Raven Duran guy, he's still 26 years old"

**Agent does:**
1. `qmd search "Raven Duran"` → finds `brain/people/raven-duran.md`
2. Read file, update `age: 26` in frontmatter
3. Add note: `- **2026-02-21**: Confirmed still 26 years old`
4. Update `last_updated` field

## Attachments

Brain entries can have attachments: photos, PDFs, videos, audio, transcripts, etc.

### 🚨 MANDATORY: Save All Media Files

**When user sends ANY media (photos, audio, video, PDF) related to a brain entry:**

1. **ALWAYS save the actual file** to `attachments/` — this is NON-NEGOTIABLE
2. THEN analyze/transcribe the content into the profile
3. NEVER skip saving the file just because you processed its content

**"Saved" means the FILE exists in `attachments/`, not just that content was transcribed.**

```bash
# REQUIRED: Copy the file
cp /path/to/inbound/media.jpg brain/places/entry/attachments/descriptive-name.jpg
```

If you transcribed content but didn't save the file → YOU DID IT WRONG. Go back and save it.

### Structure

**Flat file (no attachments):**
```
brain/places/manam.md
```

**Folder structure (with attachments):**
```
brain/places/mamou-prime-sm-podium/
  mamou-prime-sm-podium.md      # Profile (keeps original name)
  attachments/
    index.md                    # Describes each attachment
    menu-page-1.jpg
    menu-page-2.jpg
    receipt.pdf
    storefront.mp4
```

### Attachments Index (`attachments/index.md`)

```markdown
# Attachments

| File | Description | Added |
|------|-------------|-------|
| menu-page-1.jpg | Menu first page, mains section | 2026-02-21 |
| menu-page-2.jpg | Menu second page, desserts | 2026-02-21 |
| receipt.pdf | Receipt from Feb visit, ₱2,400 | 2026-02-21 |
| storefront.mp4 | Quick video of the entrance | 2026-02-21 |
```

QMD indexes this file, making attachments searchable by description.

### Adding Attachments

When user sends media about an entity (e.g., "Here's the menu for Mamou Prime"):

1. **Find the entry** — `qmd search "Mamou Prime"` → `brain/places/mamou-prime-sm-podium.md`

2. **Convert to folder structure (if flat file):**
   ```bash
   # Create folder
   mkdir -p brain/places/mamou-prime-sm-podium/attachments
   # Move profile into folder
   mv brain/places/mamou-prime-sm-podium.md brain/places/mamou-prime-sm-podium/
   # Create attachments index
   touch brain/places/mamou-prime-sm-podium/attachments/index.md
   ```

3. **Save media** to `attachments/` with descriptive filename

4. **Update `attachments/index.md`** with file description

### ⚠️ Always Save Original Files

**Do BOTH:**
1. **Analyze/transcribe** the content → add processed text to the profile (e.g., menu tables, business card info, transcript)
2. **Save the original files** → preserve in `attachments/`

The text is searchable and processable. The originals are preserved artifacts.

**Never discard attachments** unless user explicitly says "cleanup", "remove", or "delete" the files.

**Example:** User sends menu photos
- ✅ Transcribe menu into markdown tables in profile
- ✅ Save original photos to `attachments/menu-1.jpg`, `menu-2.jpg`
- ✅ Update `attachments/index.md`

**Wrong:** Only transcribing without saving originals

### Naming Attachments

Be descriptive — the index provides context:
- `menu-1.jpg`, `menu-2.jpg`
- `business-card.jpg`
- `product-demo.mp4`
- `meeting-transcript.md`
- `voice-memo-2026-02-21.mp3`

### Example: Adding Menu Photos

**User sends:** 2 photos with message "Menu at Mamou Prime"

**Agent does:**
1. Find `brain/places/mamou-prime-sm-podium.md`
2. Convert to folder structure (if needed)
3. **Analyze photos** → transcribe menu items, prices into markdown tables
4. **Update profile** with transcribed menu section
5. **Save original photos** as `attachments/menu-1.jpg`, `attachments/menu-2.jpg`
6. Update `attachments/index.md`:
   ```markdown
   # Attachments

   | File | Description | Added |
   |------|-------------|-------|
   | menu-1.jpg | Menu page 1 (transcribed to profile) | 2026-02-21 |
   | menu-2.jpg | Menu page 2 (transcribed to profile) | 2026-02-21 |
   ```
7. Confirm to user: "Transcribed menu and saved 2 photos to Mamou Prime"
