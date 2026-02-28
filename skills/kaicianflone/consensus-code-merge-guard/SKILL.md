---
name: consensus-code-merge-guard
description: Persona-weighted merge governance for AI-assisted engineering. Evaluates PR risk (tests, security markers, reliability signals), returns MERGE/BLOCK/REVISE decisions, and records board-native audit artifacts.
homepage: https://github.com/kaicianflone/consensus-code-merge-guard
source: https://github.com/kaicianflone/consensus-code-merge-guard
metadata:
  {"openclaw": {"requires": {"bins": ["node", "tsx"]}}}
---

# consensus-code-merge-guard

`consensus-code-merge-guard` turns code merge approval into a governed, auditable decision.

## What this skill does

- consumes PR/change summary input
- runs persona-weighted vote arbitration
- enforces hard constraints (e.g., tests/security flags)
- maps to engineering decision states: `MERGE | BLOCK | REVISE`
- writes decision and updated persona artifacts to board state

## Why this matters

CI passing does not guarantee risk-aware merge quality. Consensus review reduces silent failure propagation into production.

## Ecosystem role

Uses the same consensus substrate as other guards, enabling cross-domain governance with comparable metrics.

## Useful for

- autonomous or semi-autonomous merge pipelines
- high-risk repos needing policy checks
- repeatable release governance with artifact history


## Runtime, credentials, and network behavior

- runtime binaries: `node`, `tsx`
- network calls: none in the guard decision path itself
- conditional network behavior: if a run needs persona generation and your persona-generator backend uses an external LLM, that backend may perform outbound API calls
- credentials: `OPENAI_API_KEY` (or equivalent provider key) may be required **only** for persona generation in LLM-backed setups; if `persona_set_id` is provided, guards can run without LLM credentials
- filesystem writes: board/state artifacts under the configured consensus state path

## Dependency trust model

- `consensus-guard-core` and `consensus-persona-generator` are first-party consensus packages
- versions are semver-pinned in `package.json` for reproducible installs
- this skill does not request host-wide privileges and does not mutate other skills

## Quick start

```bash
node --import tsx run.js --input ./examples/input.json
```

## Tool-call integration

This skill is wired to the consensus-interact contract boundary (via shared consensus-guard-core wrappers where applicable):
- readBoardPolicy
- getLatestPersonaSet / getPersonaSet
- writeArtifact / writeDecision
- idempotent decision lookup

This keeps board orchestration standardized across skills.

## Invoke Contract

This skill exposes a canonical entrypoint:

- `invoke(input, opts?) -> Promise<OutputJson | ErrorJson>`

`invoke()` starts the guard flow, which then executes persona evaluation and consensus-interact-contract board operations (via shared guard-core wrappers where applicable).

## external_agent mode

Guards support two modes:
- `mode="persona"` (default): guard loads/generates persona_set and runs internal persona voting.
- `mode="external_agent"`: caller supplies `external_votes[]` from real agents; guard performs deterministic aggregation, policy checks, and board decision writes without requiring persona harness.
