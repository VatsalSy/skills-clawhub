#!/bin/bash
# Auto-refresh Claude Code OAuth token using Claude CLI

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(dirname "$SCRIPT_DIR")"
TOKEN_FILE="$BASE_DIR/.tokens"

echo "🔄 Auto-refreshing Claude Code OAuth token..."

# Check if claude CLI is available
if ! command -v claude >/dev/null 2>&1; then
  echo "⚠️  Claude CLI not found. Install it or run manual refresh." >&2
  exit 1
fi

# Trigger a simple query to force token refresh if needed
# Claude CLI automatically refreshes expired tokens
echo "ping" | claude --quiet >/dev/null 2>&1

# Check if refresh was successful
if [ -f ~/.claude/.credentials.json ]; then
  # Extract fresh tokens
  NEW_ACCESS=$(python3 -c "import json; d=json.load(open('$HOME/.claude/.credentials.json')); print(d.get('claudeAiOauth', {}).get('accessToken', ''))" 2>/dev/null)
  NEW_REFRESH=$(python3 -c "import json; d=json.load(open('$HOME/.claude/.credentials.json')); print(d.get('claudeAiOauth', {}).get('refreshToken', ''))" 2>/dev/null)
  
  if [ -n "$NEW_ACCESS" ] && [ -n "$NEW_REFRESH" ]; then
    # Update .tokens file for consistency
    if [ -f "$TOKEN_FILE" ]; then
      cat > "$TOKEN_FILE" <<EOF
# Claude Code OAuth Tokens
# Auto-refreshed: $(date -u +"%Y-%m-%d %H:%M UTC")

ACCESS_TOKEN="$NEW_ACCESS"
REFRESH_TOKEN="$NEW_REFRESH"
EOF
      chmod 600 "$TOKEN_FILE"
      echo "✅ Token refreshed successfully via Claude CLI!"
      echo "📝 Updated $TOKEN_FILE"
      exit 0
    fi
  fi
fi

echo "⚠️  Token refresh failed or Claude CLI not authenticated."
echo "📋 Run: claude auth login"
exit 1
