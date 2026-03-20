---
name: notaryos
description: Cryptographic accountability for AI agent actions. Seal every action with Ed25519 signatures, verify receipts, and prove what your agent did — or chose not to do.
version: 2.2.1
metadata:
  openclaw:
    emoji: "\U0001F6E1\uFE0F"
    requires:
      bins:
        - python3
    primaryEnv: NOTARY_API_KEY
    homepage: https://github.com/hellothere012/notaryos
    install:
      - kind: uv
        package: notaryos
        bins: []
---

# NotaryOS — Cryptographic Receipts for Agent Actions

**Every action you take should be verifiable. Every action you don't take should be provable.**

NotaryOS seals your agent's actions with Ed25519 cryptographic signatures. Issue receipts, verify them, and maintain an auditable chain of everything your agent does.

## License

This skill integrates with the NotaryOS API service. The SDKs are licensed under **BSL-1.1** (Business Source License). See https://github.com/hellothere012/notaryos/blob/main/LICENSE for full terms. Converts to Apache 2.0 on 2029-02-25.

## Data Flow and Privacy

> **How data moves:** The SDK sends your payload to `api.agenttownsquare.com` via HTTPS POST. The server computes a SHA-256 hash of the payload, signs the hash with Ed25519, and returns a receipt. Payload retention is tier-gated.

| Tier | Payload Sent? | Payload Retained? | Hash Stored? | Signature Stored? |
|------|--------------|-------------------|-------------|------------------|
| **Demo** (no key) | Yes, via HTTPS | No | Yes | Yes |
| **Free** (registered) | Yes, via HTTPS | Structured metadata only | Yes | Yes |
| **Pro** | Yes, via HTTPS | Configurable (opt-in/out) | Yes | Yes |
| **Enterprise** | Yes, via HTTPS | Zero retention | Yes | Yes |

**What the server always stores:** receipt_id, timestamp, action_type, payload_hash (SHA-256), Ed25519 signature, chain_previous, chain_sequence. **What it never stores on Pro/Enterprise:** the raw payload content.

Use the included `sanitize.py` helper to strip sensitive fields before sealing:

```python
from sanitize import sanitize_payload

clean = sanitize_payload({"user": "alice", "password": "hunter2", "action": "login"})
# {"user": "alice", "action": "login"} — password stripped
```

See the privacy policy at https://notaryos.org/privacy for full data handling details.

## Setup

Install the SDK (zero external dependencies):

```bash
pip install notaryos
```

> **No API key required to start.** The SDK uses a built-in demo key (10 req/min) by default. Set `NOTARY_API_KEY` for production use. Get a key at https://notaryos.org/sign-up

```python
from notaryos import NotaryClient

# Works immediately — no signup, no configuration
notary = NotaryClient()

# For production (higher rate limits, receipt persistence):
# export NOTARY_API_KEY=notary_live_xxx
# notary = NotaryClient(api_key="notary_live_xxx")
```

> **For TypeScript/Node users:** `npm install notaryos` — see https://www.npmjs.com/package/notaryos

## What to Seal

### Default Actions (always safe to seal)

These action types contain no sensitive data by default:

| Action Type | When to Seal |
|---|---|
| `file.created` | Created or modified a file |
| `file.deleted` | Deleted a file |
| `command.executed` | Ran a shell command |
| `config.changed` | Modified system configuration |

### Extended Actions (seal when relevant to the user's task)

Only seal these when the user's task involves these domains:

| Action Type | When to Seal | Sanitize? |
|---|---|---|
| `email.sent` | Sent an email on behalf of user | Yes — strip body, keep subject/to |
| `api.called` | Made an external API call | Yes — strip auth headers |
| `purchase.made` | Made a purchase or transaction | Yes — strip card/account numbers |
| `data.accessed` | Accessed sensitive data | Yes — log access, not content |
| `message.sent` | Sent a message on a platform | Yes — strip message body if private |

**Always use `sanitize_payload()` before sealing actions that may contain user data.**

## How to Seal Actions

```python
from notaryos import NotaryClient
from sanitize import sanitize_payload

notary = NotaryClient()

# Seal an action — 2 arguments: action_type and payload
receipt = notary.seal(
    "file.created",
    sanitize_payload({
        "path": "/src/main.py",
        "lines_added": 42,
        "branch": "feature/auth"
    })
)

print(receipt.receipt_hash)   # SHA-256 hash for lookup
print(receipt.signature)      # Ed25519 signature
print(receipt.verify_url)     # Public verification URL
```

### Payload Guidelines

**Include:** Action metadata, file paths, counts, timestamps, branch names, public identifiers.

**Exclude:** Passwords, API keys, tokens, credit card numbers, SSNs, private message content, file contents, personal health information.

```python
# GOOD — descriptive, auditable, no secrets
receipt = notary.seal("github.pr_created", {
    "repo": "user/project",
    "pr_number": 42,
    "title": "Fix authentication bug",
    "files_changed": 3,
    "branch": "fix/auth-bug"
})

# BAD — includes secrets (sanitize_payload would strip these)
receipt = notary.seal("api.called", {
    "api_key": "sk-secret-xxx",    # STRIPPED by sanitize_payload
    "password": "hunter2"          # STRIPPED by sanitize_payload
})
```

## Verifying Receipts

Anyone can verify a receipt without an API key:

```python
from notaryos import verify_receipt

# Standalone verification — no API key needed, no data sent
is_valid = verify_receipt(receipt.to_dict())  # Returns True or False
```

To look up a receipt by its hash:

```python
notary = NotaryClient()
result = notary.lookup("e1d66b0bdf3f8a7e...")

if result["found"] and result["verification"]["valid"]:
    print("Receipt is authentic and untampered")
    print(f"Signature OK: {result['verification']['signature_ok']}")
```

## Counterfactual Receipts

When you deliberately choose NOT to take an action, record that decision:

```python
# Simple: record a declined action as a regular receipt
receipt = notary.seal("email.declined", {
    "reason": "Draft contained potentially sensitive information",
    "action_considered": "email.send",
    "decision": "blocked — requested user review"
})

# Advanced: commit-reveal protocol for temporal binding
result = notary.commit_counterfactual(
    action_not_taken="financial.execute_trade",
    capability_proof={"permissions": ["trade.execute"]},
    opportunity_context={"ticker": "ACME", "price": 142.50},
    decision_reason="Risk score exceeds threshold",
)
```

## Receipt Chaining

Link receipts into a provenance DAG (proving action B was caused by action A):

```python
receipt1 = notary.seal("file.read", {"file": "report.pdf"})
receipt2 = notary.seal("summary.generated", {
    "source": "report.pdf",
    "summary_length": 500
}, previous_receipt_hash=receipt1.receipt_hash)
```

## Error Handling

```python
from notaryos import NotaryClient, AuthenticationError, RateLimitError, ValidationError

try:
    receipt = notary.seal("action", {"key": "value"})
except RateLimitError as e:
    # Demo key: 10 req/min. Wait or upgrade at notaryos.org
    pass
except AuthenticationError:
    # Invalid or expired API key
    pass
except ValidationError:
    # Bad request (missing action_type, etc.)
    pass
```

## Key Points

- **Zero dependencies** — uses only Python standard library (`urllib`, `hashlib`, `json`)
- **No signup needed to start** — SDK defaults to a free demo key (10 req/min)
- **API key needed for production** — set `NOTARY_API_KEY` or pass `api_key=` to constructor
- **Payloads are transmitted via HTTPS** — use `sanitize_payload()` to strip secrets before sealing
- **Payload retention is tier-gated** — demo/free retain metadata, enterprise retains nothing
- **Ed25519 signatures** — same signature scheme as SSH and TLS
- **Verification is free and public** — `verify_receipt()` and `lookup()` require no authentication

## When NOT to Seal

- Routine read operations that don't access sensitive data
- Internal reasoning steps (unless the user explicitly wants reasoning audit trails)
- High-frequency polling or health checks
- Actions where the overhead would degrade user experience

## External Endpoints

This skill communicates with the following endpoint:

| URL | Method | Data Sent | Purpose |
|-----|--------|-----------|---------|
| `api.agenttownsquare.com/v1/notary/issue` | POST | action_type + payload (JSON) | Issue signed receipt |
| `api.agenttownsquare.com/v1/notary/verify` | POST | receipt object (JSON) | Verify receipt signature |
| `api.agenttownsquare.com/v1/notary/status` | GET | None | Service health check |
| `api.agenttownsquare.com/v1/notary/r/{hash}` | GET | None (hash in URL) | Look up receipt by hash |
| `api.agenttownsquare.com/v1/notary/public-key` | GET | None | Ed25519 public key for offline verification |

No other endpoints are contacted. No telemetry, analytics, or tracking data is sent.

## Links

- Documentation: https://notaryos.org/docs
- Privacy Policy: https://notaryos.org/privacy
- Receipt Explorer: https://notaryos.org/explore
- API Reference: https://notaryos.org/api-docs
- PyPI: https://pypi.org/project/notaryos/
- npm: https://www.npmjs.com/package/notaryos
- GitHub: https://github.com/hellothere012/notaryos
- License: https://github.com/hellothere012/notaryos/blob/main/LICENSE
