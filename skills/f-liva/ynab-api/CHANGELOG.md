# Changelog

## v1.0.0 - 2026-02-21

### Initial Release

**Features:**
- Smart categorization based on transaction history
- Duplicate detection for pending transactions
- Monthly spending reports with proper exclusions
- Split transaction handling
- Milliunits handling for YNAB API
- Helper script for common operations

**Documentation:**
- Complete SKILL.md with best practices
- Category examples and best practices guide
- README with setup instructions
- Example configurations

**Best Practices Implemented:**
1. Always categorize immediately
2. Check transaction history for unknown merchants
3. Detect duplicate pending transactions
4. Proper milliunits conversion (amount * 1000)
5. Monthly expense calculation with exclusions
6. Transfer payee format standardization

**Security:**
- No hardcoded credentials
- Config file with secure permissions
- No logging of sensitive data
