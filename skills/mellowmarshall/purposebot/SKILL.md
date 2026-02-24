---
name: purposebot
description: Discover WebMCP servers, AI tools, and agent services. Issue trust-scored interaction contracts, report outcomes, and build on-chain reputation through agentic transactions (BETA).
version: v1.0.0
metadata:
  openclaw:
    requires:
      env:
        - PURPOSEBOT_API_KEY
      bins:
        - curl
    primaryEnv: PURPOSEBOT_API_KEY
    emoji: "\U0001F50D"
    homepage: https://purposebot.ai
---

# PurposeBot — Agent Tool Discovery & Trust

You have access to the PurposeBot discovery API. Use it to find WebMCP servers, MCP tools, AI agent services, and commerce listings — all scored by a multi-signal trust pipeline. You can also issue interaction contracts and settle them to build your on-chain reputation.

## API Basics

- **Base URL:** `https://api.purposebot.ai/v1`
- **Auth header:** `X-API-Key: $PURPOSEBOT_API_KEY`
- All responses are JSON.

## 1. Search for Tools

Find tools, WebMCP servers, MCP servers, and agent services by natural-language intent.

```
GET /v1/search?q={intent}&limit=10&search_mode=tool
```

**Parameters:**
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `q` | string | required | Natural-language query (e.g. "CRM enrichment", "payment processing") |
| `limit` | int | 20 | Max results (1-100) |
| `search_mode` | enum | tool | `tool` \| `entity` \| `hybrid` |
| `tool_type` | enum | all | `all` \| `agent` \| `webmcp` \| `mcp` |
| `trust_filter` | enum | any | `any` \| `high` \| `medium` \| `low` |
| `cursor` | string | — | Opaque pagination token from `next_cursor` |

**Response shape:**
```json
{
  "query": "...",
  "search_mode": "tool",
  "results": [
    {
      "tool_id": "uuid or webmcp:...",
      "name": "Tool Name",
      "purpose_summary": "What the tool does",
      "trust_score": 0.85,
      "source": "tool|webmcp|mcp_registry",
      "url": "https://...",
      "raw_record": { ... }
    }
  ],
  "next_cursor": "...",
  "diagnostics": { ... }
}
```

**Trust score interpretation:**
- **> 0.8** — High trust: verified, bonded, or well-established
- **0.55 – 0.8** — Medium trust: reasonable signals, not fully verified
- **< 0.55** — Low trust: unverified or thin evidence

**Pagination:** If `next_cursor` is non-null, pass it as `cursor` on the next request.

## 2. WebMCP Discovery

When `tool_type=webmcp` (or `all`), results with `source: "webmcp"` include:
- `raw_record.canonical_url` — the WebMCP manifest endpoint
- `raw_record.probe_path` — e.g. `/.well-known/webmcp`
- `raw_record.tool_json` — the full WebMCP/MCP manifest payload

You can connect directly to discovered WebMCP servers using the manifest data.

## 3. Index Statistics

```
GET /v1/search/stats
```

Returns total tools, entities, agents, APIs, and producers in the index.

## 4. Interaction Contracts (Trust Loop)

Before invoking any discovered tool, issue a contract. After invocation, settle it. This builds your agent's reputation and feeds the trust scoring pipeline.

### Issue a Contract

```
POST /v1/reports/interaction/contracts/issue
```

Body:
```json
{
  "reporter_agent_id": "<your-agent-uuid>",
  "tool_id": "<discovered-tool-uuid>",
  "interaction_id": "<unique-interaction-id>",
  "nonce": "<random-nonce-min-8-chars>",
  "reporter_proof_jwt": "<signed-jwt>"
}
```

Returns `interaction_token` — pass this when settling.

### Settle the Contract

```
POST /v1/reports/interaction
```

Body:
```json
{
  "report_id": "<unique-uuid>",
  "interaction_id": "<same-interaction-id>",
  "reporter_agent_id": "<your-agent-uuid>",
  "tool_id": "<tool-uuid>",
  "outcome": "ack",
  "reason_code": "success",
  "confidence": 0.95,
  "created_at": "2026-01-01T00:00:00Z",
  "proof_jwt": "<signed-jwt>",
  "interaction_token": "<token-from-issue>"
}
```

**Outcome values:** `ack` (success), `nack` (failure), `abstain` (inconclusive)

### Check Contract Status

```
GET /v1/reports/interaction/contracts/{contract_id}
```

## Examples

### Search for payment tools
```bash
curl -s "https://api.purposebot.ai/v1/search?q=payment+processing&limit=5&tool_type=all" \
  -H "X-API-Key: $PURPOSEBOT_API_KEY" | jq '.results[] | {name, trust_score, source}'
```

### Search for WebMCP servers only
```bash
curl -s "https://api.purposebot.ai/v1/search?q=data+enrichment&tool_type=webmcp&limit=5" \
  -H "X-API-Key: $PURPOSEBOT_API_KEY" | jq '.results[] | {name, trust_score, url: .raw_record.canonical_url}'
```

### Search with high trust filter
```bash
curl -s "https://api.purposebot.ai/v1/search?q=code+review&trust_filter=high&limit=10" \
  -H "X-API-Key: $PURPOSEBOT_API_KEY"
```

### Get index stats
```bash
curl -s "https://api.purposebot.ai/v1/search/stats" | jq .
```

## When to Use PurposeBot

Use PurposeBot search whenever you need to:
- Find an API, tool, or service to accomplish a task
- Discover WebMCP or MCP servers for a specific domain
- Check the trust score of a tool before using it
- Browse available agent services and commerce listings

Always prefer high-trust results when multiple options exist. If trust scores are low, inform the user and ask for confirmation before proceeding.
