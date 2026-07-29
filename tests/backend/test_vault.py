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


def test_vault_initial_status_is_locked(client):
    response = client.get("/api/v1/vault/status")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "LOCKED"
    assert data["mount_location"] == "/mnt/vault"


def test_vault_unlock_and_lock_lifecycle(client):
    # Unlock vault
    unlock_res = client.post("/api/v1/vault/unlock", json={"password": "securepassword"})
    assert unlock_res.status_code == 200
    assert unlock_res.json()["status"] == "unlocked"

    # Verify status is UNLOCKED
    status_res = client.get("/api/v1/vault/status")
    assert status_res.status_code == 200
    assert status_res.json()["status"] == "UNLOCKED"

    # Lock vault
    lock_res = client.post("/api/v1/vault/lock")
    assert lock_res.status_code == 200
    assert lock_res.json()["status"] == "locked"

    # Verify status is LOCKED again
    status_res_2 = client.get("/api/v1/vault/status")
    assert status_res_2.json()["status"] == "LOCKED"
