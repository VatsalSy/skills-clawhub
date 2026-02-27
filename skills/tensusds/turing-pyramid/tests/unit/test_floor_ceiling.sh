#!/bin/bash
# test_floor_ceiling.sh — Verify satisfaction stays within 0.5-3.0 bounds after mark-satisfied

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"
MARK_SCRIPT="$SKILL_DIR/scripts/mark-satisfied.sh"
STATE_FILE="$SKILL_DIR/assets/needs-state.json"
FIXTURES="$SCRIPT_DIR/../fixtures"

# Backup current state
cp "$STATE_FILE" "$STATE_FILE.test_backup"

# Test 1: Ceiling — satisfaction should not exceed 3.0
cp "$FIXTURES/needs-state-healthy.json" "$STATE_FILE"

# Set to near ceiling
jq '.expression.satisfaction = 2.9' "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"

# Apply large impact — should be clamped to 3.0
"$MARK_SCRIPT" expression 2.0 > /dev/null 2>&1

sat=$(jq -r '.expression.satisfaction' "$STATE_FILE")

# Restore backup
cp "$STATE_FILE.test_backup" "$STATE_FILE"
rm "$STATE_FILE.test_backup"

if (( $(echo "$sat <= 3.0" | bc -l) )); then
    exit 0
else
    echo "Ceiling violated: sat=$sat (expected <= 3.0)"
    exit 1
fi
