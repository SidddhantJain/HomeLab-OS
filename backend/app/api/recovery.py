from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from app.core.homelab_core import HomelabCore
from app.services.disaster_recovery.service import DisasterRecoveryService

router = APIRouter(prefix="/recovery", tags=["Disaster Recovery"])


class RecoveryTestRequest(BaseModel):
    backup_id: str
    file_path: Optional[str] = "/opt/homelab/backups/latest.tar.gz"


def get_recovery_service() -> DisasterRecoveryService:
    return HomelabCore.instance().get_service("disaster_recovery")


@router.post("/test")
def run_recovery_test(
    req: RecoveryTestRequest,
    service: DisasterRecoveryService = Depends(get_recovery_service)
):
    try:
        return service.run_restore_test(req.backup_id, req.file_path)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/history")
def get_recovery_history(
    service: DisasterRecoveryService = Depends(get_recovery_service)
):
    return service.get_test_history()
