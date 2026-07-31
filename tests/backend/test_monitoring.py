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


def test_monitoring_endpoints(client):
    # 1. Query status
    status_resp = client.get("/api/v1/monitoring/status")
    assert status_resp.status_code == 200
    data = status_resp.json()
    assert "cpu_percent" in data
    assert "ram_percent" in data

    # 2. Query history
    hist_resp = client.get("/api/v1/monitoring/history?metric_name=cpu_percent")
    assert hist_resp.status_code == 200
    assert isinstance(hist_resp.json(), list)

    # 3. Query monitored services
    svc_resp = client.get("/api/v1/monitoring/services")
    assert svc_resp.status_code == 200
    assert len(svc_resp.json()) > 0

    # 4. Set custom threshold
    thresh_resp = client.post("/api/v1/monitoring/threshold", json={
        "metric_name": "cpu_percent",
        "limit": 85.0
    })
    assert thresh_resp.status_code == 200
    assert thresh_resp.json()["new_threshold"] == 85.0
