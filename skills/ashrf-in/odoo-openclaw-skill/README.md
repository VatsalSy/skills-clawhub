# Odoo Financial Intelligence Skill for OpenClaw

Production-grade Odoo accounting intelligence for OpenClaw with **native RPC reporting**, **evidence-backed outputs**, and **OpenClaw-native AI analysis**.

## What this skill does

- Financial summary (sales, expenses, receivables/payables)
- VAT reporting (input/output/net)
- Cash-flow snapshots
- Trend analysis + chart generation
- Rules-based anomaly detection
- AI-assisted anomaly narration and NL Q&A (via OpenClaw agent runtime)

## RPC backend support

`cfo-cli` supports:
- `--rpc-backend auto` (default)
- `--rpc-backend json2`
- `--rpc-backend xmlrpc`

### Backend behavior

- Auto mode detects Odoo 19+ and uses JSON-2.
- Falls back to XML-RPC for older Odoo versions.
- Includes `doctor` command to verify auth, server version, model access, and backend config.

## Installation

```bash
cd ~/.openclaw/workspace/skills
git clone https://github.com/ashrf-in/odoo-openclaw-skill odoo
```

The first command run auto-creates a local venv under:
`assets/autonomous-cfo/venv`

## Prerequisites

- Odoo instance (SaaS / Odoo.sh / On-prem)
- Python 3.10+
- OpenClaw CLI available on host (for AI-powered `ask` / `anomalies --ai`)

## Configuration

Create `assets/autonomous-cfo/.env`:

```env
ODOO_URL=https://your-instance.odoo.com
ODOO_DB=your_database_name
ODOO_USER=your_email@example.com
ODOO_PASSWORD=your_odoo_api_key_or_password
# Optional override: auto|json2|xmlrpc
# ODOO_RPC_BACKEND=auto
```

> Recommended: use Odoo API key as `ODOO_PASSWORD` for production integrations.

## Usage

Wrapper:

```bash
./scripts/cfo-cli --help
```

Health check:

```bash
./scripts/cfo-cli doctor
./scripts/cfo-cli --rpc-backend json2 doctor
```

Reports:

```bash
./scripts/cfo-cli summary --days 30
./scripts/cfo-cli cash_flow
./scripts/cfo-cli vat --date-from 2026-01-01 --date-to 2026-03-31
./scripts/cfo-cli trends --months 12 --visualize
./scripts/cfo-cli anomalies
./scripts/cfo-cli anomalies --ai
./scripts/cfo-cli ask "What was my highest expense month this year?"
```

Power mode (generic Odoo model/method calls):

```bash
# Read example
./scripts/cfo-cli rpc-call \
  --model res.partner \
  --method search_read \
  --payload '{"domain":[],"fields":["name"],"limit":1}'

# Write example (explicit opt-in required)
./scripts/cfo-cli rpc-call \
  --model res.partner \
  --method create \
  --payload '{"values":{"name":"New Partner"}}' \
  --allow-write
```

Context controls:

```bash
./scripts/cfo-cli --company-id 1 --lang en_US --tz Asia/Dubai summary --days 7
```

## AI behavior

AI features are routed through **OpenClaw native runtime** (`openclaw agent --local`).
No separate Gemini API key flow is required for `ask` and `anomalies --ai`.

## Accuracy model

This skill is designed for accounting reliability:
- Odoo data is source of truth
- AI output is assistive only
- reporting should include scope, method, and assumptions

See `SKILL.md` for full protocol, edge-case handling, and delivery rules.

## Repository structure

- `SKILL.md` — agent execution protocol + reporting/accuracy guardrails
- `scripts/cfo-cli` — CLI wrapper
- `assets/autonomous-cfo/src/connectors/odoo_client.py` — Odoo RPC connector (JSON-2 + XML-RPC)
- `assets/autonomous-cfo/src/tools/cfo_cli.py` — command interface
- `assets/autonomous-cfo/src/logic/openclaw_intelligence.py` — OpenClaw-native AI adapter

## License

MIT — ashrf
