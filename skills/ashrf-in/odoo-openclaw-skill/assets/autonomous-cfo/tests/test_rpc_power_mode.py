import os
import sys
import unittest
from unittest.mock import Mock, patch

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.connectors.odoo_client import OdooClient


class TestRpcPowerMode(unittest.TestCase):
    def test_json2_call_raw_posts_model_method(self):
        client = OdooClient(
            url="https://example.odoo.com",
            db="example-db",
            username="bot@example.com",
            password="api-key-123",
            rpc_backend="json2",
        )

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"id": 1, "name": "Agrolait"}]

        with patch("src.connectors.odoo_client.requests.post", return_value=mock_response) as post:
            out = client.call_raw("res.partner", "search_read", {"domain": [], "fields": ["name"], "limit": 1})

        self.assertEqual(out, [{"id": 1, "name": "Agrolait"}])
        self.assertEqual(post.call_args.kwargs["url"], "https://example.odoo.com/json/2/res.partner/search_read")


if __name__ == "__main__":
    unittest.main()
