"""
HomeLab OS — Backup Scheduler Integration
"""

from __future__ import annotations

from app.core.homelab_core import HomelabCore
from app.core.scheduler import ScheduleMode


def register_backup_schedules() -> None:
    """Register cron tasks for rotation and backup runs with Scheduler."""
    core = HomelabCore.instance()
    scheduler = core.scheduler

    # Execute a clean nightly backup rotation trigger
    def run_nightly_backup_job():
        from app.core.database import SessionLocal
        db = SessionLocal()
        try:
            backup_svc = core.get_service("backup")
            if hasattr(backup_svc, "run_backup"):
                backup_svc.run_backup(db, "Nightly Autocopy", "/opt/homelab/workspaces", "/mnt/homelab-storage/backups")
        except Exception as exc:
            print(f"[BackupScheduler] Scheduled backup job failed: {exc}")
        finally:
            db.close()

    scheduler.register(
        name="Nightly Backup Job",
        service="backup",
        mode=ScheduleMode.INTERVAL,
        interval_seconds=86400,
        callback=run_nightly_backup_job
    )
