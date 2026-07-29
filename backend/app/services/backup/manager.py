"""
HomeLab OS — Backup Manager

Coordinates local, external disk, and network backup targets.
"""

from __future__ import annotations

from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models.backup import BackupJob
from app.core.homelab_core import HomelabCore
from app.core.event_bus import Event
from app.services.backup.events import BackupEvents


class BackupManager:
    """Orchestrates backup executions and metadata updates."""

    def __init__(self) -> None:
        pass

    def run_backup(self, db: Session, name: str, source: str, destination: str) -> BackupJob:
        """Initialize and run a backup transaction copy."""
        job = BackupJob(
            name=name,
            source=source,
            destination=destination,
            status="RUNNING"
        )
        db.add(job)
        db.commit()
        db.refresh(job)

        core = HomelabCore.instance()
        core.event_bus.publish(
            Event(
                name=BackupEvents.STARTED,
                source="backup_manager",
                payload={"job_id": job.id, "name": name}
            )
        )

        # Mock work process
        job.status = "COMPLETED"
        job.completed_at = datetime.now(timezone.utc)
        db.commit()

        core.event_bus.publish(
            Event(
                name=BackupEvents.COMPLETED,
                source="backup_manager",
                payload={"job_id": job.id, "name": name}
            )
        )
        return job
