---
name: klientenportal
description: "Automate RZL Klientenportal.at — a web-based portal by RZL Software for exchanging receipts, invoices, and reports with your tax accountant. Login/logout, upload documents (Belegübergabe), list released files, and download Kanzleidokumente via Playwright."
summary: "RZL Klientenportal automation: upload receipts, download reports."
version: 1.3.0
homepage: https://github.com/odrobnik/klientenportal-skill
metadata:
  openclaw:
    emoji: "📋"
    requires:
      bins: ["python3", "playwright"]
      python: ["playwright"]
---

# RZL Klientenportal

Automate [klientenportal.at](https://klientenportal.at) — a web portal by [RZL Software](https://www.rzl.at) for securely exchanging accounting documents between clients and their tax accountant. Upload receipts and invoices, download reports and Kanzleidokumente, all via Playwright browser automation.

**Entry point:** `{baseDir}/scripts/klientenportal.py`

## Setup

See [SETUP.md](SETUP.md) for prerequisites, installation, and configuration.

## Belegkreis Categories

| Code | Name | Use for |
|------|------|---------|
| ER | Eingangsrechnungen | Incoming invoices |
| AR | Ausgangsrechnungen | Outgoing invoices |
| KA | Kassa | Credit card payments |
| SP | Sparkasse | Bank account receipts |

## Commands

```bash
python3 {baseDir}/scripts/klientenportal.py login
python3 {baseDir}/scripts/klientenportal.py upload -f invoice.pdf --belegkreis KA
python3 {baseDir}/scripts/klientenportal.py upload -f *.xml --belegkreis SP
python3 {baseDir}/scripts/klientenportal.py released
python3 {baseDir}/scripts/klientenportal.py download
python3 {baseDir}/scripts/klientenportal.py logout
```

## Recommended Flow

```
login → upload / released / download → logout
```

Always call `logout` after completing all operations to clear the stored browser session.

## Notes
- Session state stored in `{workspace}/klientenportal/` with restrictive permissions (dirs 700, files 600).
- Download output defaults to `/tmp/openclaw/klientenportal/` (override with `-o`), sandboxed to workspace or `/tmp`.
- Credentials in `config.json` only — no `.env` file loading.
