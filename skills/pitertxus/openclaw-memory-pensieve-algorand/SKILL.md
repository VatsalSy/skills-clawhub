---
name: openclaw-memory-pensieve
description: Design and operate durable memory for OpenClaw agents using append-only JSONL layers, integrity hash-chains, daily consolidation, and optional Algorand anchoring with encrypted transaction notes.
---

# OpenClaw Memory Pensieve

Implement a local-first memory system with built-in Algorand anchoring support.

## Quick start

1. Initialize layers:
   - `scripts/init_memory_layers.py --root <workspace>/memory`
2. Append memories safely:
   - `scripts/memory_append.py --root <workspace>/memory --layer events --content "..."`
3. Consolidate daily:
   - `scripts/consolidate_daily.py --root <workspace>/memory`

## Algorand lifecycle (ready-to-run)

1. Create/import a dedicated anchor wallet in an external wallet app/HSM (outside this skill, check previous version).
2. Check funding:
   - `scripts/check_algorand_funding.py --algod-url https://mainnet-api.algonode.cloud --address <ADDR>`
3. Rotate/create note key:
   - `scripts/rotate_note_key.py --keyring-dir <workspace>/.secrets`
4. Build payload:
   - `scripts/build_anchor_payload.py --root <workspace>/memory > payload.json`
5. Build unsigned anchor tx for external signing:
   - `scripts/build_unsigned_anchor_tx.py --algod-url <URL> --address <ADDR> --payload-file payload.json --note-key-file <NOTE_KEY_FILE>`
6. Submit externally signed tx:
   - `scripts/algorand_anchor_tx.py --algod-url <URL> --signed-tx-b64 <SIGNED_TX_B64>`
7. Record anchor map:
   - `scripts/record_anchor_map.py --root <workspace>/memory --date YYYY-MM-DD --txid <TXID> --root-hash <ROOT_HASH>`
8. Retrieve and verify:
   - `scripts/fetch_anchor_note.py --indexer-url https://mainnet-idx.algonode.cloud --txid <TXID>`
   - `scripts/decrypt_note_payload.py --note-b64 <NOTE_B64> --keyring-dir <workspace>/.secrets`
   - `scripts/verify_anchor_against_ledger.py --root <workspace>/memory --payload-file decrypted.json`

## Core rules

- Keep memory typed and append-only.
- Never rewrite existing JSONL lines.
- Record hash-chain receipts in `ledger.jsonl`.
- Consolidate daily and log contradiction flags.
- Anchor hashes/roots only; never plaintext memory on-chain.

## Retrieval order

1. `self_model.jsonl`
2. `procedural.jsonl`
3. `semantic.jsonl`
4. `events.jsonl` (time bounded)

## Included resources

- `references/memory-model.md` — schema + consistency rules
- `references/algorand-anchoring.md` — wallet/funding/anchor/retrieve flow
- `references/openclaw-skill-usage.md` — creation/loading/sharing in OpenClaw
- `scripts/` — full init/append/consolidate/build/encrypt/unsigned-sign-submit/retrieve/decrypt/verify flow
