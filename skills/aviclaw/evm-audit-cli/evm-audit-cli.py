#!/usr/bin/env python3
"""
EVM Audit CLI - AI-powered smart contract auditing
Usage: evm-audit-cli <path>
"""

import os
import sys
import json
import argparse
from pathlib import Path

# Check for OpenRouter API key
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def get_audit_prompt(contracts_content):
    """Generate audit prompt for AI."""
    return f"""You are an expert smart contract security auditor.

Analyze the following Solidity contracts for security vulnerabilities.

For each vulnerability found, provide:
- title: Brief name
- severity: critical, high, medium, low, informational
- summary: Brief description
- description: File, line numbers, explanation
- recommendation: How to fix

Output ONLY valid JSON:
{{"vulnerabilities": [{{"title": "...", "severity": "...", "summary": "...", "description": "...", "recommendation": "..."}}]}}

If no vulnerabilities, output: {{"vulnerabilities": []}}

Contracts:
{contracts_content}"""

def call_ai(prompt, model="openai/gpt-4o-mini"):
    """Call AI via OpenRouter."""
    if not OPENROUTER_API_KEY:
        return None, "OPENROUTER_API_KEY not set"
    
    import requests
    
    try:
        resp = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "HTTP-Referer": "https://openclaw.ai",
                "X-Title": "EVM Audit CLI"
            },
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": "You are an expert smart contract security auditor. Output ONLY valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 3000
            },
            timeout=120
        )
        
        if resp.status_code != 200:
            return None, f"API error: {resp.status_code}"
        
        data = resp.json()
        content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
        return content, None
    except Exception as e:
        return None, str(e)

def main():
    parser = argparse.ArgumentParser(description="EVM Audit CLI - AI-powered contract auditing")
    parser.add_argument("target", help="Path to Solidity file or directory")
    parser.add_argument("--model", default="openai/gpt-4o-mini", help="AI model to use")
    parser.add_argument("--format", default="markdown", choices=["json", "markdown"])
    
    args = parser.parse_args()
    
    target = args.target
    
    if not os.path.exists(target):
        print(f"Error: {target} does not exist")
        sys.exit(1)
    
    # Read all .sol files
    contracts_content = ""
    sol_files = []
    
    if os.path.isfile(target):
        sol_files = [Path(target)]
    else:
        sol_files = list(Path(target).glob("**/*.sol"))
    
    if not sol_files:
        print("No .sol files found")
        sys.exit(1)
    
    for sol_file in sol_files[:5]:  # Limit to 5 files
        try:
            contracts_content += f"\n\n=== {sol_file.name} ===\n\n"
            contracts_content += sol_file.read_text()
        except Exception as e:
            print(f"Warning: Could not read {sol_file}: {e}", file=sys.stderr)
            pass
    
    if not contracts_content:
        print("Could not read contract files")
        sys.exit(1)
    
    print(f"Analyzing {len(sol_files)} file(s) with {args.model}...")
    
    # Call AI
    prompt = get_audit_prompt(contracts_content)
    result, err = call_ai(prompt, args.model)
    
    if err:
        print(f"Error: {err}")
        sys.exit(1)
    
    # Try to parse JSON from result
    try:
        # Find JSON in response
        start = result.find("{")
        end = result.rfind("}") + 1
        if start >= 0 and end > start:
            json_str = result[start:end]
            vulnerabilities = json.loads(json_str).get("vulnerabilities", [])
        else:
            vulnerabilities = []
    except:
        vulnerabilities = []
    
    # Output
    if args.format == "json":
        print(json.dumps({"vulnerabilities": vulnerabilities}, indent=2))
    else:
        print(f"# Audit Report: {os.path.basename(target)}")
        print(f"**Model:** {args.model}")
        print()
        
        if vulnerabilities:
            for v in vulnerabilities:
                print(f"- **{v.get('title', 'Unknown')}** ({v.get('severity', 'unknown')})")
                print(f"  {v.get('summary', '')[:100]}")
                print()
        else:
            print("No vulnerabilities found (or could not parse response)")
        
        print(f"**Note:** AI analysis - verify findings manually")

if __name__ == "__main__":
    main()
