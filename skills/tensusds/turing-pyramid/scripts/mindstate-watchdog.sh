#!/bin/bash
# mindstate-watchdog.sh — Process watchdog for mindstate scripts
# Detects hung/dead scripts, cleans up, and restarts.
# Run from cron at lower frequency than daemon (e.g. */15 * * * *).
#
# Strategy:
#   1. Check if daemon has produced output within MAX_STALE minutes
#   2. Find any zombie/hung mindstate processes older than MAX_PROC_AGE
#   3. Kill hung processes, clean up stale locks/tmp files
#   4. Optionally trigger a daemon run to recover immediately
#
# Usage: WORKSPACE=/path/to/workspace mindstate-watchdog.sh [--dry-run]

set -euo pipefail

DRY_RUN=false
[[ "${1:-}" == "--dry-run" ]] && DRY_RUN=true

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/mindstate-utils.sh"

mindstate_validate_workspace || exit 1

MINDSTATE_FILE=$(mindstate_file)
LOCK_FILE=$(mindstate_lock_file)
ASSETS_DIR="$(_ms_assets)"
MS_CONFIG=$(mindstate_ms_config)
WATCHDOG_LOG="$ASSETS_DIR/watchdog.log"

NOW_EPOCH=$(now_epoch)
NOW_ISO=$(now_iso)

# ─── Configuration ───
# Max minutes without MINDSTATE.md update before daemon is considered dead
MAX_STALE_MIN=$(jq -r '.watchdog.max_stale_minutes // 15' "$MS_CONFIG" 2>/dev/null || echo 15)
# Max seconds a mindstate process can run before it's considered hung
MAX_PROC_AGE_SEC=$(jq -r '.watchdog.max_process_age_seconds // 300' "$MS_CONFIG" 2>/dev/null || echo 300)

log() {
    local msg="[$NOW_ISO] $1"
    echo "$msg"
    echo "$msg" >> "$WATCHDOG_LOG"
}

# Rotate watchdog log (keep last 200 lines)
if [[ -f "$WATCHDOG_LOG" ]] && (( $(wc -l < "$WATCHDOG_LOG") > 200 )); then
    tail -100 "$WATCHDOG_LOG" > "$WATCHDOG_LOG.tmp"
    mv "$WATCHDOG_LOG.tmp" "$WATCHDOG_LOG"
fi

# ─── 1. Check MINDSTATE.md freshness ───
daemon_alive=true
if [[ -f "$MINDSTATE_FILE" ]]; then
    last_update=$(stat -c %Y "$MINDSTATE_FILE" 2>/dev/null || echo 0)
    stale_seconds=$((NOW_EPOCH - last_update))
    stale_minutes=$((stale_seconds / 60))
    
    if (( stale_minutes > MAX_STALE_MIN )); then
        daemon_alive=false
        log "WARN: MINDSTATE.md stale for ${stale_minutes}min (threshold: ${MAX_STALE_MIN}min)"
    fi
else
    daemon_alive=false
    log "WARN: MINDSTATE.md does not exist"
fi

# ─── 2. Find hung mindstate processes ───
hung_pids=()
while IFS= read -r line; do
    pid=$(echo "$line" | awk '{print $1}')
    elapsed_str=$(echo "$line" | awk '{print $2}')
    cmd=$(echo "$line" | awk '{$1=$2=""; print $0}' | sed 's/^ *//')
    
    # Parse elapsed time (format: [[dd-]hh:]mm:ss or mm:ss)
    elapsed_sec=0
    if [[ "$elapsed_str" =~ ([0-9]+)-([0-9]+):([0-9]+):([0-9]+) ]]; then
        elapsed_sec=$(( ${BASH_REMATCH[1]}*86400 + ${BASH_REMATCH[2]}*3600 + ${BASH_REMATCH[3]}*60 + ${BASH_REMATCH[4]} ))
    elif [[ "$elapsed_str" =~ ([0-9]+):([0-9]+):([0-9]+) ]]; then
        elapsed_sec=$(( ${BASH_REMATCH[1]}*3600 + ${BASH_REMATCH[2]}*60 + ${BASH_REMATCH[3]} ))
    elif [[ "$elapsed_str" =~ ([0-9]+):([0-9]+) ]]; then
        elapsed_sec=$(( ${BASH_REMATCH[1]}*60 + ${BASH_REMATCH[2]} ))
    fi
    
    if (( elapsed_sec > MAX_PROC_AGE_SEC )); then
        hung_pids+=("$pid")
        log "WARN: Hung process PID=$pid age=${elapsed_sec}s cmd=$cmd"
    fi
done < <(ps -eo pid,etime,args 2>/dev/null | grep -E 'mindstate-(daemon|freeze|boot)\.sh' | grep -v grep | grep -v watchdog || true)

# ─── 3. Kill hung processes ───
if (( ${#hung_pids[@]} > 0 )); then
    for pid in "${hung_pids[@]}"; do
        if $DRY_RUN; then
            log "DRY-RUN: Would kill PID=$pid"
        else
            log "ACTION: Killing hung PID=$pid"
            kill -TERM "$pid" 2>/dev/null || true
            # Wait briefly, then force-kill if still alive
            sleep 2
            if kill -0 "$pid" 2>/dev/null; then
                log "ACTION: Force-killing PID=$pid (SIGKILL)"
                kill -9 "$pid" 2>/dev/null || true
            fi
        fi
    done
fi

# ─── 4. Clean up stale lock if no process holds it ───
if [[ -f "$LOCK_FILE" ]]; then
    # Try to acquire lock non-blocking — if we can, no one holds it
    if ( exec 202>"$LOCK_FILE"; flock -n 202 ) 2>/dev/null; then
        # Lock is free — check if there are stale processes
        if ! pgrep -f 'mindstate-(daemon|freeze)\.sh' >/dev/null 2>&1; then
            # No mindstate process running, lock file is orphaned (safe)
            : # flock files are fine to leave, they're just empty files
        fi
    fi
fi

# ─── 5. Clean up orphaned tmp files ───
orphan_count=$(find "$ASSETS_DIR" "$WORKSPACE" -maxdepth 1 -name "*.tmp.*" -mmin +10 2>/dev/null | wc -l)
if (( orphan_count > 0 )); then
    if $DRY_RUN; then
        log "DRY-RUN: Would clean $orphan_count orphaned .tmp files"
    else
        find "$ASSETS_DIR" "$WORKSPACE" -maxdepth 1 -name "*.tmp.*" -mmin +10 -delete 2>/dev/null || true
        log "ACTION: Cleaned $orphan_count orphaned .tmp files"
    fi
fi

# ─── 6. Restart daemon if stale ───
if ! $daemon_alive; then
    if $DRY_RUN; then
        log "DRY-RUN: Would trigger daemon restart"
    else
        # Wait a moment for any killed processes to fully exit
        sleep 1
        log "ACTION: Triggering daemon run"
        WORKSPACE="$WORKSPACE" bash "$SCRIPT_DIR/mindstate-daemon.sh" &
        daemon_pid=$!
        # Don't wait — let it run in background
        log "ACTION: Daemon restarted (PID=$daemon_pid)"
    fi
fi

# ─── 7. Summary ───
if $daemon_alive && (( ${#hung_pids[@]} == 0 )) && (( orphan_count == 0 )); then
    # All healthy — no log spam
    exit 0
fi

log "SUMMARY: daemon_alive=$daemon_alive hung=${#hung_pids[@]} orphans=$orphan_count"
