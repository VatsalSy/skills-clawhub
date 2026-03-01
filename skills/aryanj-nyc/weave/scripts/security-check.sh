#!/usr/bin/env bash
set -euo pipefail

print_usage() {
  cat <<'EOF'
Usage:
  bash skills/weave/scripts/security-check.sh [skill_dir]

Defaults:
  skill_dir = skills/weave

Purpose:
  Run a pre-publish security lint for patterns that frequently trigger
  Clawhub suspicious flags.
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  print_usage
  exit 0
fi

skill_dir="${1:-skills/weave}"
skill_md="${skill_dir}/SKILL.md"

if [[ ! -d "${skill_dir}" ]]; then
  echo "Error: skill directory not found: ${skill_dir}" >&2
  exit 1
fi

if [[ ! -f "${skill_md}" ]]; then
  echo "Error: SKILL.md not found: ${skill_md}" >&2
  exit 1
fi

failures=0

fail_match() {
  local label="$1"
  local pattern="$2"
  if rg -n --pcre2 "${pattern}" "${skill_dir}" >/tmp/weave-security-check.out 2>/dev/null; then
    echo "FAIL: ${label}" >&2
    cat /tmp/weave-security-check.out >&2
    echo >&2
    failures=$((failures + 1))
  fi
}

echo "Running security checks in ${skill_dir}..."

# Build regex fragments without embedding common suspicious one-liners as plain text.
downloader='(c'"'"'url|w'"'"'get)'
shell_target='(ba'"'"'sh|sh)'
pipe_to_shell_regex="^\\s*${downloader}[^\\n]*\\|\\s*${shell_target}\\b"
base64_pipe_regex="^\\s*base64[^\\n]*\\|\\s*${shell_target}\\b"

fail_match "Detected pipe-to-shell installer pattern." "${pipe_to_shell_regex}"
fail_match "Detected base64 decode piped to shell." "${base64_pipe_regex}"
fail_match "Detected URL shortener usage." '(bit\.ly|tinyurl\.com|t\.co/|goo\.gl|is\.gd)'

if rg -n --pcre2 '^\s*-?\s*kind:\s*(?!brew|node|go|uv)\w+' "${skill_md}" >/tmp/weave-security-check.out 2>/dev/null; then
  echo "FAIL: Detected unsupported install kind (allowed: brew|node|go|uv)." >&2
  cat /tmp/weave-security-check.out >&2
  echo >&2
  failures=$((failures + 1))
fi

if ! rg -q --pcre2 '^\s*-?\s*kind:\s*(brew|node|go|uv)\b' "${skill_md}"; then
  echo "FAIL: No compliant install section found in SKILL.md frontmatter." >&2
  failures=$((failures + 1))
fi

if [[ ${failures} -gt 0 ]]; then
  echo "Security check failed with ${failures} issue(s)." >&2
  exit 1
fi

echo "PASS: security checks completed with no blocking findings."
