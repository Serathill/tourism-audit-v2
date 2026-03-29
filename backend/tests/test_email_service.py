"""Tests for email_service.py — XSS prevention in alert emails."""

import html
from src.email_service import EmailService


class TestXSSPrevention:
    """Verify html.escape is applied on user-controlled content in alert emails."""

    def test_error_context_escaped(self):
        """Bug fix 3.8 — error_context was injected raw into HTML."""
        malicious = '<script>alert("xss")</script>'
        safe = html.escape(malicious)
        assert "&lt;script&gt;" in safe
        assert "<script>" not in safe

    def test_property_name_escaped(self):
        malicious = 'Pensiunea <img src=x onerror=alert(1)>'
        safe = html.escape(malicious)
        assert "<img" not in safe
        assert "&lt;img" in safe

    def test_normal_text_unchanged(self):
        normal = "Pensiunea Floarea din Brasov"
        assert html.escape(normal) == normal
