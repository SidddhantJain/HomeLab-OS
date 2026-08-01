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


def test_network_discovery_and_inventory(client):
    # 1. Devices list
    dev_resp = client.get("/api/v1/network/devices")
    assert dev_resp.status_code == 200
    devices = dev_resp.json()
    assert isinstance(devices, list)
    assert len(devices) > 0

    mac = devices[0]["mac_address"]

    # 2. Friendly name assignment
    alias_resp = client.post("/api/v1/network/devices/friendly-name", json={
        "mac_address": mac,
        "friendly_name": "Living Room Router"
    })
    assert alias_resp.status_code == 200
    assert alias_resp.json()["friendly_name"] == "Living Room Router"

    # 3. Actions
    ping_resp = client.post("/api/v1/network/actions/ping", json={"target": "192.168.1.1"})
    assert ping_resp.status_code == 200
    assert ping_resp.json()["status"] == "online"

    wol_resp = client.post("/api/v1/network/actions/wol", json={"target": "00:11:22:33:44:55"})
    assert wol_resp.status_code == 200
    assert wol_resp.json()["status"] == "sent"
