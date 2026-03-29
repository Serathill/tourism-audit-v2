"""Tests for Flask routes — auth, healthz, input validation."""

import os
import pytest
from unittest.mock import patch, MagicMock

# Set env vars BEFORE importing app (module-level create_app runs at import)
os.environ.setdefault("GOOGLE_API_KEY", "test")
os.environ.setdefault("SUPABASE_URL", "https://test.supabase.co")
os.environ.setdefault("SUPABASE_KEY", "test-key")
os.environ.setdefault("RESEND_API_KEY", "test-resend")
os.environ.setdefault("BACKEND_API_KEY", "test-api-key")

from app import create_app


@pytest.fixture(autouse=True)
def _patch_api_key():
    """Patch BACKEND_API_KEY in both config and routes modules."""
    with patch("config.BACKEND_API_KEY", "test-api-key"), \
         patch("src.routes.BACKEND_API_KEY", "test-api-key"):
        yield


@pytest.fixture
def app():
    app = create_app()
    app.config["TESTING"] = True
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


class TestHealthz:
    @patch("src.routes.SupabaseService")
    def test_returns_200(self, mock_db, client):
        mock_instance = MagicMock()
        mock_instance.reset_stale_audits.return_value = 0
        mock_db.return_value = mock_instance

        response = client.get("/healthz")
        assert response.status_code == 200
        assert response.json["status"] == "ok"

    @patch("src.routes.SupabaseService")
    def test_reports_stale_count(self, mock_db, client):
        mock_instance = MagicMock()
        mock_instance.reset_stale_audits.return_value = 2
        mock_db.return_value = mock_instance

        response = client.get("/healthz")
        assert response.json["stale_reset"] == 2

    @patch("src.routes.SupabaseService", side_effect=Exception("DB down"))
    def test_healthz_survives_db_failure(self, mock_db, client):
        response = client.get("/healthz")
        assert response.status_code == 200


class TestGenerateAuditAuth:
    def test_no_api_key_returns_401(self, client):
        response = client.post(
            "/api/generate-audit",
            json={"property_id": "test-id"},
        )
        assert response.status_code == 401

    def test_wrong_api_key_returns_401(self, client):
        response = client.post(
            "/api/generate-audit",
            json={"property_id": "test-id"},
            headers={"X-API-Key": "wrong-key"},
        )
        assert response.status_code == 401

    def test_empty_api_key_returns_401(self, client):
        response = client.post(
            "/api/generate-audit",
            json={"property_id": "test-id"},
            headers={"X-API-Key": ""},
        )
        assert response.status_code == 401

    @patch("src.routes.SupabaseService")
    def test_valid_api_key_passes_auth(self, mock_db, client):
        mock_instance = MagicMock()
        mock_instance.get_property_by_id.return_value = None
        mock_db.return_value = mock_instance

        response = client.post(
            "/api/generate-audit",
            json={"property_id": "nonexistent"},
            headers={"X-API-Key": "test-api-key"},
        )
        assert response.status_code == 404

    def test_missing_property_id_returns_400(self, client):
        response = client.post(
            "/api/generate-audit",
            json={},
            headers={"X-API-Key": "test-api-key"},
        )
        assert response.status_code == 400


class TestDuplicateGuard:
    @patch("src.routes.SupabaseService")
    def test_running_audit_returns_409(self, mock_db, client):
        mock_instance = MagicMock()
        mock_property = MagicMock()
        mock_property.status = 1
        mock_instance.get_property_by_id.return_value = mock_property
        mock_db.return_value = mock_instance

        response = client.post(
            "/api/generate-audit",
            json={"property_id": "test-id"},
            headers={"X-API-Key": "test-api-key"},
        )
        assert response.status_code == 409

    @patch("src.routes.SupabaseService")
    def test_completed_audit_returns_409(self, mock_db, client):
        mock_instance = MagicMock()
        mock_property = MagicMock()
        mock_property.status = 99
        mock_instance.get_property_by_id.return_value = mock_property
        mock_db.return_value = mock_instance

        response = client.post(
            "/api/generate-audit",
            json={"property_id": "test-id"},
            headers={"X-API-Key": "test-api-key"},
        )
        assert response.status_code == 409
