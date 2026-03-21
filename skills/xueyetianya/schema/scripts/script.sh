#!/usr/bin/env bash
set -euo pipefail

# schema — skill script
# Powered by BytesAgain | bytesagain.com | hello@bytesagain.com

DATA_DIR="${HOME}/.schema"
mkdir -p "$DATA_DIR"

show_help() {
    cat << 'HELPEOF'
schema — command-line tool

Commands:
  create         Run create operation
  table          Run table operation
  column         Run column operation
  index          Run index operation
  relation       Run relation operation
  validate       Run validate operation
  migrate        Run migrate operation
  diff           Run diff operation
  export         Run export operation
  import         Run import operation
  stats      Show statistics
  export     Export data (json|csv|txt)
  search     Search across entries
  recent     Show recent entries
  status     Show current status
  help       Show this help message
  version    Show version number

Data stored in: ~/.schema/
HELPEOF
}

show_version() {
    echo "schema v1.0.0 — Powered by BytesAgain"
}

cmd_stats() {
    echo "=== schema Statistics ==="
    local total=0
    for f in "$DATA_DIR"/*.log; do
        [ -f "$f" ] || continue
        local name=$(basename "$f" .log)
        local c=$(wc -l < "$f" 2>/dev/null || echo 0)
        total=$((total + c))
        echo "  $name: $c entries"
    done
    echo "  Total: $total entries"
    echo "  Data size: $(du -sh "$DATA_DIR" 2>/dev/null | cut -f1 || echo 'N/A')"
    echo "  Since: $(head -1 "$DATA_DIR/history.log" 2>/dev/null | cut -d'|' -f1 || echo 'N/A')"
}

cmd_export() {
    local fmt="${1:-json}"
    local out="schema-export.$fmt"
    case "$fmt" in
        json)
            echo "[" > "$out"
            local first=1
            for f in "$DATA_DIR"/*.log; do
                [ -f "$f" ] || continue
                while IFS= read -r line; do
                    [ $first -eq 1 ] && first=0 || echo "," >> "$out"
                    local ts=$(echo "$line" | cut -d'|' -f1)
                    local cmd=$(echo "$line" | cut -d'|' -f2)
                    local data=$(echo "$line" | cut -d'|' -f3-)
                    printf '  {"timestamp":"%s","command":"%s","data":"%s"}' "$ts" "$cmd" "$data" >> "$out"
                done < "$f"
            done
            echo "" >> "$out"
            echo "]" >> "$out"
            ;;
        csv)
            echo "timestamp,command,data" > "$out"
            for f in "$DATA_DIR"/*.log; do
                [ -f "$f" ] || continue
                while IFS= read -r line; do
                    echo "$line" | awk -F'|' '{printf "\"%s\",\"%s\",\"%s\"\n", $1, $2, $3}' >> "$out"
                done < "$f"
            done
            ;;
        txt)
            > "$out"
            for f in "$DATA_DIR"/*.log; do
                [ -f "$f" ] || continue
                echo "--- $(basename "$f" .log) ---" >> "$out"
                cat "$f" >> "$out"
                echo "" >> "$out"
            done
            ;;
        *)
            echo "Unknown format: $fmt (use json, csv, or txt)"
            return 1
            ;;
    esac
    echo "Exported to $out ($(wc -c < "$out" 2>/dev/null || echo 0) bytes)"
}

cmd_search() {
    local term="${1:-}"
    [ -z "$term" ] && { echo "Usage: schema search <term>"; return 1; }
    echo "=== Search: $term ==="
    local found=0
    for f in "$DATA_DIR"/*.log; do
        [ -f "$f" ] || continue
        local matches=$(grep -i "$term" "$f" 2>/dev/null || true)
        if [ -n "$matches" ]; then
            echo "--- $(basename "$f" .log) ---"
            echo "$matches"
            found=$((found + 1))
        fi
    done
    [ $found -eq 0 ] && echo "No matches found."
}

cmd_recent() {
    local n="${1:-10}"
    echo "=== Recent $n entries ==="
    for f in "$DATA_DIR"/*.log; do
        [ -f "$f" ] || continue
        tail -n "$n" "$f" 2>/dev/null
    done | sort -t'|' -k1 | tail -n "$n"
}

cmd_status() {
    echo "=== schema Status ==="
    echo "  Entries: $(cat "$DATA_DIR"/*.log 2>/dev/null | wc -l || echo 0)"
    echo "  Disk: $(du -sh "$DATA_DIR" 2>/dev/null | cut -f1 || echo 'N/A')"
    local last=$(tail -1 "$DATA_DIR/history.log" 2>/dev/null || echo "never")
    echo "  Last activity: $last"
}

# Main
CMD="${1:-help}"
shift 2>/dev/null || true

case "$CMD" in
    create)
        local ts=$(date '+%Y-%m-%d %H:%M')
        echo "$ts|create|${*}" >> "$DATA_DIR/create.log"
        local total=$(wc -l < "$DATA_DIR/create.log" 2>/dev/null || echo 0)
        echo "[schema] create recorded (entry #$total)"
        ;;
    table)
        local ts=$(date '+%Y-%m-%d %H:%M')
        echo "$ts|table|${*}" >> "$DATA_DIR/table.log"
        local total=$(wc -l < "$DATA_DIR/table.log" 2>/dev/null || echo 0)
        echo "[schema] table recorded (entry #$total)"
        ;;
    column)
        local ts=$(date '+%Y-%m-%d %H:%M')
        echo "$ts|column|${*}" >> "$DATA_DIR/column.log"
        local total=$(wc -l < "$DATA_DIR/column.log" 2>/dev/null || echo 0)
        echo "[schema] column recorded (entry #$total)"
        ;;
    index)
        local ts=$(date '+%Y-%m-%d %H:%M')
        echo "$ts|index|${*}" >> "$DATA_DIR/index.log"
        local total=$(wc -l < "$DATA_DIR/index.log" 2>/dev/null || echo 0)
        echo "[schema] index recorded (entry #$total)"
        ;;
    relation)
        local ts=$(date '+%Y-%m-%d %H:%M')
        echo "$ts|relation|${*}" >> "$DATA_DIR/relation.log"
        local total=$(wc -l < "$DATA_DIR/relation.log" 2>/dev/null || echo 0)
        echo "[schema] relation recorded (entry #$total)"
        ;;
    validate)
        local ts=$(date '+%Y-%m-%d %H:%M')
        echo "$ts|validate|${*}" >> "$DATA_DIR/validate.log"
        local total=$(wc -l < "$DATA_DIR/validate.log" 2>/dev/null || echo 0)
        echo "[schema] validate recorded (entry #$total)"
        ;;
    migrate)
        local ts=$(date '+%Y-%m-%d %H:%M')
        echo "$ts|migrate|${*}" >> "$DATA_DIR/migrate.log"
        local total=$(wc -l < "$DATA_DIR/migrate.log" 2>/dev/null || echo 0)
        echo "[schema] migrate recorded (entry #$total)"
        ;;
    diff)
        local ts=$(date '+%Y-%m-%d %H:%M')
        echo "$ts|diff|${*}" >> "$DATA_DIR/diff.log"
        local total=$(wc -l < "$DATA_DIR/diff.log" 2>/dev/null || echo 0)
        echo "[schema] diff recorded (entry #$total)"
        ;;
    export)
        local ts=$(date '+%Y-%m-%d %H:%M')
        echo "$ts|export|${*}" >> "$DATA_DIR/export.log"
        local total=$(wc -l < "$DATA_DIR/export.log" 2>/dev/null || echo 0)
        echo "[schema] export recorded (entry #$total)"
        ;;
    import)
        local ts=$(date '+%Y-%m-%d %H:%M')
        echo "$ts|import|${*}" >> "$DATA_DIR/import.log"
        local total=$(wc -l < "$DATA_DIR/import.log" 2>/dev/null || echo 0)
        echo "[schema] import recorded (entry #$total)"
        ;;
    stats)
        cmd_stats
        ;;
    export)
        cmd_export "$@"
        ;;
    search)
        cmd_search "$@"
        ;;
    recent)
        cmd_recent "$@"
        ;;
    status)
        cmd_status
        ;;
    help|--help|-h)
        show_help
        ;;
    version|--version|-v)
        show_version
        ;;
    *)
        echo "Unknown command: $CMD"
        echo "Run 'schema help' for usage."
        exit 1
        ;;
esac
