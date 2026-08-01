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


def test_remote_control_and_filemanager(client):
    # 1. Remote status
    st_resp = client.get("/api/v1/remote/status")
    assert st_resp.status_code == 200
    assert st_resp.json()["status"] == "running"

    # 2. Remote command
    cmd_resp = client.post("/api/v1/remote/command", json={"command": "lock_vault"})
    assert cmd_resp.status_code == 200
    assert cmd_resp.json()["status"] == "COMPLETED"

    # 3. Terminal command execution
    term_resp = client.post("/api/v1/remote/terminal", json={"command": "ls -la"})
    assert term_resp.status_code == 200
    assert term_resp.json()["status"] == "SUCCESS"

    # 4. Terminal forbidden pattern check
    bad_term = client.post("/api/v1/remote/terminal", json={"command": "rm -rf /"})
    assert bad_term.status_code == 200
    assert bad_term.json()["status"] == "REJECTED"

    # 5. File manager browse
    fm_resp = client.get("/api/v1/filemanager/browse?path=/projects")
    assert fm_resp.status_code == 200
    assert isinstance(fm_resp.json(), list)

    # 6. File manager forbidden path check
    bad_fm = client.get("/api/v1/filemanager/browse?path=/etc/shadow")
    assert bad_fm.status_code == 403

    # 7. File manager operation
    op_resp = client.post("/api/v1/filemanager/operation", json={
        "operation_type": "download",
        "file_path": "/projects/readme.md"
    })
    assert op_resp.status_code == 200
    assert op_resp.json()["status"] == "SUCCESS"
