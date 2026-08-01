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


def test_alert_rules_and_evaluation(client):
    # 1. Create alert rule
    rule_resp = client.post("/api/v1/alerts/rules", json={
        "name": "High CPU Alert",
        "metric_name": "cpu_percent",
        "threshold": 80.0,
        "comparison": ">",
        "severity": "CRITICAL"
    })
    assert rule_resp.status_code == 200
    rule_data = rule_resp.json()
    assert rule_data["metric_name"] == "cpu_percent"

    # 2. Query alerts
    alerts_resp = client.get("/api/v1/alerts")
    assert alerts_resp.status_code == 200
    assert isinstance(alerts_resp.json(), list)
