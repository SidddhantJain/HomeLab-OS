from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_nvr_cameras_endpoint():
    r = client.get("/api/v1/nvr/cameras")
    assert r.status_code == 200
    cameras = r.json()
    assert isinstance(cameras, list)
    assert len(cameras) >= 1
    assert "camera_id" in cameras[0]


def test_nvr_ai_events_endpoint():
    r = client.get("/api/v1/nvr/events")
    assert r.status_code == 200
    events = r.json()
    assert isinstance(events, list)
    assert len(events) >= 1
    assert "label" in events[0]
    assert "confidence" in events[0]
