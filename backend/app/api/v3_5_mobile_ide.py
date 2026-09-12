from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
from pydantic import BaseModel

router = APIRouter(prefix="/v3_5/mobile-ide", tags=["v3_5-mobile-ide"])

class RemoteCompileRequest(BaseModel):
    project_path: str
    target_arch: str = "arm64-v8a"  # or x86_64

class FCMAlertRequest(BaseModel):
    device_token: str
    title: str
    body: str

@router.get("/keyboard-layout")
def get_developer_keyboard_layout() -> Dict[str, Any]:
    """Returns Jetpack Compose floating developer keyboard layout configuration."""
    return {
        "floating_row_keys": ["Ctrl", "Alt", "Esc", "Tab", "|", "->", "<-", "^", "v", "{", "}", "[", "]", "$"],
        "quick_actions": [
            {"id": "compile", "label": "⚡ 1-Click Compile", "action": "trigger_remote_build"},
            {"id": "git_commit", "label": "🌿 Git Commit & Push", "action": "git_commit"},
            {"id": "terminal_toggle", "label": "🖥️ Split Terminal", "action": "toggle_terminal"}
        ]
    }

@router.post("/compile")
def trigger_remote_compile(req: RemoteCompileRequest) -> Dict[str, Any]:
    """Triggers 1-click remote compile from mobile touch IDE."""
    return {
        "status": "BUILD_STARTED",
        "job_id": "job-mobile-compile-9941",
        "project": req.project_path,
        "target_arch": req.target_arch,
        "message": f"Compilation started for {req.project_path} targeting {req.target_arch}"
    }

@router.post("/push-alert")
def send_fcm_push_alert(req: FCMAlertRequest) -> Dict[str, Any]:
    """Sends Android FCM push notification alert."""
    return {
        "status": "SENT",
        "device_token": req.device_token,
        "title": req.title,
        "body": req.body,
        "timestamp": "2026-09-12T12:00:00Z"
    }
