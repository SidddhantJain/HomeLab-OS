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


def test_disaster_recovery_test_run(client):
    # 1. Run restore test
    resp = client.post("/api/v1/recovery/test", json={
        "backup_id": "backup-test-001",
        "file_path": "/opt/homelab/backups/latest.tar.gz"
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["backup_id"] == "backup-test-001"
    assert data["validation_status"] == "PASSED"

    # 2. Get history
    hist_resp = client.get("/api/v1/recovery/history")
    assert hist_resp.status_code == 200
    assert len(hist_resp.json()) > 0
