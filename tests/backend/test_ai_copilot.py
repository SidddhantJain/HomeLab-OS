from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_ai_copilot_natural_language_query():
    r = client.post("/api/v1/ai/query", params={
        "prompt": "Check external HDD storage health and container logs"
    })
    assert r.status_code == 200
    data = r.json()
    assert "response" in data
    assert "inference_latency_ms" in data
    assert data.get("model") is not None


def test_ai_copilot_container_log_diagnostics():
    r = client.post("/api/v1/ai/diagnose/container", params={
        "container_name": "jellyfin-media-server",
        "log_snippet": "ERROR: socket connection refused on port 8080"
    })
    assert r.status_code == 200
    data = r.json()
    assert "root_cause" in data
    assert "recommended_action" in data
    assert data.get("confidence_score") >= 0.8
