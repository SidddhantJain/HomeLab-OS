from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Dict, Any
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.homelab_core import HomelabCore
from app.services.sync.service import SyncService

router = APIRouter(prefix="/sync", tags=["Synchronization Layer"])


class SyncReq(BaseModel):
    device_id: str
    sync_key: str
    payload: Dict[str, Any]


def get_sync_service() -> SyncService:
    return HomelabCore.instance().get_service("sync")


@router.post("")
def sync_device_state(
    req: SyncReq,
    db: Session = Depends(get_db),
    service: SyncService = Depends(get_sync_service)
):
    return service.sync_payload(db, req.device_id, req.sync_key, req.payload)
