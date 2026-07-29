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


def test_list_storage_devices(client):
    response = client.get("/api/v1/storage/devices")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2
    assert "name" in data[0]
    assert "uuid" in data[0]
    assert "capacity_gb" in data[0]


def test_get_device_details(client):
    # Retrieve devices first to extract ID
    list_res = client.get("/api/v1/storage/devices")
    assert list_res.status_code == 200
    devices = list_res.json()
    device_id = devices[0]["id"]

    detail_res = client.get(f"/api/v1/storage/devices/{device_id}")
    assert detail_res.status_code == 200
    details = detail_res.json()
    assert details["id"] == device_id
    assert "filesystem" in details


def test_get_storage_health(client):
    response = client.get("/api/v1/storage/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "records" in data


def test_mount_unmount_storage(client):
    list_res = client.get("/api/v1/storage/devices")
    devices = list_res.json()
    device_id = devices[1]["id"]  # Mount the virtual external HDD

    # Mount
    mount_res = client.post(
        f"/api/v1/storage/mount/{device_id}",
        params={"mount_point": "/mnt/homelab-storage"}
    )
    assert mount_res.status_code == 200
    assert mount_res.json()["status"] == "mounted"

    # Unmount
    unmount_res = client.post(f"/api/v1/storage/unmount/{device_id}")
    assert unmount_res.status_code == 200
    assert unmount_res.json()["status"] == "unmounted"
