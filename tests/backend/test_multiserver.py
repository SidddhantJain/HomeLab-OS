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


def test_multiserver_list_and_add(client):
    # 1. List
    resp = client.get("/api/v1/multiserver")
    assert resp.status_code == 200
    servers = resp.json()
    assert len(servers) >= 1

    # 2. Add
    add_resp = client.post("/api/v1/multiserver", json={
        "name": "Secondary Office Server",
        "host": "192.168.1.200",
        "port": 8000
    })
    assert add_resp.status_code == 200
    assert add_resp.json()["name"] == "Secondary Office Server"
