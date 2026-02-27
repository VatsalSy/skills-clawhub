#!/bin/bash
# test_full_cycle.sh — Verify run-cycle.sh produces valid output

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"
RUN_CYCLE="$SKILL_DIR/scripts/run-cycle.sh"
STATE_FILE="$SKILL_DIR/assets/needs-state.json"
FIXTURES="$SCRIPT_DIR/../fixtures"

# Backup current state
cp "$STATE_FILE" "$STATE_FILE.test_backup"

# Use healthy fixture
cp "$FIXTURES/needs-state-healthy.json" "$STATE_FILE"

# Run cycle and capture output
output=$("$RUN_CYCLE" 2>&1)

# Restore backup
cp "$STATE_FILE.test_backup" "$STATE_FILE"
rm "$STATE_FILE.test_backup"

# Verify output contains expected sections
errors=0

if ! echo "$output" | grep -q "Turing Pyramid"; then
    echo "Missing header"
    ((errors++))
fi

if ! echo "$output" | grep -q "Current tensions:"; then
    echo "Missing tensions section"
    ((errors++))
fi

if ! echo "$output" | grep -q "Summary:"; then
    echo "Missing summary"
    ((errors++))
fi

# Verify at least one need is listed
if ! echo "$output" | grep -qE "^\s+(security|integrity|coherence|closure|autonomy|connection|competence|understanding|recognition|expression):"; then
    echo "No needs listed in output"
    ((errors++))
fi

if [[ $errors -eq 0 ]]; then
    exit 0
else
    echo "Errors found: $errors"
    exit 1
fi
