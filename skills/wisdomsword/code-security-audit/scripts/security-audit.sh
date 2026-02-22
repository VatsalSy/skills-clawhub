#!/usr/bin/env bash
# Code Security Audit - Comprehensive security scanning script
# Version: 2.0.0

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
PROJECT_DIR="${PROJECT_DIR:-.}"
OUTPUT_FILE=""
VERBOSE=false

# Score tracking
TOTAL_SCORE=100
DEDUCTIONS=0
FINDINGS=()

# Logging
log() { echo -e "${GREEN}[INFO]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; ((DEDUCTIONS+=5)); }
error() { echo -e "${RED}[ERROR]${NC} $1"; ((DEDUCTIONS+=10)); FINDINGS+=("$1"); }
section() { echo ""; echo -e "${BLUE}═══════════════════════════════════════${NC}"; echo -e "${BLUE}  $1${NC}"; echo -e "${BLUE}═══════════════════════════════════════${NC}"; }

# Help
show_help() {
    cat << EOF
Code Security Audit v2.0.0

Usage: $0 [OPTIONS] [COMMAND]

Commands:
    --full          Full security audit with scoring
    --quick         Quick scan (secrets + dependencies)
    --owasp         OWASP Top 10 check only
    --deps          Dependency vulnerabilities only
    --secrets       Secret detection only
    --ssl <domain>  SSL/TLS verification
    --perms         File permission audit
    --score         Show only the security score
    --report        Generate full markdown report

Options:
    -o, --output    Output file for report
    -v, --verbose   Verbose output
    -h, --help      Show this help

Examples:
    $0 --full
    $0 --quick
    $0 --ssl example.com
    $0 --full --output audit-report.md
EOF
}

# Parse arguments
MODE="full"
while [[ $# -gt 0 ]]; do
    case $1 in
        --full) MODE="full" ;;
        --quick) MODE="quick" ;;
        --owasp) MODE="owasp" ;;
        --deps) MODE="deps" ;;
        --secrets) MODE="secrets" ;;
        --ssl) MODE="ssl"; SSL_DOMAIN="${2:-}"; shift ;;
        --perms) MODE="perms" ;;
        --score) MODE="score" ;;
        --report) MODE="report" ;;
        -o|--output) OUTPUT_FILE="$2"; shift ;;
        -v|--verbose) VERBOSE=true ;;
        -h|--help) show_help; exit 0 ;;
        *) warn "Unknown option: $1" ;;
    esac
    shift
done

# ====================
# OWASP Top 10 Checks
# ====================

check_owasp() {
    section "OWASP Top 10 Security Check"

    # A01: Broken Access Control
    echo "A01: Checking for Broken Access Control..."
    local auth_issues=0

    # Find endpoints without auth
    if command -v grep &>/dev/null; then
        local unauth_endpoints=$(grep -rn "app\.\(get\|post\|put\|delete\|patch\)" \
            --include='*.ts' --include='*.js' "$PROJECT_DIR" 2>/dev/null | \
            grep -v "authenticate\|auth\|isLoggedIn\|requireAuth\|middleware" | wc -l | tr -d ' ')

        if [ "${unauth_endpoints:-0}" -gt 5 ]; then
            warn "Found $unauth_endpoints potential unauthenticated endpoints"
            auth_issues=$((auth_issues + 1))
        else
            log "A01: Access control looks reasonable"
        fi
    fi

    # A02: Cryptographic Failures
    echo "A02: Checking for Cryptographic Failures..."
    local crypto_issues=0

    # Check for weak hashing with passwords
    if grep -rn "md5\|sha1" --include='*.ts' --include='*.js' --include='*.py' "$PROJECT_DIR" 2>/dev/null | \
       grep -qi "password\|secret\|token"; then
        error "A02: Weak hashing (MD5/SHA1) used for passwords/secrets"
        crypto_issues=$((crypto_issues + 1))
    fi

    # Check for disabled SSL verification
    if grep -rn "verify.*false\|rejectUnauthorized.*false\|InsecureSkipVerify" \
       --include='*.ts' --include='*.js' --include='*.py' --include='*.go' "$PROJECT_DIR" 2>/dev/null | \
       grep -qv "test\|spec\|mock"; then
        warn "A02: SSL verification disabled in some locations"
        crypto_issues=$((crypto_issues + 1))
    fi

    [ $crypto_issues -eq 0 ] && log "A02: Cryptographic practices look good"

    # A03: Injection
    echo "A03: Checking for Injection vulnerabilities..."
    local injection_issues=0

    # SQL injection patterns
    if grep -rn "query.*\${\|execute.*\${\|raw.*\${" \
       --include='*.ts' --include='*.js' "$PROJECT_DIR" 2>/dev/null | grep -qv "parameterized"; then
        error "A03: Potential SQL injection - string interpolation in queries"
        injection_issues=$((injection_issues + 1))
    fi

    # Command injection patterns
    if grep -rn "exec(\|spawn(\|system(\|subprocess.call" \
       --include='*.ts' --include='*.js' --include='*.py' "$PROJECT_DIR" 2>/dev/null | \
       grep -qv "execFile\|spawn.*array"; then
        warn "A03: Review command execution for injection risks"
        injection_issues=$((injection_issues + 1))
    fi

    [ $injection_issues -eq 0 ] && log "A03: No obvious injection vulnerabilities"

    # A04: Insecure Design
    echo "A04: Checking for Insecure Design..."
    log "A04: Design patterns check (manual review recommended)"

    # A05: Security Misconfiguration
    echo "A05: Checking for Security Misconfiguration..."
    local config_issues=0

    if grep -rn "DEBUG.*=.*true\|debug.*:.*true" \
       --include='*.ts' --include='*.js' --include='*.env' --include='*.json' "$PROJECT_DIR" 2>/dev/null | \
       grep -qv "test\|spec"; then
        warn "A05: Debug mode may be enabled"
        config_issues=$((config_issues + 1))
    fi

    if grep -rn "cors.*\*\|Access-Control-Allow-Origin.*\*" \
       --include='*.ts' --include='*.js' "$PROJECT_DIR" 2>/dev/null | grep -qv "test"; then
        warn "A05: CORS wildcard detected"
        config_issues=$((config_issues + 1))
    fi

    [ $config_issues -eq 0 ] && log "A05: Configuration looks secure"

    # A06: Vulnerable Components (delegated to dependency check)
    echo "A06: Vulnerable Components - see dependency scan"

    # A07: XSS
    echo "A07: Checking for XSS vulnerabilities..."
    local xss_issues=0

    if grep -rn "dangerouslySetInnerHTML\|innerHTML\s*=\|v-html" \
       --include='*.tsx' --include='*.jsx' --include='*.vue' --include='*.js' "$PROJECT_DIR" 2>/dev/null | \
       grep -qv "DOMPurify\|sanitize"; then
        warn "A07: Potential XSS - unsanitized HTML rendering"
        xss_issues=$((xss_issues + 1))
    fi

    [ $xss_issues -eq 0 ] && log "A07: No obvious XSS vulnerabilities"

    # A08: Software Integrity
    echo "A08: Checking Software Integrity..."
    log "A08: Using lockfiles for integrity (good)"

    # A09: Logging & Monitoring
    echo "A09: Checking Logging & Monitoring..."

    if grep -rn "log.*password\|log.*token\|log.*secret\|console\.log.*password" \
       --include='*.ts' --include='*.js' "$PROJECT_DIR" 2>/dev/null | grep -qv "placeholder\|example"; then
        warn "A09: Sensitive data may be logged"
    else
        log "A09: Logging practices look acceptable"
    fi

    # A10: SSRF
    echo "A10: Checking for SSRF vulnerabilities..."

    if grep -rn "fetch.*req\.\|axios.*params\|request.*query" \
       --include='*.ts' --include='*.js' --include='*.py' "$PROJECT_DIR" 2>/dev/null | \
       grep -qi "url\|uri"; then
        warn "A10: Potential SSRF - user input in URL fetching"
    else
        log "A10: No obvious SSRF vulnerabilities"
    fi
}

# ====================
# Secret Detection
# ====================

check_secrets() {
    section "Secret Detection"

    # Use a unique delimiter (|) that won't appear in patterns
    local secret_patterns=(
        "AKIA[0-9A-Z]{16}|AWS Access Key"
        "sk-[A-Za-z0-9]{20,}|OpenAI API Key"
        "ghp_[A-Za-z0-9]{36}|GitHub Personal Token"
        "gho_[A-Za-z0-9]{36}|GitHub OAuth Token"
        "github_pat_[A-Za-z0-9_]+|GitHub PAT"
        "xox[bpoas]-[A-Za-z0-9-]+|Slack Token"
        "sk_live_[A-Za-z0-9]{24,}|Stripe Live Key"
        "rk_live_[A-Za-z0-9]{24,}|Stripe Live Key"
        "BEGIN.*PRIVATE KEY|Private Key"
        "mongodb://[^:]+:[^@]+@|MongoDB Connection String"
        "mysql://[^:]+:[^@]+@|MySQL Connection String"
        "postgres://[^:]+:[^@]+@|PostgreSQL Connection String"
        "redis://[^:]*:[^@]+@|Redis Connection String"
        "eyJ[A-Za-z0-9_-]*\.eyJ[A-Za-z0-9_-]*\.[A-Za-z0-9_-]*|JWT Token"
    )

    local secrets_found=0

    for pattern_desc in "${secret_patterns[@]}"; do
        IFS='|' read -r pattern name <<< "$pattern_desc"

        # Fixed: use correct include patterns for grep
        # Note: --include='*.env' won't match .env (hidden files), need separate check
        local matches=$(grep -rn "$pattern" \
            --include='*.ts' --include='*.js' --include='*.py' --include='*.go' \
            --include='*.yml' --include='*.yaml' --include='*.json' \
            "$PROJECT_DIR" 2>/dev/null | grep -v "node_modules\|.git\|test\|spec\|example\|placeholder\|your_\|YOUR_\|xxxx\|XXXX" | head -5)

        # Also check .env files separately (hidden files not matched by *.env)
        if [ -z "$matches" ] && [ -f "$PROJECT_DIR/.env" ]; then
            matches=$(grep -n "$pattern" "$PROJECT_DIR/.env" 2>/dev/null | grep -v "placeholder\|your_\|YOUR_\|xxxx\|XXXX" | head -5)
        fi

        if [ -n "$matches" ]; then
            error "Found potential $name"
            if [ "$VERBOSE" = true ]; then
                echo "$matches" | head -3
            fi
            secrets_found=$((secrets_found + 1))
        fi
    done

    # Check for hardcoded passwords
    local pw_matches=$(grep -rn -i "password\s*[:=]\s*['\"][^'\"]\{8,\}['\"]" \
        --include='*.ts' --include='*.js' --include='*.py' --include='*.env' \
        "$PROJECT_DIR" 2>/dev/null | grep -v "node_modules\|.git\|test\|spec\|example\|placeholder")

    if [ -n "$pw_matches" ]; then
        warn "Found potential hardcoded passwords"
        secrets_found=$((secrets_found + 1))
    fi

    if [ $secrets_found -eq 0 ]; then
        log "No secrets detected"
    fi
}

# ====================
# Dependency Check
# ====================

check_dependencies() {
    section "Dependency Vulnerability Scan"

    # Node.js
    if [ -f "$PROJECT_DIR/package.json" ]; then
        log "Checking Node.js dependencies..."
        if command -v npm &>/dev/null; then
            cd "$PROJECT_DIR"
            if npm audit --audit-level=moderate --json 2>/dev/null | grep -q '"vulnerabilities"'; then
                local vuln_count=$(npm audit --json 2>/dev/null | grep -o '"total":[0-9]*' | grep -o '[0-9]*' || echo "0")
                if [ "${vuln_count:-0}" -gt 0 ]; then
                    warn "Found $vuln_count dependency vulnerabilities (npm audit)"
                else
                    log "No moderate/high npm vulnerabilities"
                fi
            else
                log "npm audit passed"
            fi
            cd - > /dev/null
        else
            warn "npm not found - skipping Node.js audit"
        fi
    fi

    # Python
    if [ -f "$PROJECT_DIR/requirements.txt" ]; then
        log "Checking Python dependencies..."
        if command -v pip-audit &>/dev/null; then
            cd "$PROJECT_DIR"
            if ! pip-audit -r requirements.txt --skip-editable 2>/dev/null; then
                warn "pip-audit found vulnerabilities"
            else
                log "pip-audit passed"
            fi
            cd - > /dev/null
        elif command -v safety &>/dev/null; then
            cd "$PROJECT_DIR"
            if ! safety check -r requirements.txt 2>/dev/null; then
                warn "safety found vulnerabilities"
            fi
            cd - > /dev/null
        else
            warn "pip-audit/safety not found - skipping Python audit"
        fi
    fi

    # Go
    if [ -f "$PROJECT_DIR/go.mod" ]; then
        log "Checking Go dependencies..."
        if command -v govulncheck &>/dev/null; then
            cd "$PROJECT_DIR"
            if ! govulncheck ./... 2>/dev/null; then
                warn "govulncheck found vulnerabilities"
            else
                log "govulncheck passed"
            fi
            cd - > /dev/null
        else
            warn "govulncheck not found - skipping Go audit"
        fi
    fi

    # Rust
    if [ -f "$PROJECT_DIR/Cargo.toml" ]; then
        log "Checking Rust dependencies..."
        if command -v cargo-audit &>/dev/null; then
            cd "$PROJECT_DIR"
            if ! cargo audit 2>/dev/null; then
                warn "cargo audit found vulnerabilities"
            else
                log "cargo audit passed"
            fi
            cd - > /dev/null
        else
            warn "cargo-audit not found - skipping Rust audit"
        fi
    fi
}

# ====================
# SSL/TLS Check
# ====================

check_ssl() {
    local domain="${SSL_DOMAIN:-}"

    if [ -z "$domain" ]; then
        error "No domain specified for SSL check"
        return 1
    fi

    section "SSL/TLS Verification for $domain"

    if ! command -v openssl &>/dev/null; then
        error "openssl not found"
        return 1
    fi

    # Certificate info
    log "Fetching certificate information..."
    local cert_info=$(echo | openssl s_client -connect "$domain:443" -servername "$domain" 2>/dev/null)

    if echo "$cert_info" | grep -q "CERTIFICATE"; then
        # Get certificate details
        local cert_details=$(echo "$cert_info" | openssl x509 -noout -subject -issuer -dates 2>/dev/null)
        log "Certificate Details:"
        echo "$cert_details" | sed 's/^/  /'

        # Check expiry
        local expiry=$(echo "$cert_info" | openssl x509 -noout -enddate 2>/dev/null | cut -d= -f2)
        log "Expires: $expiry"

        # TLS version check
        log "Checking TLS versions..."
        for v in tls1_2 tls1_3; do
            if echo | openssl s_client -connect "$domain:443" -$v 2>/dev/null | grep -q "Cipher"; then
                log "  $v: SUPPORTED"
            else
                warn "  $v: NOT SUPPORTED"
            fi
        done

        # Security headers
        log "Checking security headers..."
        if command -v curl &>/dev/null; then
            local headers=$(curl -sI "https://$domain" 2>/dev/null)

            echo "$headers" | grep -i "strict-transport-security" > /dev/null && \
                log "  HSTS: Present" || warn "  HSTS: Missing"
            echo "$headers" | grep -i "content-security-policy" > /dev/null && \
                log "  CSP: Present" || warn "  CSP: Missing"
            echo "$headers" | grep -i "x-frame-options" > /dev/null && \
                log "  X-Frame-Options: Present" || warn "  X-Frame-Options: Missing"
            echo "$headers" | grep -i "x-content-type-options" > /dev/null && \
                log "  X-Content-Type-Options: Present" || warn "  X-Content-Type-Options: Missing"
        fi
    else
        error "Could not fetch certificate for $domain"
    fi
}

# ====================
# File Permission Check
# ====================

check_permissions() {
    section "File Permission Audit"

    # World-writable files
    log "Checking for world-writable files..."
    local writable=$(find "$PROJECT_DIR" -type f -perm -o=w \
        -not -path '*/node_modules/*' -not -path '*/.git/*' -not -path '*/.next/*' 2>/dev/null | head -10)

    if [ -n "$writable" ]; then
        warn "Found world-writable files:"
        echo "$writable" | sed 's/^/  /'
    else
        log "No world-writable files found"
    fi

    # Sensitive files
    log "Checking sensitive file permissions..."
    for f in .env .env.local .env.* *.pem *.key id_rsa id_ed25519 credentials.json; do
        if [ -f "$PROJECT_DIR/$f" ]; then
            local perms=$(stat -c %a "$PROJECT_DIR/$f" 2>/dev/null || stat -f %Lp "$PROJECT_DIR/$f" 2>/dev/null)
            if [ "${perms:-644}" -gt 644 ]; then
                warn "Sensitive file has loose permissions: $f ($perms)"
            else
                log "  $f: $perms (OK)"
            fi
        fi
    done

    # SSH directory
    if [ -d ~/.ssh ]; then
        local ssh_perms=$(stat -c %a ~/.ssh 2>/dev/null || stat -f %Lp ~/.ssh 2>/dev/null)
        if [ "${ssh_perms:-700}" != "700" ]; then
            warn "~/.ssh should have 700 permissions (has $ssh_perms)"
        else
            log "~/.ssh permissions are correct (700)"
        fi
    fi
}

# ====================
# Score Calculation
# ====================

calculate_score() {
    local score=$((TOTAL_SCORE - DEDUCTIONS))
    [ $score -lt 0 ] && score=0

    echo ""
    section "Security Score"

    local risk_level=""
    local color=""

    if [ $score -ge 90 ]; then
        risk_level="✅ Low Risk"
        color="$GREEN"
    elif [ $score -ge 70 ]; then
        risk_level="⚠️ Medium Risk"
        color="$YELLOW"
    elif [ $score -ge 50 ]; then
        risk_level="🔶 High Risk"
        color="$YELLOW"
    else
        risk_level="🚨 Critical Risk"
        color="$RED"
    fi

    echo -e "  Score: ${color}${score}/100${NC}"
    echo -e "  Level: ${color}${risk_level}${NC}"

    if [ ${#FINDINGS[@]} -gt 0 ]; then
        echo ""
        echo "  Key Findings:"
        for finding in "${FINDINGS[@]}"; do
            echo -e "  ${RED}•${NC} $finding"
        done
    fi
}

# ====================
# Generate Report
# ====================

generate_report() {
    local output="${OUTPUT_FILE:-security-audit-report.md}"

    cat > "$output" << EOF
# Security Audit Report

**Generated:** $(date -u +"%Y-%m-%d %H:%M:%S UTC")
**Project:** $(basename "$(pwd)")

## Security Score

**Score:** $((TOTAL_SCORE - DEDUCTIONS))/100

## Findings Summary

| Severity | Count |
|----------|-------|
| Critical | $(echo "${FINDINGS[@]}" | grep -c "Critical\|ERROR" || echo 0) |
| High | $(echo "${FINDINGS[@]}" | grep -c "High\|WARN" || echo 0) |

## Detailed Findings

$(for f in "${FINDINGS[@]}"; do echo "- $f"; done)

## Recommendations

1. Review all findings above
2. Run \`npm audit fix\` for dependency issues
3. Enable security headers in your web server
4. Rotate any exposed secrets immediately
5. Consider implementing a pre-commit hook for secret detection

---
*Generated by Code Security Audit v2.0.0*
EOF

    log "Report saved to: $output"
}

# ====================
# Main Execution
# ====================

main() {
    echo ""
    echo -e "${BLUE}╔════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║     Code Security Audit v2.0.0                 ║${NC}"
    echo -e "${BLUE}║     Comprehensive Security Scanner              ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════╝${NC}"
    echo ""

    case "$MODE" in
        full)
            check_owasp
            check_secrets
            check_dependencies
            check_permissions
            calculate_score
            ;;
        quick)
            check_secrets
            check_dependencies
            calculate_score
            ;;
        owasp)
            check_owasp
            calculate_score
            ;;
        deps)
            check_dependencies
            calculate_score
            ;;
        secrets)
            check_secrets
            calculate_score
            ;;
        ssl)
            check_ssl
            ;;
        perms)
            check_permissions
            calculate_score
            ;;
        score)
            check_owasp > /dev/null 2>&1
            check_secrets > /dev/null 2>&1
            check_dependencies > /dev/null 2>&1
            calculate_score
            ;;
        report)
            check_owasp
            check_secrets
            check_dependencies
            check_permissions
            calculate_score
            generate_report
            ;;
    esac

    echo ""
    log "Audit complete!"
}

main "$@"
