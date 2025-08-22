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


def test_intermittents_create_get_delete_ok():
    c = _make_client()
    token = _login_token(c)
    auth = {"Authorization": f"Bearer {token}"}
    r = c.post(
        "/intermittents",
        json={"first_name": "John", "last_name": "Doe", "skills": "guitar"},
        headers=auth,
    )
    assert r.status_code == 201, r.text
    iid = r.json()["id"]
    r2 = c.get(f"/intermittents/{iid}", headers=auth)
    assert r2.status_code == 200
    r3 = c.delete(f"/intermittents/{iid}", headers=auth)
    assert r3.status_code == 204
    r4 = c.get(f"/intermittents/{iid}", headers=auth)
    assert r4.status_code == 404


def test_intermittents_list_filters_pagination_ok():
    c = _make_client()
    token = _login_token(c)
    auth = {"Authorization": f"Bearer {token}"}
    data = [
        {"first_name": "John", "last_name": "Doe", "skills": "guitar,drums"},
        {
            "first_name": "Jane",
            "last_name": "Smith",
            "is_active": False,
            "skills": "piano",
        },
        {"first_name": "Jack", "last_name": "Johnson", "skills": "guitar"},
    ]
    for p in data:
        c.post("/intermittents", json=p, headers=auth)
    for i in range(20):
        c.post(
            "/intermittents",
            json={"first_name": f"F{i}", "last_name": f"L{i}"},
            headers=auth,
        )
    r = c.get("/intermittents?q=son", headers=auth)
    assert r.status_code == 200
    assert len(r.json()["items"]) == 1
    r = c.get("/intermittents?active=false", headers=auth)
    assert r.status_code == 200
    assert len(r.json()["items"]) == 1 and r.json()["items"][0]["first_name"] == "Jane"
    r = c.get("/intermittents?skill=guitar", headers=auth)
    assert r.status_code == 200
    names = {i["first_name"] for i in r.json()["items"]}
    assert names == {"John", "Jack"}
    r = c.get("/intermittents?page=2&size=10", headers=auth)
    assert r.status_code == 200
    assert r.json()["page"] == 2 and len(r.json()["items"]) == 10


def test_intermittents_duplicate_409():
    c = _make_client()
    token = _login_token(c)
    auth = {"Authorization": f"Bearer {token}"}
    payload = {"first_name": "Dup", "last_name": "Lee"}
    c.post("/intermittents", json=payload, headers=auth)
    r = c.post("/intermittents", json=payload, headers=auth)
    assert r.status_code == 409


def test_intermittents_not_found_404():
    c = _make_client()
    token = _login_token(c)
    r = c.get("/intermittents/9999", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 404
