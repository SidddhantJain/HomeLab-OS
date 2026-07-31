import os
import sys
import pytest
from fastapi.testclient import TestClient

os.environ["TESTING"] = "1"
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backend')))

from app.main import app
from app.core.database import Base, engine, SessionLocal
from app.core.homelab_core import HomelabCore
from app.models.workspace import Workspace


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


def test_workspace_lifecycle(client):
    db = SessionLocal()
    try:
        # 1. Create workspace
        resp = client.post("/api/v1/workspaces", json={
            "name": "test_space",
            "owner": "developer",
            "description": "Test integration workspace"
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["name"] == "test_space"
        ws_id = data["id"]

        # 2. Get workspaces
        list_resp = client.get("/api/v1/workspaces")
        assert list_resp.status_code == 200
        list_data = list_resp.json()
        assert any(w["id"] == ws_id for w in list_data)

        # 3. Archive
        arch_resp = client.post(f"/api/v1/workspaces/{ws_id}/archive")
        assert arch_resp.status_code == 200
        assert arch_resp.json()["status"] == "archived"

        # 4. Restore
        rest_resp = client.post(f"/api/v1/workspaces/{ws_id}/restore")
        assert rest_resp.status_code == 200
        assert rest_resp.json()["status"] == "active"

        # 5. Delete
        del_resp = client.delete(f"/api/v1/workspaces/{ws_id}")
        assert del_resp.status_code == 200
        assert del_resp.json()["status"] == "deleted"

    finally:
        db.close()
