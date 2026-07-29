"""
HomeLab OS — Backup Service

Main coordination class.
"""

from __future__ import annotations

from typing import Any, Dict, List
from sqlalchemy.orm import Session

from app.core.base_service import BaseService
from app.services.backup.manager import BackupManager
from app.services.backup.models import BackupJob
from app.services.backup.scheduler import register_backup_schedules


class BackupService(BaseService):
    """Integrates local/external database backup runs with the Scheduler."""

    def __init__(self) -> None:
        self._manager = BackupManager()

    @property
    def name(self) -> str:
        return "backup"

    def initialize(self) -> None:
        """Register automated schedule tasks."""
        register_backup_schedules()

    def shutdown(self) -> None:
        """Shutdown hook."""
        pass

    def health(self) -> Dict[str, Any]:
        """Telemetry health checks."""
        return {
            "status": "healthy",
            "message": "Backup service is initialized."
        }

    # ------------------------------------------------------------------
    # Backup operations
    # ------------------------------------------------------------------

    def run_backup(self, db: Session, name: str, source: str, destination: str) -> BackupJob:
        """Initiate manual backup copy."""
        return self._manager.run_backup(db, name, source, destination)

    def get_backup_jobs(self, db: Session) -> List[BackupJob]:
        """Fetch historical backup job runs."""
        return db.query(BackupJob).all()
