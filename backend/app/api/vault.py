from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.homelab_core import HomelabCore
from app.services.vault.service import VaultService

router = APIRouter(prefix="/vault", tags=["Private Vault"])


class UnlockRequest(BaseModel):
    password: str


def get_vault_service() -> VaultService:
    core = HomelabCore.instance()
    return core.get_service("vault")


@router.get("/status")
def get_vault_status(
    db: Session = Depends(get_db),
    service: VaultService = Depends(get_vault_service)
) -> Dict[str, Any]:
    return service.get_vault_status(db)


@router.post("/unlock")
def unlock_vault(
    req: UnlockRequest,
    db: Session = Depends(get_db),
    service: VaultService = Depends(get_vault_service)
):
    res = service.unlock_vault(db, req.password)
    if res.get("status") == "locked":
        raise HTTPException(status_code=400, detail=res.get("message"))
    return res


@router.post("/lock")
def lock_vault(
    db: Session = Depends(get_db),
    service: VaultService = Depends(get_vault_service)
):
    res = service.lock_vault(db)
    if res.get("status") == "unlocked":
        raise HTTPException(status_code=500, detail=res.get("message"))
    return res

