from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

from app.dependencies.auth import require_auth
from app.models.auth import UserInfo


@pytest.fixture
def client():
    from app.main import create_app

    app = create_app()
    return TestClient(app)


@pytest.fixture
def authed_client():
    """Client with authenticated session via dependency override."""
    from app.main import create_app

    app = create_app()

    async def _mock_require_auth():
        return UserInfo(sub="user123", name="Test User", id="user123")

    app.dependency_overrides[require_auth] = _mock_require_auth
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_health_no_auth(client):
    """Health endpoint remains public."""
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_hello_redirects_when_unauthenticated(client):
    """/hello redirects to /auth/login when no session (browser request)."""
    resp = client.get(
        "/hello",
        follow_redirects=False,
        headers={"Accept": "text/html"},
    )
    assert resp.status_code == 302
    location = resp.headers["location"]
    assert "/auth/login" in location
    assert "next=" in location
    assert "/hello" in location


def test_hello_authenticated_with_session(authed_client):
    """/hello serves response when user is authenticated."""
    resp = authed_client.get("/hello")
    assert resp.status_code == 200
    data = resp.json()
    assert "message" in data
    assert "current_time" in data


def test_oidc_login_redirects_to_provider(client):
    """/auth/login redirects to OIDC provider."""
    with patch(
        "app.routers.oidc.get_authorization_url",
        new_callable=AsyncMock,
    ) as mock_auth_url:
        mock_auth_url.return_value = "https://idp.example.com/authorize?client_id=test"
        resp = client.get("/auth/login?next=/hello", follow_redirects=False)
        assert resp.status_code == 302
        location = resp.headers["location"]
        assert "idp.example.com" in location


def test_oidc_logout_clears_session(client):
    """/auth/logout clears session and redirects to /health."""
    resp = client.get("/auth/logout", follow_redirects=False)
    assert resp.status_code == 302
    assert "/health" in resp.headers["location"]


def test_oidc_callback_error(client):
    """Callback with error returns 401."""
    resp = client.get("/auth/callback?error=access_denied")
    assert resp.status_code == 401


def test_oidc_callback_missing_code(client):
    """Callback without code returns 401."""
    resp = client.get("/auth/callback")
    assert resp.status_code == 401
