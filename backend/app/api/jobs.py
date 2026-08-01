from fastapi import APIRouter, Depends
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.homelab_core import HomelabCore
from app.services.jobs.service import JobService

router = APIRouter(prefix="/jobs", tags=["Background Job Center"])


def get_job_service() -> JobService:
    return HomelabCore.instance().get_service("jobs")


@router.get("")
def list_background_jobs(
    db: Session = Depends(get_db),
    service: JobService = Depends(get_job_service)
):
    jobs = service.list_jobs(db)
    return [
        {
            "id": j.id,
            "name": j.name,
            "job_type": j.job_type,
            "status": j.status,
            "progress_pct": j.progress_pct,
            "created_at": j.created_at
        } for j in jobs
    ]
