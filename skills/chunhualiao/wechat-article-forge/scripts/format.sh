#!/usr/bin/env bash
# format.sh — Deterministic formatting pipeline (steps 7-8)
# Usage: bash format.sh <draft-dir> [draft-file]
# Example: bash format.sh ~/.wechat-article-writer/drafts/my-article-20260220 draft-v3.md
set -euo pipefail

DRAFT_DIR="${1:?Usage: format.sh <draft-dir> [draft-file]}"
DRAFT_FILE="${2:-draft.md}"
DRAFT_PATH="$DRAFT_DIR/$DRAFT_FILE"
RAW_HTML="$DRAFT_DIR/raw.html"
FORMATTED="$DRAFT_DIR/formatted.html"

# Verify draft exists
if [[ ! -f "$DRAFT_PATH" ]]; then
  echo "ERROR: Draft not found: $DRAFT_PATH" >&2
  exit 1
fi

# Step 7: wenyan render (reads from stdin)
echo "▸ Rendering markdown → WeChat HTML..."
if ! command -v wenyan &>/dev/null; then
  echo "ERROR: wenyan-cli not found. Install: pnpm add -g @wenyan-md/cli" >&2
  exit 1
fi
cat "$DRAFT_PATH" | wenyan render > "$RAW_HTML"
echo "  ✓ raw.html ($(wc -c < "$RAW_HTML") bytes)"

# Step 8: Post-process
echo "▸ Post-processing HTML..."
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S %Z')

{
  # Charset (required — without it browser shows garbled Chinese)
  echo '<meta charset="utf-8">'
  # Preview timestamp banner for cache-busting
  echo "<div style=\"background:#fff3cd;padding:8px 12px;font-size:12px;color:#856404;border-bottom:1px solid #ffc107;text-align:center;\">Preview build: $TIMESTAMP</div>"
  # Original wenyan output
  cat "$RAW_HTML"
} > "$FORMATTED"

echo "  ✓ formatted.html ($(wc -c < "$FORMATTED") bytes)"
echo "✅ Format complete: $FORMATTED"
