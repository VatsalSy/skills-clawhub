#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3}"
INTERVAL_MIN="${INTERVAL_MIN:-5}"
CRON_CMD="*/${INTERVAL_MIN} * * * * cd ${REPO_ROOT} && ${PYTHON_BIN} scripts/task_tick_all.py >/dev/null 2>&1"

usage() {
  cat <<EOF
Install or print a cron entry for recurring durable-task status ticks.

Environment overrides:
  PYTHON_BIN     Python executable (default: python3)
  INTERVAL_MIN   Tick interval in minutes (default: 5)

Usage:
  $0 --print   Print the cron entry only
  $0 --apply   Install/update the cron entry for the current user
EOF
}

case "${1:-}" in
  --print)
    printf '%s\n' "$CRON_CMD"
    ;;
  --apply)
    current="$(crontab -l 2>/dev/null || true)"
    filtered="$(printf '%s\n' "$current" | grep -Fv 'scripts/task_tick_all.py' || true)"
    {
      printf '%s\n' "$filtered"
      printf '%s\n' "$CRON_CMD"
    } | sed '/^$/N;/^\n$/D' | crontab -
    echo "Installed cron entry: $CRON_CMD"
    ;;
  *)
    usage
    exit 2
    ;;
esac
