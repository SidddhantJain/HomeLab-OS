import os
import sys
import pytest
from fastapi.testclient import TestClient

os.environ["TESTING"] = "1"
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backend')))

from app.main import app
from app.core.database import Base, engine, SessionLocal
from app.core.homelab_core import HomelabCore
from app.models.snapshot import Snapshot
from app.services.projects.snapshot.manager import SnapshotManager


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


def test_snapshots_retention_and_restorations(client):
    db = SessionLocal()
    try:
        # Register a project first
        p_resp = client.post("/api/v1/projects", json={
            "name": "Snap Test",
            "path": ".",
            "description": "Virtual snapshots base"
        })
        proj_id = p_resp.json()["id"]

        # Create snapshots
        snap_resp = client.post(f"/api/v1/projects/{proj_id}/snapshot")
        assert snap_resp.status_code == 200
        snap_id = snap_resp.json()["snapshot_id"]

        # Get snapshots
        list_resp = client.get(f"/api/v1/projects/{proj_id}/snapshots")
        assert list_resp.status_code == 200
        assert len(list_resp.json()) > 0

        # Restore snapshot
        rest_resp = client.post(f"/api/v1/projects/snapshots/{snap_id}/restore")
        assert rest_resp.status_code == 200
        assert rest_resp.json()["status"] == "restored"

        # Verify retention policy logic (limit = 3)
        manager = SnapshotManager(keep_snapshots_limit=3)
        for _ in range(5):
            manager.create_snapshot(db, "fake-workspace")

        snaps = db.query(Snapshot).filter(Snapshot.workspace_id == "fake-workspace").all()
        assert len(snaps) <= 3

    finally:
        db.close()
