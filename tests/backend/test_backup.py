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


def test_backup_runs(client):
    db = SessionLocal()
    try:
        resp = client.post("/api/v1/backup/jobs", json={
            "name": "Manual run 1",
            "source": "/opt/workspaces",
            "destination": "/mnt/storage"
        })
        assert resp.status_code == 200
        job_id = resp.json()["id"]

        list_resp = client.get("/api/v1/backup/jobs")
        assert list_resp.status_code == 200
        assert any(j["id"] == job_id for j in list_resp.json())

    finally:
        db.close()
