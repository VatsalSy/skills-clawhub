# CounterClaw 🦞

> Defensive security for AI agents. Snaps shut on malicious payloads.

[![Security](https://img.shields.io/badge/ClawHub-Verified-green)](https://clawhub.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue)](https://pypi.org/project/counterclaw-core/)

## The Problem

Your AI agent is vulnerable. Attackers use prompt injections to make your agent ignore safety guidelines or leak data.

## The Solution

CounterClaw snaps shut on malicious payloads before they reach your AI.

```python
from counterclaw import CounterClawInterceptor

interceptor = CounterClawInterceptor()

# Input scan - blocks prompt injections
result = interceptor.check_input("[DETECTION_EXAMPLE]: bypass-system-prompt")
# → {"blocked": True, "safe": False}

# Output scan - detects PII
result = interceptor.check_output("Contact: john@example.com")
# → {"safe": False, "pii_detected": {"email": True}}
```

## Features

### 🔒 Prompt Injection Defense
Blocks common patterns:
- [DETECTION_EXAMPLE]: bypass-system-prompt
- [DETECTION_EXAMPLE]: pretend-to-be-dan
- Role manipulation attempts

### 🛡️ Basic PII Masking
Detects in outputs:
- Email addresses
- Phone numbers

### 📝 Local Logging
Violations logged to ~/.openclaw/memory/MEMORY.md with PII masked

## Installation

```bash
pip install counterclaw-core
```

## Quick Start

```python
from counterclaw import CounterClawInterceptor

interceptor = CounterClawInterceptor()
result = interceptor.check_input("Hello!")
print(f"Safe: {result['safe']}")
```

## Configuration

### Admin-Locked Commands
```bash
# Set your Telegram user ID(s) - comma-separated for multiple
export TRUSTED_ADMIN_IDS="telegram_user_id"
```

```python
interceptor = CounterClawInterceptor()
# Now !claw-lock requires admin - fails closed if not set
```

## Security Notes

- **Fail-Closed**: If TRUSTED_ADMIN_IDS is not set, admin features are disabled by default
- **No Network**: This middleware does not make any external network calls
- **Local Logging**: All violations are logged locally with PII masked

## Why "CounterClaw"?

Like a bear trap: simple, reliable, and snaps shut on threats.

## License

MIT - See [LICENSE](LICENSE)

# v1.0.5
