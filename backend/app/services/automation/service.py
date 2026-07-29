"""
HomeLab OS — Automation Service

Main coordination class.
"""

from __future__ import annotations

from typing import Any, Dict
from app.core.base_service import BaseService
from app.core.homelab_core import HomelabCore
from app.core.scheduler import ScheduleMode
from app.services.automation.cleanup import CleanupAutomation


class AutomationService(BaseService):
    """Orchestrates routine prunings and schedules cleanup tasks."""

    def __init__(self) -> None:
        self._cleanup = CleanupAutomation()

    @property
    def name(self) -> str:
        return "automation"

    def initialize(self) -> None:
        """Register automated pruner tasks with the global Scheduler on startup."""
        core = HomelabCore.instance()
        scheduler = core.scheduler

        # 1. Clean temporary files (every 24 hours)
        scheduler.register(
            name="Temporary File Cleanup",
            service=self.name,
            mode=ScheduleMode.INTERVAL,
            interval_seconds=86400,
            callback=lambda: self._cleanup.clean_temp_files("/tmp/homelab-temp")
        )

        # 2. Rotate logs (every 24 hours)
        scheduler.register(
            name="Log Rotation Job",
            service=self.name,
            mode=ScheduleMode.INTERVAL,
            interval_seconds=86400,
            callback=lambda: self._cleanup.rotate_logs("/var/log/homelab")
        )

    def shutdown(self) -> None:
        """Shutdown hook."""
        pass

    def health(self) -> Dict[str, Any]:
        """Telemetry health checks."""
        return {
            "status": "healthy",
            "message": "Automation service is registered and schedules are loaded."
        }
