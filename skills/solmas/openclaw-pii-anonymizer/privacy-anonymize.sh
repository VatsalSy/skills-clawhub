#!/bin/bash
# OpenClaw PII Anonymizer (Ollama phi3:mini)
# OLLAMA_URL defaults to localhost:11434; override for host (10.0.2.2:11434)

OLLAMA_URL="${OLLAMA_URL:-http://localhost:11434}"
MODEL="phi3:mini"

prompt_anonymize() {
  local input="$1"
  curl -s "$OLLAMA_URL/v1/chat/completions" \
    -H "Content-Type: application/json" \
    -d "{
      \"model\": \"$MODEL\",
      \"messages\": [
        {\"role\": \"system\", \"content\": \"Anonymize PII only: Replace names/emails/paths/IPs/phones/SSNs/URLs/companies with [PERSON], [EMAIL], [PATH], [IP], [PHONE], [SSN], [URL], [ORG]. Keep all else verbatim. No hallucinations, additions, or changes to structure. Output only the cleaned text.\"},
        {\"role\": \"user\", \"content\": \"$input\"}
      ],
      \"stream\": false,
      \"options\": {\"temperature\": 0.1}
    }" | jq -r '.choices[0].message.content // empty' | tr -d '\n\r' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//'
}

if [ $# -eq 0 ]; then
  echo "Usage: $0 'your raw text'"
  exit 1
fi

prompt_anonymize "$1"
