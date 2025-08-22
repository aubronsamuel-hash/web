import os
from datetime import datetime, timedelta

import pytest  # noqa: F401
from fastapi.testclient import TestClient
from sqlalchemy import select

from app.db import Base, get_engine, session_scope
from app.main import create_app
from app.models_audit import AuditLog
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


def test_missions_create_publish_audit_ok():
    c = _make_client()
    token = _login_token(c)
    auth = {"Authorization": f"Bearer {token}"}
    now = datetime.utcnow()
    payload = {
        "title": "Show",
        "start_at": (now + timedelta(hours=1)).isoformat(),
        "end_at": (now + timedelta(hours=2)).isoformat(),
    }
    r = c.post("/missions", json=payload, headers=auth)
    assert r.status_code == 201, r.text
    rid_create = r.headers["X-Request-ID"]
    mid = r.json()["id"]
    r2 = c.post(f"/missions/{mid}/publish", headers=auth)
    assert r2.status_code == 200
    rid_publish = r2.headers["X-Request-ID"]
    with session_scope() as db:
        actions_create = db.scalars(
            select(AuditLog.action).where(AuditLog.request_id == rid_create)
        ).all()
        actions_publish = db.scalars(
            select(AuditLog.action).where(AuditLog.request_id == rid_publish)
        ).all()
    assert actions_create == ["create"]
    assert actions_publish == ["publish"]


def test_missions_duplicate_search_ok():
    c = _make_client()
    token = _login_token(c)
    auth = {"Authorization": f"Bearer {token}"}
    now = datetime.utcnow()
    payload = {
        "title": "Concert",
        "start_at": (now + timedelta(hours=1)).isoformat(),
        "end_at": (now + timedelta(hours=2)).isoformat(),
    }
    r = c.post("/missions", json=payload, headers=auth)
    mid = r.json()["id"]
    r2 = c.post(f"/missions/{mid}/duplicate", headers=auth)
    assert r2.status_code == 201
    r3 = c.get("/missions?q=Concert", headers=auth)
    assert r3.status_code == 200
    assert len(r3.json()["items"]) == 2


def test_missions_publish_404():
    c = _make_client()
    token = _login_token(c)
    r = c.post("/missions/9999/publish", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 404


def test_missions_duplicate_404():
    c = _make_client()
    token = _login_token(c)
    r = c.post("/missions/9999/duplicate", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 404
