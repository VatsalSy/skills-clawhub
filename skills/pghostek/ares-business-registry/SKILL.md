---
name: ares-business-registry
description: Query Czech ARES business registry by ICO or name with human/JSON/raw outputs, retries, and legal-form decoding.
---

# ARES Business Registry (CZ)

Use `scripts/ares_client.py` for ICO lookup and business search.

## Working directory

- From workspace root:
  - `python3 skills/ares-business-registry/scripts/ares_client.py ...`
- From `skills/ares-business-registry`:
  - `python3 scripts/ares_client.py ...`

## Commands

You can run via the wrapper (recommended):
- `./ares ico <ico>`
- `./ares name "NAME" [--city CITY] [--limit N] [--offset N] [--pick INDEX]`

The underlying script also supports:
- `python3 scripts/ares_client.py search --name "NAME" ...`

## Output modes

- default: human-readable summary
- `--json`: normalized JSON output (stable keys)
- `--raw`: full raw ARES payload

## Examples

```bash
python3 scripts/ares_client.py ico 27604977
python3 scripts/ares_client.py ico 27604977 --json
python3 scripts/ares_client.py ico 27604977 --raw

python3 scripts/ares_client.py search --name Google
python3 scripts/ares_client.py search --name Google --limit 3 --json
python3 scripts/ares_client.py search --name Google --city Praha --limit 10 --offset 0
python3 scripts/ares_client.py search --name Google --limit 3 --pick 1
```

## Normalized JSON

- `ico` output:
  - `{ "subject": { "name", "ico", "dic", "datumVzniku", "address", "codes", "decoded" } }`
- `search` output:
  - `{ "query", "total", "items", "picked?" }`
- `dic` can be `null`.
- `datumVzniku` can be `null`.

## Error JSON contract (`--json` only)

```json
{
  "error": {
    "code": "validation_error | ares_error | network_error",
    "message": "Human readable message",
    "status": 429,
    "details": {}
  }
}
```

## Validation and exits

- ICO: exactly 8 digits + mod11 checksum
- Search: `--name` length >= 3
- `--limit`: default 10, capped to 100
- `--offset`: must be >= 0
- Exit codes:
  - `0` success
  - `1` validation error
  - `2` ARES non-OK response
  - `3` network/timeout

## Caching and decoding

- Legal form decoding (`PravniForma`) is loaded via POST `/ciselniky-nazevniky/vyhledat`
- Cache path: `skills/ares-business-registry/.cache/pravni_forma.json`
- Cache TTL: 24h
- In-memory fallback is used if cache file is stale/unavailable
- Curated overrides:
  - `112 -> s.r.o.`
  - `121 -> a.s.`
  - `141 -> z.s.`
  - `701 -> OSVČ`
  - `301 -> s.p.`
  - `331 -> p.o.`

## City filter limitation

- `--city` maps to `sidlo.nazevObce` (structured filter).
- Matching remains best-effort only; ARES server-side matching/ranking can still return records outside the expected municipality.

## Retries and rate limits

- HTTP timeout: connect 5s, read 20s
- Retries for transient failures: `429/502/503/504` + network timeout/connection issues
- Backoff: `1s`, `2s`, `4s`
- Honors `Retry-After` for 429 where provided
