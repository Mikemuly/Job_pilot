import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool

from main import app
from database import get_session
from models import Profile, Job

@pytest.fixture
def client():
    engine = create_engine(
        "sqlite://",
        connect_args= {"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    
    def override():
        with Session(engine) as session:
            yield session
            
    app.dependency_overrides[get_session] = override
    
    with Session(engine) as s:
        s.add(Profile(full_name="Test", email="t@example.com", skills="python"))
        s.add(Job(source_id="1", title="Dev", company="Acme", url="http://x"))
        s.commit()
        
    with TestClient(app) as c:
        yield c
        
    app.dependency_overrides.clear()
    
def test_create_application(client):
    r = client.post("/applications", params={"profile_id": 1, "job_id": 1})
    assert r.status_code == 200
    assert r.json()["status"] == "approved"
    
def test_duplicate_application_rejected(client):
    client.post("/applications", params={"profile_id": 1, "job_id": 1})
    r = client.post("/applications", params={"profile_id": 1, "job_id": 1})
    assert r.status_code == 409
    
def test_update_status(client):
    client.post("/applications", params={"profile_id": 1, "job_id": 1})
    r = client.patch("/applications/1", params={"status": "applied"})
    assert r.status_code == 200
    assert r.json()["status"]  == "applied"
    
def test_invalid_status_rejected(client):
    client.post("/applications", params={"profile_id": 1, "job_id": 1})
    r = client.patch("/applications/1", params={"status": "banana"})
    assert r.status_code == 400 
