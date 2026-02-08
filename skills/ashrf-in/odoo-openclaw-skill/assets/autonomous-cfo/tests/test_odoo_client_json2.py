import os
import sys
import unittest
from unittest.mock import Mock, patch

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.connectors.odoo_client import OdooClient


class TestOdooClientJson2(unittest.TestCase):
    def test_json2_search_read_calls_http_endpoint(self):
        client = OdooClient(
            url="https://example.odoo.com",
            db="example-db",
            username="bot@example.com",
            password="api-key-123",
            rpc_backend="json2",
        )

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"id": 1, "name": "Deco Addict"}]
        mock_response.raise_for_status.return_value = None

        with patch("src.connectors.odoo_client.requests.post", return_value=mock_response) as post:
            rows = client.search_read(
                "res.partner",
                domain=[["is_company", "=", True]],
                fields=["name"],
                limit=5,
                offset=0,
            )

        self.assertEqual(rows, [{"id": 1, "name": "Deco Addict"}])
        post.assert_called_once()
        url = post.call_args.kwargs["url"]
        headers = post.call_args.kwargs["headers"]
        payload = post.call_args.kwargs["json"]

        self.assertEqual(url, "https://example.odoo.com/json/2/res.partner/search_read")
        self.assertEqual(headers["Authorization"], "bearer api-key-123")
        self.assertEqual(headers["X-Odoo-Database"], "example-db")
        self.assertEqual(payload["domain"], [["is_company", "=", True]])
        self.assertEqual(payload["fields"], ["name"])
        self.assertEqual(payload["limit"], 5)

    def test_json2_read_uses_ids_payload(self):
        client = OdooClient(
            url="https://example.odoo.com",
            db="example-db",
            username="bot@example.com",
            password="api-key-123",
            rpc_backend="json2",
        )

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"id": 10, "name": "Partner 10"}]
        mock_response.raise_for_status.return_value = None

        with patch("src.connectors.odoo_client.requests.post", return_value=mock_response) as post:
            _ = client.read("res.partner", [10], fields=["name"])

        payload = post.call_args.kwargs["json"]
        self.assertEqual(payload["ids"], [10])
        self.assertEqual(payload["fields"], ["name"])


if __name__ == "__main__":
    unittest.main()
