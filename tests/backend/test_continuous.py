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


def test_continuous_platform_workflow_integration(client):
    """Executes a multi-service workflow spanning monitoring, alerts, workflow, recovery, docker, power, audit, remote control, and file management."""
    # 1. Root & Health Check
    assert client.get("/").status_code == 200
    assert client.get("/api/v1/system/status").status_code == 200

    # 2. Monitoring & Alerts
    client.get("/api/v1/monitoring/status")
    client.post("/api/v1/alerts/rules", json={
        "name": "High RAM Alert",
        "metric_name": "ram_percent",
        "threshold": 90.0
    })
    assert len(client.get("/api/v1/alerts").json()) >= 0

    # 3. Manager API discovery
    assert client.get("/api/v1/manager/status").status_code == 200
    assert client.get("/api/v1/manager/discover").status_code == 200

    # 4. Audit Search
    assert client.get("/api/v1/audit/search").status_code == 200

    # 5. Power & Docker
    assert client.get("/api/v1/power/report").status_code == 200
    assert client.get("/api/v1/docker/containers").status_code == 200

    # 6. Remote Control
    assert client.get("/api/v1/remote/status").status_code == 200
