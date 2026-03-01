---
name: consensus-deployment-guard
description: Pre-deployment governance for release and infrastructure rollout requests. Use when an agent or workflow proposes shipping code/config/infrastructure changes to staging or production and you need deterministic ALLOW/BLOCK/REQUIRE_REWRITE decisions with strict schema validation, idempotency, and board-native audit artifacts.
---

# consensus-deployment-guard

`consensus-deployment-guard` is the final safety gate before deployment execution.

## What this skill does

- validates deployment requests against a strict JSON schema (reject unknown fields)
- evaluates hard-block and rewrite policy flags for release risk patterns
- runs persona-weighted voting (or aggregates external votes)
- returns one of: `ALLOW | BLOCK | REQUIRE_REWRITE`
- writes decision and persona update artifacts for replay/audit

## Decision policy shape

Hard-block examples:
- required tests not passing
- CI status failed
- rollback artifact missing when required
- incompatible schema migration
- error budget already breached

Rewrite examples:
- production rollout not using canary when policy requires it
- initial rollout percentage above policy limit
- production deploy missing explicit human confirmation gate
- CI still pending
- schema compatibility unknown

## Runtime and safety model

- runtime binaries: `node`, `tsx`
- credentials: none required for local deterministic decision path
- network behavior: guard logic is local; persona generation backend may use external LLMs depending on deployment
- filesystem writes: consensus board/state artifacts under configured state path

## Invoke contract

- `invoke(input, opts?) -> Promise<OutputJson | ErrorJson>`

Modes:
- `mode="persona"` (default): load/generate persona_set and vote internally
- `mode="external_agent"`: consume `external_votes[]`, aggregate deterministically, and enforce policy

## Quick start

```bash
node --import tsx run.js --input ./examples/input.json
```

## Tests

```bash
npm test
```

Coverage includes schema rejection, hard-block paths, rewrite paths, allow paths, idempotent retries, and external-agent aggregation behavior.
