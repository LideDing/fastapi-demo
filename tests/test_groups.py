"""Tests for /groups API — admin vs non-admin access."""
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi.testclient import TestClient

from app.dependencies.auth import require_admin, require_auth
from app.models.auth import UserInfo


def _admin_user() -> UserInfo:
    return UserInfo(id="admin-id", sub="admin-id", name="Admin", groups=["admin"])


def _regular_user() -> UserInfo:
    return UserInfo(id="user-id", sub="user-id", name="Regular", groups=[])


@pytest.fixture
def admin_client():
    from app.main import create_app

    app = create_app()

    async def _mock_auth():
        return _admin_user()

    async def _mock_admin():
        return _admin_user()

    app.dependency_overrides[require_auth] = _mock_auth
    app.dependency_overrides[require_admin] = _mock_admin
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture
def regular_client():
    from app.main import create_app

    app = create_app()

    async def _mock_auth():
        return _regular_user()

    app.dependency_overrides[require_auth] = _mock_auth
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


# ── admin can list groups ──────────────────────────────────────────────────────

def test_admin_can_list_groups(admin_client):
    """Admin can GET /groups."""
    mock_group = MagicMock()
    mock_group.id = "00000000-0000-0000-0000-000000000001"
    mock_group.name = "admin"
    mock_group.description = "Administrators"
    from datetime import datetime
    mock_group.created_at = datetime(2024, 1, 1)

    with __import__("unittest.mock", fromlist=["patch"]).patch(
        "app.routers.groups.group_svc.list_groups",
        new_callable=AsyncMock,
        return_value=[mock_group],
    ):
        resp = admin_client.get("/groups")

    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert data[0]["name"] == "admin"


def test_admin_can_create_group(admin_client):
    """Admin can POST /groups."""
    mock_group = MagicMock()
    mock_group.id = "00000000-0000-0000-0000-000000000002"
    mock_group.name = "editors"
    mock_group.description = None
    from datetime import datetime
    mock_group.created_at = datetime(2024, 1, 1)

    with __import__("unittest.mock", fromlist=["patch"]).patch(
        "app.routers.groups.group_svc.create_group",
        new_callable=AsyncMock,
        return_value=mock_group,
    ):
        resp = admin_client.post("/groups", json={"name": "editors"})

    assert resp.status_code == 201
    assert resp.json()["name"] == "editors"


# ── non-admin is forbidden ─────────────────────────────────────────────────────

def test_non_admin_cannot_list_groups(regular_client):
    """Non-admin user gets 403 on GET /groups."""
    resp = regular_client.get("/groups")
    assert resp.status_code == 403


def test_non_admin_cannot_create_group(regular_client):
    """Non-admin user gets 403 on POST /groups."""
    resp = regular_client.post("/groups", json={"name": "hackers"})
    assert resp.status_code == 403
