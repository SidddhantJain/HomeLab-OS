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


def test_workflow_creation_and_execution(client):
    # 1. Create workflow
    resp = client.post("/api/v1/workflow", json={
        "name": "Auto Cleanup Workflow",
        "trigger_type": "threshold",
        "actions": [{"name": "cleanup"}],
        "conditions": {"field": "disk_percent", "operator": ">", "value": 80.0}
    })
    assert resp.status_code == 200
    wf_data = resp.json()
    assert wf_data["name"] == "Auto Cleanup Workflow"
    wf_id = wf_data["id"]

    # 2. List workflows
    list_resp = client.get("/api/v1/workflow")
    assert list_resp.status_code == 200
    assert any(w["id"] == wf_id for w in list_resp.json())

    # 3. Execute workflow
    exec_resp = client.post(f"/api/v1/workflow/{wf_id}/execute")
    assert exec_resp.status_code == 200
    assert exec_resp.json()["status"] == "SUCCESS"
