import os

from fastapi.testclient import TestClient

from app.main import create_app
from app.settings import get_settings


def setup_module(_m):
    # Isoler le cache settings pour ce module
    try:
        get_settings.cache_clear()  # type: ignore[attr-defined]
    except Exception:
        pass


def _make_client():
    # Config de test
    os.environ["ADMIN_EMAIL"] = "admin@example.com"
    os.environ["ADMIN_PASSWORD"] = "s3cret"
    os.environ["JWT_SECRET"] = "unit-test-secret"
    try:
        get_settings.cache_clear()  # type: ignore[attr-defined]
    except Exception:
        pass
    app = create_app()
    return TestClient(app)


def test_login_ok_and_me_ok():
    c = _make_client()
    r = c.post("/auth/token", data={"username": "admin@example.com", "password": "s3cret"})
    assert r.status_code == 200, r.text
    token = r.json()["access_token"]
    r2 = c.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert r2.status_code == 200
    assert r2.json()["email"] == "admin@example.com"


def test_login_wrong_password_401():
    c = _make_client()
    r = c.post("/auth/token", data={"username": "admin@example.com", "password": "bad"})
    assert r.status_code == 401
    assert "invalid" in r.text.lower() or "identifiants" in r.text.lower()


def test_me_unauthorized_401():
    c = _make_client()
    r = c.get("/auth/me")
    assert r.status_code == 401
