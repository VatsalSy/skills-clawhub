#!/bin/bash
# OpenClaw Callback - Send callback via OpenClaw system event

set -euo pipefail

# Default values
STATUS="done"
MODE="single"
TASK=""
MESSAGE=""
OUTPUT=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --status)
            STATUS="$2"
            shift 2
            ;;
        --mode)
            MODE="$2"
            shift 2
            ;;
        --task)
            TASK="$2"
            shift 2
            ;;
        --message)
            MESSAGE="$2"
            shift 2
            ;;
        --output)
            OUTPUT="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Build message
if [[ -n "$MESSAGE" ]]; then
    MSG="fast-claude-code:$STATUS | mode=$MODE | task=$TASK | msg=$MESSAGE"
else
    MSG="fast-claude-code:$STATUS | mode=$MODE | task=$TASK"
fi

# Append output if provided
if [[ -n "$OUTPUT" ]]; then
    MSG="$MSG

--- Response ---
${OUTPUT}"
fi

# Check if openclaw is available
if command -v openclaw &> /dev/null; then
    openclaw system event --text "$MSG" --mode now
else
    echo "Warning: openclaw not found, using echo instead"
    echo "$MSG"
fi
