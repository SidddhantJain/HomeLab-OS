from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.homelab_core import HomelabCore
from app.services.backup.service import BackupService

router = APIRouter(prefix="/backup", tags=["Backups"])


class BackupCreate(BaseModel):
    name: str
    source: str
    destination: str


def get_backup_service() -> BackupService:
    return HomelabCore.instance().get_service("backup")


@router.get("/jobs")
def list_backup_jobs(
    db: Session = Depends(get_db),
    service: BackupService = Depends(get_backup_service)
):
    jobs = service.get_backup_jobs(db)
    return [
        {
            "id": j.id,
            "name": j.name,
            "source": j.source,
            "destination": j.destination,
            "status": j.status,
            "created_at": j.created_at,
            "completed_at": j.completed_at
        } for j in jobs
    ]


@router.post("/jobs")
def trigger_backup(
    req: BackupCreate,
    db: Session = Depends(get_db),
    service: BackupService = Depends(get_backup_service)
):
    try:
        return service.run_backup(db, req.name, req.source, req.destination)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
