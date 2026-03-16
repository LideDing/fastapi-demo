"""Tests for JWT-based authentication dependency."""
from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient
from jose import jwt


def _make_token(user_id: str, secret: str = "test-jwt-secret-for-unit-tests", exp_delta_seconds: int = 3600) -> str:
    exp = datetime.now(UTC) + timedelta(seconds=exp_delta_seconds)
    return jwt.encode({"sub": user_id, "exp": exp}, secret, algorithm="HS256")


@pytest.fixture
def client():
    from app.main import create_app

    app = create_app()
    return TestClient(app)


def _mock_user_with_groups(user_id: str = "test-user-id", groups: list[str] | None = None):
    mock_user = MagicMock()
    mock_user.id = user_id
    mock_user.username = "alice"
    return mock_user, groups or []


def test_valid_jwt_authenticates(client):
    """Valid Bearer JWT resolves to authenticated user."""
    token = _make_token("00000000-0000-0000-0000-000000000001")

    with patch(
        "app.dependencies.auth.get_user_with_groups",
        new_callable=AsyncMock,
        return_value=_mock_user_with_groups("00000000-0000-0000-0000-000000000001", ["admin"]),
    ):
        resp = client.get(
            "/hello",
            headers={"Authorization": f"Bearer {token}", "Accept": "application/json"},
        )

    assert resp.status_code == 200


def test_expired_jwt_returns_401(client):
    """Expired JWT returns 401 with 'Token expired' detail."""
    token = _make_token("00000000-0000-0000-0000-000000000001", exp_delta_seconds=-10)

    resp = client.get(
        "/hello",
        headers={"Authorization": f"Bearer {token}", "Accept": "application/json"},
    )

    assert resp.status_code == 401
    assert "expired" in resp.json()["detail"].lower()


def test_invalid_jwt_signature_returns_401(client):
    """Tampered JWT returns 401 with 'Invalid token' detail."""
    token = _make_token("some-user", secret="wrong-secret")

    resp = client.get(
        "/hello",
        headers={"Authorization": f"Bearer {token}", "Accept": "application/json"},
    )

    assert resp.status_code == 401
    assert "invalid" in resp.json()["detail"].lower()
