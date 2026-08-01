import os
import sys
import time
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


def test_api_response_latency_benchmark(client):
    start = time.time()
    resp = client.get("/api/v1/system/status")
    duration = time.time() - start
    assert resp.status_code == 200
    assert duration < 0.500  # API response should be faster than 500ms
