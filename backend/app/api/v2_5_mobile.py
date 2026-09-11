from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
import uuid

router = APIRouter(prefix="/mobile", tags=["Android Native App Companion & WebRTC"])

_paired_devices: Dict[str, Dict[str, Any]] = {
    "dev-pixel7-01": {
        "device_id": "dev-pixel7-01",
        "device_name": "Google Pixel 7 Pro",
        "platform": "Android 14",
        "biometrics_enabled": True,
        "fcm_token": "fcm_token_sample_pixel7_9921",
        "paired_at": "2026-09-11 20:15:00",
        "status": "ONLINE"
    }
}

_dedup_hashes: set[str] = {"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"}


@router.get("/devices", response_model=List[Dict[str, Any]])
def list_paired_mobile_devices():
    """List paired Android mobile companion devices."""
    return list(_paired_devices.values())


@router.post("/pair")
def pair_mobile_device(device_name: str, platform: str, fcm_token: str):
    """Pair a new Android phone/tablet with HomeLab OS server."""
    if not device_name:
        raise HTTPException(status_code=400, detail="device_name parameter is required.")

    dev_id = f"dev-{uuid.uuid4().hex[:6]}"
    record = {
        "device_id": dev_id,
        "device_name": device_name,
        "platform": platform or "Android",
        "biometrics_enabled": True,
        "fcm_token": fcm_token or "fcm_default_token",
        "paired_at": "Just now",
        "status": "ONLINE"
    }
    _paired_devices[dev_id] = record
    return {"status": "PAIRED", "device": record}


@router.post("/deduplicate/check")
def check_media_deduplication(file_hash: str, filename: str):
    """Check if media file SHA-256 hash already exists in storage vault."""
    if not file_hash:
        raise HTTPException(status_code=400, detail="file_hash parameter is required.")

    exists = file_hash in _dedup_hashes
    if not exists:
        _dedup_hashes.add(file_hash)

    return {
        "file_hash": file_hash,
        "filename": filename,
        "already_exists": exists,
        "action": "SKIP_UPLOAD" if exists else "UPLOAD_REQUIRED"
    }


@router.post("/webrtc/signal")
def WebRTC_signal_session(device_id: str, sdp_offer: str):
    """Establish WebRTC P2P remote terminal signaling session."""
    return {
        "status": "CONNECTED",
        "session_id": f"rtc-{uuid.uuid4().hex[:8]}",
        "device_id": device_id,
        "sdp_answer": "v=0\r\no=- 14920 2 IN IP4 192.168.0.180\r\ns=HomeLabOS-WebRTC",
        "ice_servers": [{"urls": "stun:stun.l.google.com:19302"}]
    }
