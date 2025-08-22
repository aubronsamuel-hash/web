import os
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from app.main import create_app
from app.settings import get_settings
from app.db import Base, get_engine


def _client():
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


def _token(c: TestClient) -> str:
    r = c.post(
        "/auth/token",
        data={"username": "admin@example.com", "password": "s3cret"},
    )
    assert r.status_code == 200
    return r.json()["access_token"]


def test_filter_by_request_id_ok():
    c = _client()
    t = _token(c)
    h = {"Authorization": f"Bearer {t}"}
    now = datetime.utcnow()
    r = c.post(
        "/missions",
        json={
            "title": "AuditCase",
            "start_at": now.isoformat(),
            "end_at": (now + timedelta(hours=1)).isoformat(),
        },
        headers=h,
    )
    assert r.status_code == 201
    rid = r.headers.get("X-Request-ID")
    r2 = c.get(f"/audits?request_id={rid}", headers=h)
    assert r2.status_code == 200
    data = r2.json()
    assert data["total"] >= 1
    for it in data["items"]:
        assert it["request_id"] == rid


def test_delete_action_audited_ok():
    c = _client()
    t = _token(c)
    h = {"Authorization": f"Bearer {t}"}
    now = datetime.utcnow()
    r = c.post(
        "/missions",
        json={
            "title": "ToDelete",
            "start_at": now.isoformat(),
            "end_at": (now + timedelta(hours=1)).isoformat(),
        },
        headers=h,
    )
    mid = r.json()["id"]
    r2 = c.delete(f"/missions/{mid}", headers=h)
    assert r2.status_code == 204
    r3 = c.get("/audits?action=delete&entity=mission", headers=h)
    assert r3.status_code == 200
    assert r3.json()["total"] >= 1


def test_bad_time_range_400():
    c = _client()
    t = _token(c)
    h = {"Authorization": f"Bearer {t}"}
    r = c.get(
        "/audits?from_ts=2025-12-31T00:00:00&to_ts=2025-01-01T00:00:00",
        headers=h,
    )
    assert r.status_code == 400
