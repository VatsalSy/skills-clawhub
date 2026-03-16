---
name: context-hub-openclaw
description: Use Context Hub (chub) to fetch versioned API docs/skills before coding, then persist learnings with annotations.
homepage: https://github.com/andrewyng/context-hub
metadata: {"clawdbot":{"emoji":"🧠","requires":{"bins":["chub"]},"install":[{"id":"node","kind":"node","package":"@aisuite/chub","bins":["chub"],"label":"Install Context Hub CLI (npm)"}]}}
---

# Context Hub for OpenClaw

Use this skill whenever implementation depends on third-party APIs/SDKs or fast-changing tools.

## When to use

Trigger this skill when the user asks to:
- integrate with OpenAI/Anthropic/Stripe/etc.
- write SDK/API code where versions matter
- debug integration failures likely caused by doc drift
- create reusable internal implementation playbooks

Do **not** rely only on memorized API shapes. Fetch current docs first.

## Core workflow (doc-first coding)

1) Search candidates

```bash
chub search "<vendor api or sdk>" --json
```

2) Fetch the best match (pin language/version when available)

```bash
chub get <id> --lang js --json
# or
chub get <id> --lang py --version <sdk-version> --json
```

3) Pull only needed references to reduce token noise

```bash
chub get <id> --file references/errors.md
# or
chub get <id> --full
```

4) Implement against fetched docs, not assumptions.

5) Persist new learnings (only non-obvious, high-value findings)

```bash
chub annotate <id> "<gotcha + fix + context>"
```

6) Optional quality feedback (ask user before sending)

```bash
chub feedback <id> up
chub feedback <id> down --label outdated --label wrong-examples
```

## Annotation quality standard

Good annotation format:
- **Symptom:** what broke
- **Cause:** why docs/code failed in practice
- **Fix:** exact change that worked
- **Scope:** version/environment constraints

Example:

```bash
chub annotate stripe/api "Webhook signature failed in Next.js route handlers; use raw request body before JSON parse. Verified on stripe-node 17.x."
```

Avoid annotations that just restate obvious doc text.

## OpenClaw integration pattern

- Treat Context Hub as first source for coding accuracy.
- Save references to project files when useful:

```bash
mkdir -p .context
chub get <id> --lang js -o .context/<id>.md
```

- For repeated workflows, maintain a compact project playbook (e.g., `shared/<project>/context-notes.md`) and keep chub annotations concise.

## Useful commands

```bash
chub update
chub cache status
chub search "stripe webhooks"
chub get stripe/api --lang js
chub annotate --list --json
chub feedback --status
```

## Safety + ops notes

- Prefer `--json` for machine parsing in agent flows.
- Keep annotation volume low and signal high.
- If docs conflict with runtime behavior, annotate locally and continue with verified behavior.
- Use version targeting (`--version`) when package major versions differ.
