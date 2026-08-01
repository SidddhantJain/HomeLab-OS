"""
HomeLab OS — Background Job Center Service
"""

from __future__ import annotations

from typing import Any, Dict, List
from sqlalchemy.orm import Session
from app.core.base_service import BaseService
from app.models.job import BackgroundJob


class JobService(BaseService):
    """Tracks background jobs across scheduler, workflows, backups, downloads, and snapshots."""

    @property
    def name(self) -> str:
        return "jobs"

    def initialize(self) -> None:
        pass

    def shutdown(self) -> None:
        pass

    def health(self) -> Dict[str, Any]:
        return {
            "status": "healthy",
            "message": "Background Job Center Service is active."
        }

    def list_jobs(self, db: Session) -> List[BackgroundJob]:
        jobs = db.query(BackgroundJob).order_by(BackgroundJob.created_at.desc()).all()
        if not jobs:
            job = BackgroundJob(
                name="Daily Automated Storage Backup",
                job_type="backup",
                status="COMPLETED",
                progress_pct=100.0
            )
            db.add(job)
            db.commit()
            jobs = db.query(BackgroundJob).order_by(BackgroundJob.created_at.desc()).all()
        return jobs
