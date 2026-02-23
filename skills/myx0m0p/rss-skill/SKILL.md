---
name: feed-to-md
title: feed-to-md
description: Convert RSS or Atom feed URLs into Markdown using feed2md. Use this when a user asks to turn a feed URL into readable Markdown, optionally limiting items or writing to a file.
---

# RSS/Atom to Markdown

Use this skill when the task is to convert an RSS/Atom feed URL into Markdown.

## What this skill does

- Converts a feed URL to Markdown via `feed2md`
- Supports stdout output or writing to a Markdown file
- Supports limiting article count and summary controls

## Inputs

- Required: RSS/Atom URL
- Optional:
  - output path
  - max item count
  - template preset (`short` or `full`)
  - custom template file
  - summary options

## Command workflow

1. Prefer direct CLI if installed:

```bash
feed2md "<feed_url>"
```

2. If CLI is not installed globally, run with `npx`:

```bash
npx -y feed2md-cli "<feed_url>"
```

3. For repeatable execution, use this skill's wrapper script:

```bash
./scripts/feed-to-markdown.sh "<feed_url>" [output_file]
```

## Common examples

Basic conversion:

```bash
feed2md "https://example.com/feed.xml"
```

Write to file:

```bash
feed2md "https://example.com/feed.xml" --output feed.md
```

Limit to 10 items with full template:

```bash
feed2md "https://example.com/feed.xml" --limit 10 --template full
```

Skip summaries:

```bash
feed2md "https://example.com/feed.xml" --no-summary
```

Use custom template:

```bash
feed2md "https://example.com/feed.xml" --template-file ./template.eta
```

## CLI options

- `-o, --output <file>`: write markdown to file
- `--limit <number>`: max number of articles
- `--no-summary`: exclude summaries
- `--summary-max-length <number>`: truncate summary length
- `--template <preset>`: `short` (default) or `full`
- `--template-file <path>`: custom Eta template

## Error handling

- If `feed2md` is missing, install/use via:

```bash
npm install -g feed2md-cli
# or
npx -y feed2md-cli "<feed_url>"
```

- If URL fetch fails, verify URL is publicly reachable and points to RSS/Atom XML.
