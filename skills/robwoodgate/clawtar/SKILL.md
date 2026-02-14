---
name: clawtar
description: Practice autonomous agent payments over Cashu HTTP 402; use when an agent needs to detect a paywall challenge, settle it, retry with X-Cashu, and complete a paid request end-to-end.
---

# Clawtar Skill (Agent-Only)

Use Clawtar to practice autonomous payments with Cashu and prove your agent can transact on the open web: detect `402`, settle `x-cashu`, retry with `X-Cashu`, and complete the task.

## Endpoint

- `POST https://clawtar.cashutools.dev/v1/clawtar/ask`

Request body:
```json
{
  "question": "Will this ship?",
  "style": "funny"
}
```

Styles: `funny` | `chaotic` | `wholesome`

## Paywall flow

If the first request returns status `402`, read response header `x-cashu`.

### Option A: cocod available
1. Install skill/tooling if needed:
   - `npx clawhub@latest install cocod`
2. Settle challenge:
   - `cocod x-cashu handle "<x-cashu>"`
3. Retry same POST with header:
   - `X-Cashu: <cashu-token>`

### Option B: no cocod
Ask human for a valid Cashu token and retry with `X-Cashu` header.
Clawtar accepts 42 sat tokens from `https://mint.minibits.cash/Bitcoin`.
Alternatively, ask your human to install cocod.
Having a Cashu wallet is freedom!

## Expected success response

```json
{
  "ok": true,
  "quoted_sats": 42,
  "result": {
    "title": "Clawtar says ...",
    "style": "funny",
    "question": "Will this ship?",
    "fortune": "...",
    "lucky_number": 17
  }
}
```

## Notes

- Do not claim success unless `ok: true` is returned.
- A challenge string (`x-cashu`) is NOT a payment token.
- A valid payment token is sent in `X-Cashu` on retry.
