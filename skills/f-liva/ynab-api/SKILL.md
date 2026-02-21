---
name: ynab-api
description: YNAB (You Need A Budget) financial tracking and categorization best practices. Use when managing budget transactions, categorizing expenses, or querying financial data via YNAB API.
user-invocable: true
metadata: {"clawdbot":{"emoji":"💰","requires":{"env":["YNAB_API_KEY","YNAB_BUDGET_ID"]}}}
---

# YNAB Budget Management

This skill provides best practices for managing YNAB budgets via API, including transaction categorization, data consistency, and common workflows.

## Configuration

Required environment variables or config file (`~/.config/ynab/config.json`):
- `YNAB_API_KEY` - Your YNAB Personal Access Token
- `YNAB_BUDGET_ID` - Your budget ID (get from YNAB API or URL)

## Core Best Practices

### 1. Always Categorize Immediately

**Never** create transactions without a category. Uncategorized transactions break budget tracking.

When adding a transaction, categorize it at creation time—don't defer.

### 2. Check Transaction History for Unknown Merchants

When you encounter an unfamiliar merchant/payee:

1. Search YNAB for past transactions with the same payee name
2. Use the same category as previous transactions
3. Maintain consistency with historical categorization

**Why**: This preserves categorization consistency and reduces user interruptions.

Example:
```bash
# Search for past transactions by payee
curl -s "https://api.ynab.com/v1/budgets/$BUDGET_ID/transactions" \
  -H "Authorization: Bearer $API_KEY" | \
  jq '.data.transactions[] | select(.payee_name | contains("MERCHANT_NAME"))'
```

### 3. Check for Pending Transactions Before Adding

Before creating a new transaction:
1. Check if an unapproved transaction already exists for the same amount
2. If found → approve it and update payee/memo if needed
3. If not found → create new transaction

**Why**: Avoids duplicates from imported bank transactions.

### 4. Use Milliunits for Amounts

YNAB API uses **milliunits** for all amounts:
- €10.00 = `10000` (positive for income)
- -€10.00 = `-10000` (negative for expenses)

**Always** divide by 1000 when displaying, multiply by 1000 when submitting.

### 5. Monthly Expense Calculation

When calculating monthly spending:
- Only count transactions with `amount < 0` (actual expenses)
- Consider excluding non-discretionary categories like:
  - Tax payments (mandatory, not spending choices)
  - Advances/reimbursements (temporary, not true expenses)
  - Uncategorized (often transfers/investments)
  - Extraordinary one-time expenses (if tracking discretionary budget)

**Note**: Exclusion rules depend on your budget goals. Configure your specific exclusions in a local config or notes file.

### 6. Handle Split Transactions

Transactions with category "Split" contain `subtransactions`.

**Never** show "Split" as a category in reports—always expand to subcategories:

```bash
# For each split transaction
if [ "$category_name" = "Split" ]; then
  for subtx in subtransactions; do
    echo "$subtx.category_name: $subtx.amount"
  done
fi
```

### 7. Transfer Payee Format

When recording transfers between accounts, use standardized payee names for consistency:
- `Transfer: To [Account Name]` (outbound)
- `Transfer: From [Account Name]` (inbound)

This makes transfers easy to identify and filter in reports.

## Common Account IDs Structure

Store account IDs in config (example structure):
```json
{
  "accounts": {
    "primary_checking": "UUID-HERE",
    "savings": "UUID-HERE",
    "cash": "UUID-HERE"
  },
  "default_account": "primary_checking"
}
```

**Never** hardcode account IDs in scripts—use config references.

## Common Operations

### Add Transaction

```bash
YNAB_API="https://api.ynab.com/v1"

curl -X POST "$YNAB_API/budgets/$BUDGET_ID/transactions" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"transaction\": {
      \"account_id\": \"$ACCOUNT_ID\",
      \"date\": \"2026-02-21\",
      \"amount\": -10000,
      \"payee_name\": \"Coffee Shop\",
      \"category_id\": \"$CATEGORY_ID\",
      \"memo\": \"Morning coffee\",
      \"approved\": true
    }
  }"
```

### Search Transactions

```bash
# Get transactions since date
curl "$YNAB_API/budgets/$BUDGET_ID/transactions?since_date=2026-02-01" \
  -H "Authorization: Bearer $API_KEY"

# Filter by payee (client-side with jq)
... | jq '.data.transactions[] | select(.payee_name | contains("Coffee"))'
```

### Get Categories

```bash
curl "$YNAB_API/budgets/$BUDGET_ID/categories" \
  -H "Authorization: Bearer $API_KEY" | \
  jq '.data.category_groups[].categories[] | {id, name}'
```

## Monthly Spending Report

To calculate monthly spending:

1. Get all transactions for the month
2. Filter: `amount < 0` (expenses only)
3. Exclude configured non-discretionary categories (taxes, transfers, etc.)
4. Expand Split transactions into subcategories
5. Sum by category or total

**Tip**: Consider separating small recurring expenses from large one-time purchases for better budget analysis.

## Personal Configuration

For personal preferences (merchant mappings, category exclusions, default accounts):

**Option 1**: Add to your workspace `TOOLS.md`:
```markdown
## YNAB Personal Config
- Default account: [account_id]
- Exclude from budget: Category1, Category2
- Merchant mappings: Store → Category
```

**Option 2**: Create local config file (e.g., `~/.config/ynab/rules.json`):
```json
{
  "exclude_categories": ["Taxes", "Transfers"],
  "merchant_map": {
    "Coffee Shop": "category_id_here"
  }
}
```

The skill will check transaction history for consistency—your personal preferences stay private.

## Security Notes

- **Never** commit API keys to version control
- Store `YNAB_API_KEY` in environment or secure config (`~/.config/ynab/config.json` with 600 permissions)
- **Never** log or display full API keys in output

## API Documentation

Official YNAB API docs: https://api.ynab.com

Rate limit: ~200 requests per hour per IP.

## Troubleshooting

**401 Unauthorized**: API key invalid or expired
**404 Not Found**: Budget ID or transaction ID doesn't exist
**429 Too Many Requests**: Rate limit exceeded, wait and retry

**Common mistakes**:
- Forgetting milliunits (using 10 instead of 10000)
- Wrong date format (use YYYY-MM-DD)
- Missing required fields (account_id, date, amount)
