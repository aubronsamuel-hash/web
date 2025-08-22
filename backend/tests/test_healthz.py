from fastapi.testclient import TestClient

from app.main import app
from app.settings import get_settings

client = TestClient(app)


def test_healthz_ok() -> None:
    r = client.get("/healthz")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}
    rid_header = get_settings().request_id_header
    assert r.headers.get(rid_header)


def test_healthz_ko_404() -> None:
    r = client.get("/health")
    assert r.status_code == 404
    data = r.json()
    assert "detail" in data
