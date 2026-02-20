---
name: evm-audit-cli
description: AI-powered smart contract auditing using OpenRouter. Lightweight alternative to evmbench - no docker needed.
env:
  required:
    - OPENROUTER_API_KEY
---

# EVM Audit CLI

AI-powered smart contract security auditor - lightweight, no docker.

## What It Does

1. **Reads local Solidity files** - No fetch from block explorers
2. **Calls AI via OpenRouter** - Uses GPT-4o-mini (or other models)
3. **Parses vulnerability report** - Outputs JSON with findings

## What It Does NOT Do

- ❌ Fetch contracts from Etherscan (use local files)
- ❌ Require docker
- ❌ Run static analysis (see `slither-audit` for that)

## Requirements

```bash
# Get free API key from https://openrouter.ai
export OPENROUTER_API_KEY=your_key
```

## Usage

```bash
python3 evm-audit-cli.py /path/to/contracts/

# With specific model
python3 evm-audit-cli.py ./contracts/ --model openai/gpt-4o

# JSON output
python3 evm-audit-cli.py ./contracts/ --format json
```

## Example Output

```
# Audit Report: Vulnerable.sol
**Model:** openai/gpt-4o-mini

- **Reentrancy Attack** (critical)
  The withdraw function can be exploited via a reentrancy attack.

**Note:** AI analysis - verify findings manually
```

## Models

Default: `openai/gpt-4o-mini` (fast, cheap)

Other options:
- `openai/gpt-4o` (more capable)
- `anthropic/claude-3.5-sonnet` (if available)
- `google/gemini-2.0-flash-exp` (fast)

## Limitations

- Local files only
- AI can miss issues - verify manually
- For professional audits, use manual review + slither

## See Also

- `slither-audit` - Static analysis with Slither (no AI, no API key)
- `evmbench` - Full Docker-based AI auditing