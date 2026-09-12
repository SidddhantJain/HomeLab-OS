import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.hardware.federation import federation_hal

client = TestClient(app)

def test_federation_hal_status():
    status = federation_hal.get_federation_status()
    assert "Sovereign P2P Federation" in status["engine"]
    assert status["active_nodes_count"] >= 1
    assert status["quantum_crypto"]["pqc_enabled"] is True
    assert status["ai_agents_count"] >= 1

def test_federation_p2p_node_pairing():
    # Pair new node
    new_node = federation_hal.pair_node(
        name="Test-Offsite-Node",
        owner="Unit Test Owner",
        ip_address="100.64.0.99",
        shared_quota_tb=8.0
    )
    assert new_node["name"] == "Test-Offsite-Node"
    assert new_node["quantum_encrypted"] is True
    assert new_node["status"] == "CONNECTED"

def test_federation_quantum_crypto_and_ai_agents():
    q_info = federation_hal.get_quantum_crypto_info()
    assert "Kyber-1024" in q_info["kem_algorithm"]
    assert "Dilithium-5" in q_info["signature_algorithm"]

    agents = federation_hal.list_ai_agents()
    assert len(agents) > 0

    triggered = federation_hal.trigger_agent_task(
        agent_id="agent-diagnostician",
        task_name="Run ZFS Bitrot Repair Sweep"
    )
    assert triggered["status"] == "EXECUTING"

def test_federation_api_endpoints():
    # GET status
    r = client.get("/api/v1/v5/federation/status")
    assert r.status_code == 200
    assert r.json()["quantum_crypto"]["pqc_enabled"] is True

    # GET nodes
    r = client.get("/api/v1/v5/federation/nodes")
    assert r.status_code == 200
    assert isinstance(r.json(), list)

    # POST nodes/pair
    payload = {"name": "API-Node-Gamma", "owner": "API Test", "ip_address": "100.64.0.120", "shared_quota_tb": 4.0}
    r = client.post("/api/v1/v5/federation/nodes/pair", json=payload)
    assert r.status_code == 200
    assert r.json()["name"] == "API-Node-Gamma"

    # GET quantum-crypto
    r = client.get("/api/v1/v5/federation/quantum-crypto")
    assert r.status_code == 200

    # GET ai-agents
    r = client.get("/api/v1/v5/federation/ai-agents")
    assert r.status_code == 200

    # POST ai-agents/trigger
    r = client.post("/api/v1/v5/federation/ai-agents/trigger", json={"agent_id": "agent-security", "task_name": "Rotate Kyber Public Keys"})
    assert r.status_code == 200
    assert r.json()["status"] == "EXECUTING"
