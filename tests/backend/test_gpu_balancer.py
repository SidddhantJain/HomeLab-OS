from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_gpu_balancer_status_endpoint():
    r = client.get("/api/v1/gpu/status")
    assert r.status_code == 200
    data = r.json()
    assert "quicksync" in data
    assert "nvenc" in data
    assert "active_balancer_mode" in data


def test_gpu_balancer_route_task():
    r = client.post("/api/v1/gpu/transcode/route", params={
        "video_file": "sample_video_4k.mkv",
        "target_codec": "h264"
    })
    assert r.status_code == 200
    data = r.json()
    assert data.get("status") == "routed"
    assert "assigned_encoder" in data
    assert "ffmpeg_encoder_flag" in data
