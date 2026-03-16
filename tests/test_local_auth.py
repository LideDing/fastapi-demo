"""Tests for POST /auth/register and POST /auth/login."""
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.exc import IntegrityError


@pytest.fixture
def client():
    from app.main import create_app

    app = create_app()
    return TestClient(app)


# ── register ──────────────────────────────────────────────────────────────────


def test_register_success(client):
    """Successful registration returns 201 with user_id and username."""
    mock_user = MagicMock()
    mock_user.id = "00000000-0000-0000-0000-000000000001"
    mock_user.username = "alice"

    with patch(
        "app.routers.local_auth.create_user",
        new_callable=AsyncMock,
        return_value=mock_user,
    ):
        resp = client.post(
            "/auth/register",
            json={"username": "alice", "password": "securepass"},
        )

    assert resp.status_code == 201
    data = resp.json()
    assert data["username"] == "alice"
    assert "user_id" in data


def test_register_duplicate_username(client):
    """Duplicate username returns 409."""
    with patch(
        "app.routers.local_auth.create_user",
        new_callable=AsyncMock,
        side_effect=IntegrityError("unique", {}, None),
    ):
        resp = client.post(
            "/auth/register",
            json={"username": "alice", "password": "securepass"},
        )

    assert resp.status_code == 409


def test_register_password_too_short(client):
    """Password shorter than 8 chars returns 422."""
    resp = client.post(
        "/auth/register",
        json={"username": "bob", "password": "short"},
    )
    assert resp.status_code == 422


# ── login ─────────────────────────────────────────────────────────────────────


def test_login_success(client):
    """Valid credentials return access_token."""
    mock_user = MagicMock()
    mock_user.id = "00000000-0000-0000-0000-000000000001"

    with (
        patch(
            "app.routers.local_auth.authenticate_user",
            new_callable=AsyncMock,
            return_value=mock_user,
        ),
        patch(
            "app.routers.local_auth.create_access_token",
            return_value="fake.jwt.token",
        ),
    ):
        resp = client.post(
            "/auth/login",
            json={"username": "alice", "password": "securepass"},
        )

    assert resp.status_code == 200
    data = resp.json()
    assert data["access_token"] == "fake.jwt.token"
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client):
    """Wrong password returns 401."""
    with patch(
        "app.routers.local_auth.authenticate_user",
        new_callable=AsyncMock,
        return_value=None,
    ):
        resp = client.post(
            "/auth/login",
            json={"username": "alice", "password": "wrongpass"},
        )

    assert resp.status_code == 401
    assert resp.json()["detail"] == "Invalid credentials"


def test_login_unknown_user(client):
    """Non-existent user returns 401."""
    with patch(
        "app.routers.local_auth.authenticate_user",
        new_callable=AsyncMock,
        return_value=None,
    ):
        resp = client.post(
            "/auth/login",
            json={"username": "nobody", "password": "securepass"},
        )

    assert resp.status_code == 401
