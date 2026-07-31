import os
import sys
import pytest
from fastapi.testclient import TestClient

os.environ["TESTING"] = "1"
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backend')))

from app.main import app
from app.core.database import Base, engine, SessionLocal
from app.core.homelab_core import HomelabCore


@pytest.fixture(autouse=True)
def setup_test_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    HomelabCore.reset()
    with TestClient(app) as c:
        yield c


def test_download_queuing(client):
    db = SessionLocal()
    try:
        resp = client.post("/api/v1/downloads", json={
            "url": "https://example.com/file.zip",
            "destination": "/opt/homelab/downloads"
        })
        assert resp.status_code == 200
        task_id = resp.json()["id"]

        list_resp = client.get("/api/v1/downloads")
        assert list_resp.status_code == 200
        assert any(t["id"] == task_id for t in list_resp.json())

    finally:
        db.close()
