import json
import subprocess
from typing import Any, Dict, List


class OpenClawIntelligence:
    def __init__(self, session_id: str = "cfo-cli-ai", timeout_seconds: int = 120):
        self.session_id = session_id
        self.timeout_seconds = timeout_seconds

    def generate(self, prompt: str) -> str:
        cmd = [
            "openclaw",
            "agent",
            "--local",
            "--json",
            "--session-id",
            self.session_id,
            "--message",
            prompt,
            "--timeout",
            str(self.timeout_seconds),
        ]

        cp = subprocess.run(
            args=cmd,
            text=True,
            capture_output=True,
            check=False,
        )

        if cp.returncode != 0:
            raise RuntimeError(f"OpenClaw agent failed: {cp.stderr or cp.stdout}")

        return self._extract_text(cp.stdout)

    def analyze_anomalies(self, transactions: List[Dict[str, Any]]) -> str:
        prompt = (
            "You are an expert forensic accountant. Analyze these Odoo transactions for "
            "duplicates, unusual amounts, missing tax indicators, and suspicious timing. "
            "Return concise findings and action items.\n\n"
            f"Transactions JSON:\n{json.dumps(transactions, indent=2)}"
        )
        return self.generate(prompt)

    def natural_language_query(self, query: str, context_data: Dict[str, Any]) -> str:
        prompt = (
            "You are the Autonomous CFO. Answer using the provided Odoo context only. "
            "Be direct, use AED for currency references, and flag risks. "
            "If missing data, say exactly what to query next in Odoo.\n\n"
            f"Question: {query}\n\n"
            f"Context JSON:\n{json.dumps(context_data, indent=2)}"
        )
        return self.generate(prompt)

    @staticmethod
    def _extract_text(stdout: str) -> str:
        data: Dict[str, Any] = json.loads(stdout)
        payloads = data.get("payloads") or []
        if not payloads:
            return ""
        first = payloads[0] if isinstance(payloads[0], dict) else {}
        return str(first.get("text") or "")
