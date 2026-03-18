# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2024-03-18

### Changed
- **ShieldClaw is now completely free and open source!**
- Removed all pricing tiers and license restrictions
- All features are now available to everyone at no cost

## [1.0.0] - 2024-03-18

### Added

#### Core Security Features
- **Scan Module** - Automated security scanning for OpenClaw Skills
  - Static code analysis for dangerous functions
  - Hardcoded secret detection
  - Permission risk assessment
  - Suspicious domain detection
  - Risk scoring (0-100)

- **Guard Module** - Real-time behavior monitoring
  - File system operation interception
  - Network request monitoring
  - Process execution blocking
  - Custom protection rules

- **Vault Module** - Sensitive data protection
  - AES-256-GCM encryption
  - Automatic sensitive data detection (phone, email, ID, etc.)
  - Smart data masking
  - Secure key storage in system keychain

- **Audit Module** - Security logging and reporting
  - Complete operation audit trail
  - PDF/Excel report generation
  - Compliance reporting
  - Timeline analysis

#### Technical Features
- Event-driven architecture with EventBus
- Hot configuration reloading
- Prometheus metrics collection
- SQLite with WAL mode for high-performance logging
- Cross-platform support (Windows, macOS, Linux)

#### Development
- TypeScript 5.3+ with strict type checking
- 200+ unit tests with Vitest
- Monorepo structure with pnpm workspaces
- Comprehensive API documentation

[1.1.0]: https://github.com/yourname/shieldclaw/releases/tag/v1.1.0
[1.0.0]: https://github.com/yourname/shieldclaw/releases/tag/v1.0.0
