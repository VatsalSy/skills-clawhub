---
name: pastewatch-mcp
description: Secret redaction MCP server for OpenClaw agents. Prevents API keys, DB credentials, SSH keys, emails, IPs, JWTs, and 29 other secret types from leaking to LLM providers. Use when reading/writing files that may contain secrets, setting up agent security, or auditing for credential exposure.
metadata: {"openclaw":{"requires":{"bins":["pastewatch-cli","mcporter"]}}}
---

# Pastewatch MCP — Secret Redaction

Prevents secrets from reaching your LLM provider. The agent works with placeholders, secrets stay local.

**Source:** https://github.com/ppiankov/pastewatch
**Requires:** `mcporter` (MCP tool management), Swift 5.9.2 runtime on Linux

## Install

### macOS (Homebrew — recommended)

```bash
brew install ppiankov/tap/pastewatch
pastewatch-cli version
```

### Linux (binary + checksum verification)

```bash
# Download binary and checksum
curl -fsSL https://github.com/ppiankov/pastewatch/releases/latest/download/pastewatch-cli-linux-amd64 \
  -o /usr/local/bin/pastewatch-cli
curl -fsSL https://github.com/ppiankov/pastewatch/releases/latest/download/pastewatch-cli-linux-amd64.sha256 \
  -o /tmp/pastewatch-cli.sha256

# Verify checksum before making executable
cd /usr/local/bin && sha256sum -c /tmp/pastewatch-cli.sha256
chmod +x /usr/local/bin/pastewatch-cli

# Verify
pastewatch-cli version
```

If `pastewatch-cli version` fails with `libswiftCore.so: cannot open shared object file`, the Swift runtime is needed. **This modifies /usr/lib — ask the user before proceeding:**

```bash
# Swift 5.9.2 runtime (Linux only, requires root, modifies /usr/lib)
# IMPORTANT: This installs shared libraries into /usr/lib. Confirm with user first.
cd /tmp
curl -fsSL "https://download.swift.org/swift-5.9.2-release/ubuntu2204/swift-5.9.2-RELEASE/swift-5.9.2-RELEASE-ubuntu22.04.tar.gz" -o swift.tar.gz
# Verify download (check size is ~500MB+, not a redirect page)
ls -lh swift.tar.gz
tar xzf swift.tar.gz --wildcards "*/usr/lib/swift/linux/lib*"
cp -af swift-5.9.2-RELEASE-ubuntu22.04/usr/lib/swift/linux/lib* /usr/lib/
ldconfig
rm -rf swift.tar.gz swift-5.9.2-RELEASE-ubuntu22.04
pastewatch-cli version
```

## MCP Server Setup

Requires `mcporter` — install with `npm install -g mcporter` if not present.

```bash
mcporter config add pastewatch --command "pastewatch-cli mcp --audit-log /var/log/pastewatch-audit.log"
mcporter list pastewatch --schema  # should show 6 tools
```

## MCP Tools

| Tool | Purpose |
|------|---------|
| `pastewatch_read_file` | Read file with secrets replaced by `__PW{TYPE_N}__` placeholders |
| `pastewatch_write_file` | Write file, resolving placeholders back to real values locally |
| `pastewatch_check_output` | Verify text contains no raw secrets before returning |
| `pastewatch_scan` | Scan text for sensitive data |
| `pastewatch_scan_file` | Scan a file |
| `pastewatch_scan_dir` | Scan directory recursively |

## How It Works

```
Agent reads config.env → pastewatch intercepts → Agent sees __PW{AWS_KEY_1}__
Agent edits and writes → pastewatch resolves → Real values restored on disk
Secrets never leave your machine.
```

Mappings live in RAM only. No persistence. Die when server stops.

## CLI Usage (no MCP needed)

```bash
echo "AWS_KEY=AKIAIOSFODNN7EXAMPLE" | pastewatch-cli scan
pastewatch-cli scan --file config.yml
pastewatch-cli scan --dir ./project --check
pastewatch-cli scan --format json < input.txt
```

## Detection Scope

29 types: AWS keys, Anthropic/OpenAI/HuggingFace/Groq keys, DB connections, SSH keys, JWTs, emails, IPs, credit cards (Luhn validated), Slack/Discord webhooks, Azure connections, GCP service accounts, npm/PyPI/RubyGems/GitLab tokens, Telegram bot tokens, and more.

Deterministic regex. No ML. No API calls. Microseconds per scan.

## Audit Log

```bash
tail -f /var/log/pastewatch-audit.log
```

Logs timestamps, tool calls, file paths, redaction counts. Never logs secret values.

## Limitations

- Protects secrets (API keys, credentials, tokens) from reaching LLM provider
- Does NOT protect prompt content, business logic, or code structure
- For full privacy, use a local model
