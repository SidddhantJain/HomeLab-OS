from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_live_migration_start_and_status():
    r = client.post("/api/v1/cluster/migration/start", params={
        "workload_id": "test-jellyfin-container",
        "target_node_ip": "192.168.0.185",
        "workload_type": "container"
    })
    assert r.status_code == 200
    data = r.json()
    assert "migration_id" in data
    assert data.get("workload_id") == "test-jellyfin-container"
    assert data.get("status") in ["IN_PROGRESS", "COMPLETED"]

    mig_id = data.get("migration_id")
    r2 = client.get(f"/api/v1/cluster/migration/status/{mig_id}")
    assert r2.status_code == 200
    data2 = r2.json()
    assert data2.get("migration_id") == mig_id


def test_live_migration_list():
    r = client.get("/api/v1/cluster/migration/list")
    assert r.status_code == 200
    assert isinstance(r.json(), list)
