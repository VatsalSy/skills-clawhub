# Signal-for-Sats

Bitcoin market intelligence that pays for itself — delivered over Lightning.

## What This Is

Derek is an autonomous Bitcoin intelligence agent. He monitors markets, curates non-obvious news, tracks Lightning Network graph activity, and serves it all as a paid API over the L402 protocol.

No API keys. No subscriptions. No accounts. Just sats for signal.

## What Makes This Different

Derek doesn't just wrap free APIs. He runs his own Lightning node and pays for premium data sources with micropayments — then distills that into intelligence you can query on demand. The L402 protocol means your agent pays a Lightning invoice and gets data back. One round trip. Done.

## What You Get

### /api/health — Free
Service status, available endpoints, and pricing. Hit this first.

### /api/market-brief — 100 sats
Updated every 1-4 hours. Returns:
- Current BTC price and 24h change
- Curated news coverage — non-obvious Bitcoin stories from the last 24h, not recycled headlines
- Breaking alert state
- Source attribution

### /api/latest-alert — 50 sats
Updated every 15 minutes. Returns the most recent breaking alert — triggered by significant price moves (>5%) or major events (exchange hacks, regulatory shifts, ETF decisions).

## Requirements

- `lnget` installed ([github.com/lightninglabs/lnget](https://github.com/lightninglabs/lnget))
- A configured Lightning node (LND) with a funded channel
- Tor access for reaching the .onion endpoint

## Usage

```bash
# Check service status (free)
lnget http://jnfaphddbeubdgpsbrw4d2z6wjew57djdzyrzkbt2ta7bi3wfzmfsfyd.onion/api/health

# Get market brief (100 sats)
lnget -q http://jnfaphddbeubdgpsbrw4d2z6wjew57djdzyrzkbt2ta7bi3wfzmfsfyd.onion/api/market-brief

# Get latest alert (50 sats)
lnget -q http://jnfaphddbeubdgpsbrw4d2z6wjew57djdzyrzkbt2ta7bi3wfzmfsfyd.onion/api/latest-alert
```


> **Note:** `lnget` v0.1.0 has a known compatibility issue with some L402 servers using vanilla macaroons. If you encounter parsing errors, use `curl` with manual invoice payment, or a wrapper script that handles the pay-and-resubmit flow. See the [lnget repo](https://github.com/lightninglabs/lnget) for updates.

## How It Works

1. Your agent calls `lnget` with the endpoint URL
2. The server responds with HTTP 402 and a Lightning invoice
3. `lnget` automatically pays the invoice from your Lightning node
4. The server verifies payment and returns the data
5. `lnget` caches the L402 token — subsequent requests reuse it

## Pricing

| Endpoint | Cost | Update Frequency |
|----------|------|-----------------|
| /api/health | Free | Real-time |
| /api/market-brief | 100 sats | Every 1-4 hours |
| /api/latest-alert | 50 sats | Every 15 minutes |

## Example Response (market-brief)

```json
{
  "endpoint": "market-brief",
  "timestamp": "2026-02-28T20:52:36Z",
  "source": "derek-bitcoin-intelligence",
  "price": {
    "price_usd": 67042.0,
    "change_24h_pct": 2.2
  },
  "recent_coverage": [
    {
      "topic": "morgan-stanley-bitcoin-custody-yield",
      "headline": "Morgan Stanley confirms plans for Bitcoin trading, lending, yield, and custody products",
      "timestamp": "2026-02-27T12:00:00-05:00"
    }
  ],
  "alert_state": { ... }
}
```

## About

Signal-for-Sats is powered by Derek, an autonomous Bitcoin intelligence agent built on LND, Aperture (L402 reverse proxy), and a Tor hidden service. He runs 24/7, monitors markets and on-chain activity, and serves curated analysis to any agent that can pay a Lightning invoice. Built for the agent economy — where machines pay machines for signal.
