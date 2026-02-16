#!/bin/bash
# Push dashboard state to Supabase for realtime updates
# 
# Usage:
#   ./push-dashboard.sh '{"actionRequired": [...], "activeNow": [...], ...}'
#   cat dashboard-data.json | ./push-dashboard.sh
#
# Environment variables required:
#   SUPABASE_URL         - Your Supabase project URL
#   SUPABASE_SERVICE_KEY - Service role key (NOT anon key!)
#
# Security note: The service_role key has full database access.
# Keep it secret. Never put it in client-side code.

set -e

# Check required env vars
if [ -z "$SUPABASE_URL" ]; then
    echo "Error: SUPABASE_URL environment variable is not set" >&2
    echo "Set it with: export SUPABASE_URL='https://your-project.supabase.co'" >&2
    exit 1
fi

if [ -z "$SUPABASE_SERVICE_KEY" ]; then
    echo "Error: SUPABASE_SERVICE_KEY environment variable is not set" >&2
    echo "Set it with: export SUPABASE_SERVICE_KEY='your-service-role-key'" >&2
    exit 1
fi

# Read data from argument or stdin
DATA="${1:-$(cat -)}"

# Validate JSON
if ! echo "$DATA" | jq . > /dev/null 2>&1; then
    echo "Error: Invalid JSON input" >&2
    exit 1
fi

# Get current timestamp
TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)

# Update the dashboard_state table
RESPONSE=$(curl -s -w "\n%{http_code}" -X PATCH \
    "$SUPABASE_URL/rest/v1/dashboard_state?id=eq.main" \
    -H "apikey: $SUPABASE_SERVICE_KEY" \
    -H "Authorization: Bearer $SUPABASE_SERVICE_KEY" \
    -H "Content-Type: application/json" \
    -H "Prefer: return=minimal" \
    -d "{\"data\": $DATA, \"updated_at\": \"$TIMESTAMP\"}")

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" -ge 200 ] && [ "$HTTP_CODE" -lt 300 ]; then
    echo "✅ Dashboard updated successfully at $TIMESTAMP"
    exit 0
else
    echo "❌ Failed to update dashboard (HTTP $HTTP_CODE)" >&2
    [ -n "$BODY" ] && echo "$BODY" >&2
    exit 1
fi
