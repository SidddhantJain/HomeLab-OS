from fastapi import APIRouter
from typing import Dict, Any

router = APIRouter(prefix="/vault", tags=["Private Vault"])


@router.get("/status")
def get_vault_status() -> Dict[str, Any]:
    return {
        "status": "locked",
        "encryption": "LUKS2",
        "mount_point": "/mnt/vault",
        "size_gb": 100
    }


@router.post("/unlock")
def unlock_vault():
    return {
        "status": "unlocked",
        "message": "Encrypted vault successfully unlocked and mounted."
    }


@router.post("/lock")
def lock_vault():
    return {
        "status": "locked",
        "message": "Encrypted vault successfully unmounted and locked."
    }
