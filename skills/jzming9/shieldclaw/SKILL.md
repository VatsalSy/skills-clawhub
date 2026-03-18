---
name: shieldclaw
description: "Security suite for OpenClaw. Provides security scanning, real-time protection, audit logging, and sensitive data encryption. Use this skill when users need security-related operations, threat detection, or data protection."
metadata:
  {
    "copaw":
      {
        "emoji": "🛡️",
        "requires": {}
      }
  }
---

# ShieldClaw Security Suite

Use this skill when users need security-related operations in OpenClaw, including:
- Scanning Skills for security risks
- Monitoring and blocking suspicious operations
- Encrypting sensitive data
- Generating security audit reports

## Core Capabilities

### 1. Security Scan (scan)
Scan OpenClaw Skills for potential security risks.

**When to use:**
- User wants to check if a Skill is safe
- Before installing a new Skill
- Regular security audits

**Usage:**
```typescript
// Perform security scan
scanSkill(skillPath: string): ScanReport

// Check specific risk types
checkPermissions(skillId: string): PermissionRisk[]
checkNetworkDomains(skillId: string): DomainRisk[]
```

### 2. Real-time Guard (guard)
Monitor and intercept suspicious operations in real-time.

**When to use:**
- User wants to protect sensitive files/directories
- Blocking dangerous API calls
- Enforcing security policies

**Usage:**
```typescript
// Register protection rules
registerGuardRule(rule: GuardRule): void

// Check if operation is allowed
validateOperation(context: OperationContext): boolean
```

### 3. Data Vault (vault)
Encrypt and securely store sensitive data.

**When to use:**
- User needs to store passwords, API keys, or credentials
- Masking sensitive data in logs
- Secure data transmission

**Usage:**
```typescript
// Encrypt sensitive data
encrypt(data: string, type: DataType): VaultEntry

// Decrypt when needed
decrypt(vaultId: string): string

// Auto-detect and mask sensitive data
maskSensitiveData(text: string): ProcessResult
```

### 4. Audit & Reporting (audit)
Log operations and generate security reports.

**When to use:**
- User needs security reports
- Security incident investigation
- Operation history review

**Usage:**
```typescript
// Log security event
logAudit(event: AuditEvent): void

// Generate security report
generateReport(options: ReportOptions): AuditReport
```

## Safety Guidelines

- Always scan third-party Skills before installation
- Use Vault for any sensitive data (passwords, keys, tokens)
- Enable Guard for critical directories (SSH keys, config files)
- Regularly review audit logs for suspicious activities

## Limitations

- Vault encryption keys are stored in system keychain
- Some features require manual configuration

## Related Skills

- browser_use: For web-based security checks
- file_reader: For reading security reports
- execute_shell_command: For system-level security operations
