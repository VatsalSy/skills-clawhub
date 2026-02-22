# Code Security Audit

Unified security audit toolkit for comprehensive code security analysis.

## Features

- **OWASP Top 10 Detection** - All 10 vulnerability categories with code patterns
- **Dependency Vulnerability Scanning** - npm, pip, cargo, go modules
- **Secret Detection** - 50+ API key patterns, credentials, private keys
- **SSL/TLS Verification** - Certificate validation, cipher suite checks
- **Security Scoring** - Quantified 0-100 security score
- **Multi-Language Support** - JS/TS, Python, Go, Java, Rust, PHP, Ruby

## Quick Start

```bash
# Full security audit with scoring
./scripts/security-audit.sh --full

# Quick scan (secrets + dependencies only)
./scripts/security-audit.sh --quick

# OWASP Top 10 check
./scripts/security-audit.sh --owasp

# SSL/TLS verification
./scripts/security-audit.sh --ssl example.com

# Generate report
./scripts/security-audit.sh --full --output report.md
```

## Security Score

| Score | Risk Level |
|-------|------------|
| 90-100 | ✅ Low |
| 70-89 | ⚠️ Medium |
| 50-69 | 🔶 High |
| 0-49 | 🚨 Critical |

## CI/CD Integration

See `templates/` directory for GitHub Actions and GitLab CI templates.

## License

MIT
