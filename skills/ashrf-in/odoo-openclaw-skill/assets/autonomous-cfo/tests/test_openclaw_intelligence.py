import os
import sys
import unittest
from unittest.mock import Mock, patch

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.logic.openclaw_intelligence import OpenClawIntelligence


class TestOpenClawIntelligence(unittest.TestCase):
    def test_generates_text_via_openclaw_agent_local_json(self):
        llm = OpenClawIntelligence(session_id="cfo-cli-test")

        cp = Mock()
        cp.returncode = 0
        cp.stdout = '{"payloads":[{"text":"analysis ready"}]}'

        with patch("src.logic.openclaw_intelligence.subprocess.run", return_value=cp) as run:
            text = llm.generate("hello")

        self.assertEqual(text, "analysis ready")
        cmd = run.call_args.kwargs["args"]
        self.assertIn("openclaw", cmd)
        self.assertIn("agent", cmd)
        self.assertIn("--local", cmd)
        self.assertIn("--json", cmd)

    def test_raises_when_openclaw_command_fails(self):
        llm = OpenClawIntelligence(session_id="cfo-cli-test")

        cp = Mock()
        cp.returncode = 1
        cp.stdout = ""
        cp.stderr = "boom"

        with patch("src.logic.openclaw_intelligence.subprocess.run", return_value=cp):
            with self.assertRaises(RuntimeError):
                llm.generate("hello")


if __name__ == "__main__":
    unittest.main()
