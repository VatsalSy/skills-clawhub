# YNAB Budget Management Skill

A comprehensive skill for managing YNAB (You Need A Budget) budgets via API, including transaction categorization best practices, consistency checks, and common financial workflows.

## Features

- ✅ **Smart Categorization**: Automatically checks past transactions to maintain category consistency
- ✅ **Duplicate Detection**: Prevents duplicate entries by checking for pending transactions
- ✅ **Monthly Reports**: Calculate true discretionary spending with proper exclusions
- ✅ **Split Transaction Handling**: Properly expands split transactions to subcategories
- ✅ **Best Practices**: Learned patterns for accurate financial tracking

## Installation

### Via ClawHub

```bash
clawhub install ynab
```

### Manual Installation

```bash
git clone <repo-url> ~/.openclaw/skills/ynab
```

## Configuration

Create a config file at `~/.config/ynab/config.json`:

```json
{
  "api_key": "YOUR_YNAB_PERSONAL_ACCESS_TOKEN",
  "budget_id": "YOUR_BUDGET_UUID",
  "default_account_id": "YOUR_PRIMARY_ACCOUNT_UUID"
}
```

### Getting Your YNAB Credentials

1. **API Key**: Go to https://app.ynab.com/settings/developer → Generate New Token
2. **Budget ID**: Open your budget in YNAB web app, copy UUID from URL: `https://app.ynab.com/{BUDGET_ID}/...`
3. **Account ID**: Use the helper script: `./scripts/ynab-helper.sh list-categories`

Set secure permissions:
```bash
chmod 600 ~/.config/ynab/config.json
```

## Usage

### With Claude/OpenClaw

The skill activates automatically when you:
- Ask about budget transactions
- Need to categorize expenses
- Want monthly spending reports
- Query financial data

Examples:
- "Add a €25 coffee shop transaction to my budget"
- "What did I spend on groceries this month?"
- "Categorize this expense based on past transactions"

### Command-Line Helper Script

```bash
# Search past transactions by merchant
./scripts/ynab-helper.sh search-payee "Coffee"

# List all categories with IDs
./scripts/ynab-helper.sh list-categories

# Get spending for current month
./scripts/ynab-helper.sh month-spending

# Get spending for specific month
./scripts/ynab-helper.sh month-spending 2026-01

# Add transaction interactively
./scripts/ynab-helper.sh add-transaction
```

## Best Practices Included

1. **Always categorize immediately** - Never leave transactions uncategorized
2. **Check transaction history** - Maintain consistency with past categorizations
3. **Detect duplicates** - Check for pending transactions before adding new ones
4. **Use milliunits** - Remember YNAB uses milliunits (€10 = 10000)
5. **Exclude non-discretionary** - Proper monthly spending calculation excludes taxes, advances, etc.
6. **Handle splits** - Expand split transactions to show actual subcategories

## Category Reference

The skill includes a reference guide with category examples and best practices. See `references/category-examples.md` for:
- Common category structures
- Merchant-to-category mapping guidelines
- Split transaction examples
- Exclusion strategies for budget calculations

## Security

- ⚠️ **Never commit** your API key to version control
- 🔒 Store credentials in `~/.config/ynab/config.json` with 600 permissions
- 🚫 The skill **never logs** or displays full API keys

## API Rate Limits

YNAB API limit: ~200 requests/hour per IP.

The skill caches category lookups and minimizes API calls where possible.

## Troubleshooting

**401 Unauthorized**: Check your API key in config file
**404 Not Found**: Verify budget_id and account_id are correct
**Transaction not appearing**: Check if it's pending approval (unapproved)

## Contributing

Improvements welcome! Common additions:
- Additional category mappings for different locales
- Budget goal tracking
- Scheduled transaction management
- Multi-currency support

## License

MIT License - See LICENSE file for details

## Resources

- YNAB API Docs: https://api.ynab.com
- YNAB Help: https://support.ynab.com
