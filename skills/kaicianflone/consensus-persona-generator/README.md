# consensus-persona-generator

Generate and persist reusable `persona_set` artifacts on a consensus-tools local JSON board.

## 60-second quickstart

```bash
cd repos/persona-generator
npm i
node --import tsx run.js --input ./examples/persona-input.json
```

Output JSON is written to `./out` and printed as a summary.

## Input contract

See `examples/persona-input.json`.

## Output contract

Strict JSON object:
- `board_id`
- `persona_set_id`
- `created_at`
- `personas[]`
- `board_write`

Error output:
- `board_id`
- `error { code, message, details }`

## Notes

- Board persistence is job/submission-based (`artifact:persona_set`) over the consensus-tools local JSON state.
- Deterministic generation path is used by default for demoability.
- Strict input schema validation is enforced (unknown fields are rejected).
- Artifact indexing helpers are included (in-memory index built from board state, then O(1) lookups for latest/by-id access).
