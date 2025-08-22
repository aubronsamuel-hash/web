import os
from datetime import datetime, timedelta

from fastapi.testclient import TestClient

from app.db import Base, get_engine
from app.main import create_app
from app.settings import get_settings


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
    r = c.post("/auth/token", data={"username": "admin@example.com", "password": "s3cret"})
    assert r.status_code == 200
    return r.json()["access_token"]


def _mk_mission(c: TestClient, t: str, start: datetime, end: datetime, token: str) -> int:
    r = c.post(
        "/missions",
        json={"title": t, "start_at": start.isoformat(), "end_at": end.isoformat()},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 201, r.text
    return r.json()["id"]


def _mk_avail(c: TestClient, inter_id: int, start: datetime, end: datetime, token: str) -> int:
    r = c.post(
        "/availabilities",
        json={
            "intermittent_id": inter_id,
            "start_at": start.isoformat(),
            "end_at": end.isoformat(),
            "busy": True,
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 201, r.text
    return r.json()["id"]


def test_conflict_with_other_missions_ok():
    c = _client()
    t = _token(c)
    now = datetime.utcnow()
    _mk_mission(c, "A", now + timedelta(hours=1), now + timedelta(hours=3), t)
    b = _mk_mission(c, "B", now + timedelta(hours=2), now + timedelta(hours=4), t)
    body = {
        "start_at": (now + timedelta(hours=1)).isoformat(),
        "end_at": (now + timedelta(hours=3)).isoformat(),
    }
    r = c.post("/planning/check", json=body, headers={"Authorization": f"Bearer {t}"})
    assert r.status_code == 200
    mids = [m["id"] for m in r.json()["conflicts"]["missions"]]
    assert b in mids


def test_conflict_with_availability_ok():
    c = _client()
    t = _token(c)
    now = datetime.utcnow()
    _mk_mission(c, "A", now + timedelta(hours=5), now + timedelta(hours=6), t)
    inter_id = 123
    _mk_avail(c, inter_id, now + timedelta(hours=1), now + timedelta(hours=3), t)
    body = {
        "start_at": (now + timedelta(hours=2)).isoformat(),
        "end_at": (now + timedelta(hours=2, minutes=30)).isoformat(),
        "intermittent_id": inter_id,
    }
    r = c.post("/planning/check", json=body, headers={"Authorization": f"Bearer {t}"})
    assert r.status_code == 200
    aids = [a["id"] for a in r.json()["conflicts"]["availabilities"]]
    assert len(aids) == 1


def test_no_conflicts_ko_expected_empty():
    c = _client()
    t = _token(c)
    now = datetime.utcnow()
    _mk_mission(c, "A", now + timedelta(hours=1), now + timedelta(hours=2), t)
    body = {
        "start_at": (now + timedelta(hours=3)).isoformat(),
        "end_at": (now + timedelta(hours=4)).isoformat(),
    }
    r = c.post("/planning/check", json=body, headers={"Authorization": f"Bearer {t}"})
    assert r.status_code == 200
    data = r.json()["conflicts"]
    assert data["missions"] == [] and data["availabilities"] == []
