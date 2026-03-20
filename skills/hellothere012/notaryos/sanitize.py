"""
sanitize.py — Payload sanitization for NotaryOS receipts.

Strips sensitive fields from payloads before they are sealed and transmitted
to the NotaryOS API. Use this before every notary.seal() call when the payload
may contain user data.

No external dependencies. No network calls. No file access.

Usage:
    from sanitize import sanitize_payload, seal_safe

    # Strip sensitive fields
    clean = sanitize_payload({"user": "alice", "password": "hunter2"})
    # -> {"user": "alice"}

    # Or use seal_safe() for one-step sanitize + seal
    from notaryos import NotaryClient
    notary = NotaryClient()
    receipt = seal_safe(notary, "user.login", {"user": "alice", "password": "hunter2"})

License: BSL-1.1 (https://github.com/hellothere012/notaryos/blob/main/LICENSE)
"""

from typing import Any, Dict, Optional, Set

# Fields that are ALWAYS stripped from payloads before transmission.
# Case-insensitive matching. Add domain-specific fields as needed.
SENSITIVE_FIELDS: Set[str] = {
    # Authentication
    "password",
    "passwd",
    "secret",
    "token",
    "api_key",
    "apikey",
    "api_secret",
    "access_token",
    "refresh_token",
    "auth_token",
    "bearer",
    "credentials",
    "private_key",
    "signing_key",
    # Financial
    "credit_card",
    "card_number",
    "cvv",
    "cvc",
    "expiry",
    "account_number",
    "routing_number",
    "iban",
    "swift",
    "bank_account",
    # Personal
    "ssn",
    "social_security",
    "date_of_birth",
    "dob",
    "national_id",
    "passport_number",
    "drivers_license",
    # Contact (optional — uncomment if needed)
    # "phone",
    # "email",
    # "address",
}

# Patterns in field names that suggest sensitivity (substring match)
SENSITIVE_PATTERNS = (
    "password",
    "secret",
    "token",
    "credential",
    "private_key",
    "api_key",
)


def sanitize_payload(
    payload: Dict[str, Any],
    extra_fields: Optional[Set[str]] = None,
    redact_marker: str = "[REDACTED]",
) -> Dict[str, Any]:
    """
    Remove sensitive fields from a payload dict before sealing.

    Args:
        payload: The raw payload dict to sanitize.
        extra_fields: Additional field names to strip (merged with defaults).
        redact_marker: If set, replaced value is this string. If None, key is removed entirely.

    Returns:
        A new dict with sensitive fields removed or redacted.
        Original dict is not modified.
    """
    blocked = SENSITIVE_FIELDS | (extra_fields or set())
    result = {}

    for key, value in payload.items():
        key_lower = key.lower()

        # Check exact match
        if key_lower in blocked:
            if redact_marker is not None:
                result[key] = redact_marker
            continue

        # Check substring patterns
        if any(pat in key_lower for pat in SENSITIVE_PATTERNS):
            if redact_marker is not None:
                result[key] = redact_marker
            continue

        # Recursively sanitize nested dicts
        if isinstance(value, dict):
            result[key] = sanitize_payload(value, extra_fields, redact_marker)
        elif isinstance(value, list):
            result[key] = [
                sanitize_payload(item, extra_fields, redact_marker)
                if isinstance(item, dict) else item
                for item in value
            ]
        else:
            result[key] = value

    return result


def seal_safe(
    notary,
    action_type: str,
    payload: Dict[str, Any],
    extra_fields: Optional[Set[str]] = None,
    **kwargs,
):
    """
    Sanitize payload then seal in one step.

    Args:
        notary: NotaryClient instance
        action_type: Action type string (e.g., "file.created")
        payload: Raw payload dict (will be sanitized before sealing)
        extra_fields: Additional fields to strip
        **kwargs: Passed to notary.seal() (e.g., previous_receipt_hash)

    Returns:
        Receipt object from notary.seal()
    """
    clean = sanitize_payload(payload, extra_fields, redact_marker=None)
    return notary.seal(action_type, clean, **kwargs)


# ---------------------------------------------------------------------------
# Self-test (runs when executed directly: python sanitize.py)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=== sanitize.py self-test ===\n")

    # Test 1: Basic field stripping
    raw = {
        "user": "alice",
        "password": "hunter2",
        "api_key": "sk-secret-xxx",
        "action": "login",
        "ip": "192.168.1.1",
    }
    clean = sanitize_payload(raw)
    assert "password" not in clean or clean["password"] == "[REDACTED]"
    assert "api_key" not in clean or clean["api_key"] == "[REDACTED]"
    assert clean["user"] == "alice"
    assert clean["action"] == "login"
    print(f"Test 1 PASS: {raw} -> {clean}")

    # Test 2: Nested dict sanitization
    nested = {
        "config": {
            "database_url": "postgres://...",
            "secret": "mysecret",
            "host": "localhost",
        },
        "name": "my-service",
    }
    clean2 = sanitize_payload(nested)
    assert clean2["config"]["host"] == "localhost"
    assert clean2["config"]["secret"] == "[REDACTED]"
    print(f"Test 2 PASS: nested secret redacted")

    # Test 3: Pattern matching (substring)
    pattern_test = {
        "user_password_hash": "abc123",
        "db_secret_key": "xyz",
        "display_name": "Alice",
    }
    clean3 = sanitize_payload(pattern_test)
    assert clean3["display_name"] == "Alice"
    assert clean3.get("user_password_hash") == "[REDACTED]"
    assert clean3.get("db_secret_key") == "[REDACTED]"
    print(f"Test 3 PASS: pattern matching works")

    # Test 4: Remove instead of redact
    clean4 = sanitize_payload(raw, redact_marker=None)
    assert "password" not in clean4
    assert "api_key" not in clean4
    assert clean4["user"] == "alice"
    print(f"Test 4 PASS: removal mode (no marker)")

    # Test 5: Extra fields
    clean5 = sanitize_payload(
        {"email": "alice@example.com", "name": "Alice"},
        extra_fields={"email"},
    )
    assert clean5.get("email") == "[REDACTED]"
    assert clean5["name"] == "Alice"
    print(f"Test 5 PASS: extra_fields parameter")

    print("\n=== All 5 tests passed ===")
