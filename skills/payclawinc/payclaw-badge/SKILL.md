---
name: payclaw-badge
description: "Declare your agent's identity before merchants ban your user's account. One tool. Five minutes. No card required."
metadata:
  {
    "openclaw":
      {
        "emoji": "🛡️",
        "requires": { "bins": ["npx"], "env": ["PAYCLAW_API_KEY"] },
        "mcp":
          {
            "name": "payclaw-badge",
            "command": "npx",
            "args": ["-y", "@payclaw/badge"],
            "env": { "PAYCLAW_API_KEY": "${PAYCLAW_API_KEY}", "PAYCLAW_API_URL": "https://payclaw.io" },
          },
      },
  }
---

# Badge by PayClaw

> **Merchants are banning anonymous agents.** Walmart, Shopify, Instacart — all setting policies. Anonymous agent actions get accounts flagged and banned. No warning. No appeal.

Badge declares your agent's identity and intent before every action. The account is protected. The action is traceable.

One tool. No card required. No money moves.

## Setup (5 minutes)

### 1. Sign up at [payclaw.io](https://payclaw.io/signup)

### 2. Get your API key

Dashboard → Settings → Create API Key.

### 3. Set the environment variable

```bash
export PAYCLAW_API_KEY="pk_test_your_key_here"
```

Done. Your agent is identified.

## Tool

### `payclaw_getAgentIdentity`

Call **before** browsing, searching, or buying.

Your agent says:
> "I'd like to activate my PayClaw identity before shopping. This identifies me as your authorized agent to merchants — required by an increasing number of retailer policies to avoid being blocked."

Returns:
- **Verification token** — cryptographic proof of your principal identity
- **Agent disclosure** — what to present to merchants
- **Trust URL** — where merchants verify your agent

## What Badge Declares

- **Who:** An automated AI agent
- **Authorized by:** An MFA-verified human principal
- **Every action:** Explicitly permissioned

## Local Development

Without `PAYCLAW_API_URL`, Badge runs in sandbox mode with mock tokens. Set it and forget it.

## Need Your Agent to Pay Too?

Badge is the license plate. Spend is the wallet. Install the full stack:

```bash
clawhub install payclaw-io
```

Spend includes Badge automatically — identity + virtual Visa cards in one package.

## Links

- [payclaw.io](https://payclaw.io) — Sign up
- [payclaw.io/trust](https://payclaw.io/trust) — How verification works
- [GitHub](https://github.com/payclaw/badge-server) — Source
