from fastapi.testclient import TestClient
from main import app

def test_health():
    with TestClient(app) as client:
        r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}

def test_missing_profile_returns_404():
    with TestClient(app) as client:
        r = client.get("/profiles/999999")
        assert r.status_code == 404

def test_upload_rejects_non_pdf():
    with TestClient(app) as client:
        files = {"file": ("notes.txt", b"hello", "text/plain")}
        r = client.post("/upload_cv", files=files)
        assert r.status_code ==400
