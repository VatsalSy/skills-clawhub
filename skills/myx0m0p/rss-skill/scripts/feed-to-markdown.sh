#!/usr/bin/env bash
set -euo pipefail

SCRIPT_NAME="$(basename "$0")"
readonly SCRIPT_NAME
readonly NPX_PACKAGE="feed2md-cli"

usage() {
  cat >&2 <<EOF
Usage:
  $SCRIPT_NAME <feed_url> [output_file]
  $SCRIPT_NAME [--output <file>] <feed_url> [feed2md options...]

Examples:
  $SCRIPT_NAME "https://example.com/feed.xml"
  $SCRIPT_NAME "https://example.com/feed.xml" output.md
  $SCRIPT_NAME --output output.md "https://example.com/feed.xml" --limit 10 --template full
EOF
}

die() {
  echo "Error: $*" >&2
  exit 1
}

if [[ $# -eq 0 ]]; then
  usage
  exit 1
fi

feed_url=""
output_file=""
declare -a extra_args=()

# Backward-compatible mode:
#   script <feed_url> [output_file]
if [[ $# -le 2 && "${1:-}" != -* ]]; then
  feed_url="$1"
  output_file="${2:-}"
else
  while (($# > 0)); do
    case "$1" in
      -h|--help)
        usage
        exit 0
        ;;
      -o|--output)
        [[ $# -ge 2 ]] || die "Missing value for $1"
        output_file="$2"
        shift 2
        ;;
      --)
        shift
        extra_args+=("$@")
        break
        ;;
      -*)
        extra_args+=("$1")
        shift
        ;;
      *)
        if [[ -z "$feed_url" && "$1" =~ ^https?:// ]]; then
          feed_url="$1"
        else
          extra_args+=("$1")
        fi
        shift
        ;;
    esac
  done
fi

[[ -n "$feed_url" ]] || die "Feed URL is required."
[[ "$feed_url" =~ ^https?:// ]] || die "Feed URL must start with http:// or https://"

declare -a cmd=()
if command -v feed2md >/dev/null 2>&1; then
  cmd=(feed2md "$feed_url")
elif command -v npx >/dev/null 2>&1; then
  cmd=(npx -y "$NPX_PACKAGE" "$feed_url")
else
  die "Neither 'feed2md' nor 'npx' is available. Install Node.js and run: npm install -g $NPX_PACKAGE"
fi

if [[ -n "$output_file" ]]; then
  cmd+=(--output "$output_file")
fi
cmd+=("${extra_args[@]}")

exec "${cmd[@]}"
