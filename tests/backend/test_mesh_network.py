from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_mesh_network_status_endpoint():
    r = client.get("/api/v1/mesh/status")
    assert r.status_code == 200
    data = r.json()
    assert data.get("mesh_status") == "ACTIVE"
    assert "peers" in data
    assert isinstance(data.get("peers"), list)


def test_mesh_network_add_peer():
    r = client.post("/api/v1/mesh/peer/add", params={
        "device_name": "Pixel 8 Pro Mobile Node",
        "public_key": "wg_pk_pixel8_sample_9921="
    })
    assert r.status_code == 200
    data = r.json()
    assert "peer_id" in data
    assert data.get("device_name") == "Pixel 8 Pro Mobile Node"
    assert "mesh_ip" in data
