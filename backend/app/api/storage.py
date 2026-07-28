from fastapi import APIRouter
from typing import List, Dict, Any

router = APIRouter(prefix="/storage", tags=["Storage Management"])


@router.get("/devices")
def list_storage_devices() -> List[Dict[str, Any]]:
    return [
        {
            "id": "dev-ssd-1",
            "name": "Internal SSD",
            "mount_point": "/",
            "filesystem": "ext4",
            "capacity_gb": 240,
            "free_space_gb": 165,
            "type": "SSD",
            "health": "GOOD"
        },
        {
            "id": "dev-hdd-1",
            "name": "External Storage HDD",
            "mount_point": "/mnt/storage",
            "filesystem": "ext4",
            "capacity_gb": 1000,
            "free_space_gb": 850,
            "type": "HDD",
            "health": "GOOD"
        }
    ]


@router.get("/health")
def get_storage_health():
    return {
        "status": "healthy",
        "ssd_smart": "PASSED",
        "hdd_smart": "PASSED",
        "temp_c": 38
    }


@router.post("/mount")
def mount_storage(device_id: str):
    return {
        "status": "mounted",
        "device_id": device_id,
        "message": f"Storage device {device_id} successfully mounted."
    }
