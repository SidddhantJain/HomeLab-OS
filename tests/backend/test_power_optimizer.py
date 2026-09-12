from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_power_optimizer_metrics_endpoint():
    r = client.get("/api/v1/power/optimizer/metrics")
    assert r.status_code == 200
    data = r.json()
    assert "power_source" in data
    assert "cpu_temperature_celsius" in data
    assert "active_policy" in data


def test_power_optimizer_set_policy():
    r = client.post("/api/v1/power/optimizer/policy/set", params={
        "policy_name": "ECO_SOLAR_MODE"
    })
    assert r.status_code == 200
    data = r.json()
    assert data.get("status") == "UPDATED"
    assert data.get("policy") == "ECO_SOLAR_MODE"
