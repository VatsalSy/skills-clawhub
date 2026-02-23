# feed-to-md Skill

This skill converts RSS/Atom feed URLs into Markdown using `feed2md`.

## Files

- `SKILL.md`: skill definition and usage instructions
- `scripts/feed-to-markdown.sh`: wrapper script to run the CLI directly or via `npx`

## Requirements

- `feed2md` installed globally, or
- `npx` available from Node.js

## Install CLI

```bash
npm install -g feed2md-cli
```

## Usage

Direct CLI:

```bash
feed2md "https://example.com/feed.xml"
```

Wrapper script:

```bash
./scripts/feed-to-markdown.sh "https://example.com/feed.xml"
./scripts/feed-to-markdown.sh "https://example.com/feed.xml" output.md
```
