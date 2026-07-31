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


def test_projects_registry(client):
    db = SessionLocal()
    try:
        # Create project
        resp = client.post("/api/v1/projects", json={
            "name": "Integration Project",
            "path": ".",
            "description": "Local codebase inspection"
        })
        assert resp.status_code == 200
        p_data = resp.json()
        assert p_data["name"] == "Integration Project"
        proj_id = p_data["id"]

        # List projects
        list_resp = client.get("/api/v1/projects")
        assert list_resp.status_code == 200
        list_data = list_resp.json()
        assert any(p["id"] == proj_id for p in list_data)

    finally:
        db.close()
