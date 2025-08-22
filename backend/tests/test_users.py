import os

import pytest  # noqa: F401
from fastapi.testclient import TestClient

from app.db import Base, get_engine
from app.main import create_app
from app.settings import get_settings


def _make_client():
    os.environ["ADMIN_EMAIL"] = "admin@example.com"
    os.environ["ADMIN_PASSWORD"] = "s3cret"
    os.environ["JWT_SECRET"] = "unit-test-secret"
    os.environ["DB_DSN"] = "sqlite://"
    try:
        get_settings.cache_clear()  # type: ignore[attr-defined]
    except Exception:
        pass
    # Fresh in-memory DB
    engine = get_engine()
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    app = create_app()
    return TestClient(app)


def _login_token(c: TestClient) -> str:
    r = c.post(
        "/auth/token",
        data={"username": "admin@example.com", "password": "s3cret"},
    )
    assert r.status_code == 200, r.text
    return r.json()["access_token"]


def test_users_create_and_get_ok():
    c = _make_client()
    token = _login_token(c)
    r = c.post(
        "/users",
        json={"email": "a@b.com", "full_name": "A B"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 201, r.text
    uid = r.json()["id"]
    r2 = c.get(f"/users/{uid}", headers={"Authorization": f"Bearer {token}"})
    assert r2.status_code == 200
    assert r2.json()["email"] == "a@b.com"


def test_users_list_paginated_ok():
    c = _make_client()
    token = _login_token(c)
    for i in range(35):
        c.post(
            "/users",
            json={"email": f"user{i}@ex.com"},
            headers={"Authorization": f"Bearer {token}"},
        )
    r = c.get(
        "/users?page=2&size=20",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 200
    data = r.json()
    assert data["page"] == 2 and data["size"] == 20 and data["total"] == 35 and data["pages"] == 2
    assert len(data["items"]) == 15


def test_users_duplicate_email_409():
    c = _make_client()
    token = _login_token(c)
    c.post(
        "/users",
        json={"email": "dup@ex.com"},
        headers={"Authorization": f"Bearer {token}"},
    )
    r = c.post(
        "/users",
        json={"email": "dup@ex.com"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 409


def test_users_not_found_404():
    c = _make_client()
    token = _login_token(c)
    r = c.get("/users/9999", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 404

