from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_mobile_companion_device_pairing_and_list():
    r = client.post("/api/v1/mobile/pair", params={
        "device_name": "Samsung Galaxy S24 Ultra",
        "platform": "Android 14",
        "fcm_token": "fcm_token_s24_sample"
    })
    assert r.status_code == 200
    data = r.json()
    assert data.get("status") == "PAIRED"
    assert "device_id" in data.get("device", {})

    r2 = client.get("/api/v1/mobile/devices")
    assert r2.status_code == 200
    assert isinstance(r2.json(), list)
    assert len(r2.json()) >= 1


def test_mobile_media_deduplication():
    r = client.post("/api/v1/mobile/deduplicate/check", params={
        "file_hash": "a1b2c3d4e5f67890123456789abcdef0123456789abcdef0123456789abcdef0",
        "filename": "photo_2026_09_11.jpg"
    })
    assert r.status_code == 200
    data = r.json()
    assert "already_exists" in data
    assert data.get("action") in ["UPLOAD_REQUIRED", "SKIP_UPLOAD"]


def test_webrtc_remote_terminal_signaling():
    r = client.post("/api/v1/mobile/webrtc/signal", params={
        "device_id": "dev-pixel7-01",
        "sdp_offer": "sample_sdp_offer_data"
    })
    assert r.status_code == 200
    data = r.json()
    assert data.get("status") == "CONNECTED"
    assert "sdp_answer" in data
    assert "ice_servers" in data
