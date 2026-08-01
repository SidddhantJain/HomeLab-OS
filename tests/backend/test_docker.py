import os
import sys
import pytest
from fastapi.testclient import TestClient

os.environ["TESTING"] = "1"
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backend')))

from app.main import app
from app.core.database import Base, engine
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


def test_docker_management_endpoints(client):
    # 1. List containers
    resp = client.get("/api/v1/docker/containers")
    assert resp.status_code == 200
    containers = resp.json()
    assert isinstance(containers, list)
    assert len(containers) > 0

    cid = containers[0]["container_id"]

    # 2. Restart container
    restart_resp = client.post(f"/api/v1/docker/restart/{cid}")
    assert restart_resp.status_code == 200
    assert restart_resp.json()["status"] == "restarted"

    # 3. Get logs
    logs_resp = client.get(f"/api/v1/docker/logs/{cid}")
    assert logs_resp.status_code == 200
    assert "logs" in logs_resp.json()
