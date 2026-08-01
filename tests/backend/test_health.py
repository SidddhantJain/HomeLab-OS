import os
import sys
import pytest
from fastapi.testclient import TestClient

os.environ["TESTING"] = "1"
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backend')))

from app.main import app
from app.core.homelab_core import HomelabCore


@pytest.fixture
def client():
    HomelabCore.reset()
    with TestClient(app) as c:
        yield c


def test_health_summary_endpoint(client):
    resp = client.get("/api/v1/health/summary")
    assert resp.status_code == 200
    res = resp.json()
    assert res["overall_health_score"] >= 90
    assert "metrics" in res
