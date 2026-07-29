"""
HomeLab OS — Scheduler Framework

Provides a centralised job scheduler that services register tasks into.
Supports interval-based, cron-based, and one-shot scheduling modes.
The scheduler is lifecycle-aware — it pauses during MAINTENANCE, BACKUP,
and UPDATING server states.

Design note: this is the framework skeleton.  Actual scheduling is backed
by ``asyncio`` tasks or an ``APScheduler``-like library in production.
"""

from __future__ import annotations

import enum
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable, Optional


class ScheduleMode(str, enum.Enum):
    """How a scheduled job should recur."""

    INTERVAL = "interval"  # repeat every N seconds
    CRON = "cron"          # cron-style expression
    ONE_SHOT = "one_shot"  # run once at a specific time


@dataclass
class ScheduledJob:
    """Metadata for a registered scheduled job."""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    service: str = ""
    mode: ScheduleMode = ScheduleMode.INTERVAL
    interval_seconds: Optional[int] = None
    cron_expression: Optional[str] = None
    run_at: Optional[datetime] = None
    enabled: bool = True
    last_run: Optional[datetime] = None
    next_run: Optional[datetime] = None
    run_count: int = 0


class Scheduler:
    """Central job scheduler for HomeLab OS.

    Usage:
        scheduler = Scheduler()
        job = scheduler.register(
            name="health_check",
            service="monitoring",
            mode=ScheduleMode.INTERVAL,
            interval_seconds=60,
            callback=run_health_check,
        )
        scheduler.cancel(job.id)
    """

    def __init__(self) -> None:
        self._jobs: dict[str, tuple[ScheduledJob, Callable[[], Any]]] = {}
        self._paused: bool = False

    def register(
        self,
        name: str,
        service: str,
        mode: ScheduleMode,
        callback: Callable[[], Any],
        interval_seconds: Optional[int] = None,
        cron_expression: Optional[str] = None,
        run_at: Optional[datetime] = None,
    ) -> ScheduledJob:
        """Register a new scheduled job and return its metadata."""
        job = ScheduledJob(
            name=name,
            service=service,
            mode=mode,
            interval_seconds=interval_seconds,
            cron_expression=cron_expression,
            run_at=run_at,
        )
        self._jobs[job.id] = (job, callback)
        return job

    def cancel(self, job_id: str) -> bool:
        """Cancel a scheduled job.  Returns ``True`` if found and removed."""
        return self._jobs.pop(job_id, None) is not None

    def pause(self) -> None:
        """Pause all job execution (e.g. during maintenance)."""
        self._paused = True

    def resume(self) -> None:
        """Resume job execution."""
        self._paused = False

    @property
    def is_paused(self) -> bool:
        return self._paused

    @property
    def jobs(self) -> list[ScheduledJob]:
        """Return metadata for all registered jobs."""
        return [job for job, _cb in self._jobs.values()]

    def get_job(self, job_id: str) -> Optional[ScheduledJob]:
        """Retrieve metadata for a specific job."""
        entry = self._jobs.get(job_id)
        return entry[0] if entry else None
