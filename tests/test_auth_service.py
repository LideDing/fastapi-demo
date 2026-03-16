import pytest
from starlette.testclient import TestClient

from app.models.auth import UserInfo


@pytest.fixture
def client():
    from app.main import create_app

    app = create_app()
    return TestClient(app)


def test_require_auth_redirects_without_session(client):
    """Missing session triggers redirect to /auth/login for browser requests."""
    resp = client.get(
        "/hello",
        follow_redirects=False,
        headers={"Accept": "text/html"},
    )
    assert resp.status_code == 302
    location = resp.headers["location"]
    assert "/auth/login" in location
    assert "next=" in location


def test_userinfo_model():
    """UserInfo model parses correctly."""
    user = UserInfo(sub="user123", name="Test User", id="user123")
    assert user.sub == "user123"
    assert user.name == "Test User"
    assert user.extra == {}
    assert user.groups == []


def test_userinfo_model_minimal():
    """UserInfo model works with minimal fields."""
    user = UserInfo(sub="user123")
    assert user.sub == "user123"
    assert user.name == ""
    assert user.groups == []
