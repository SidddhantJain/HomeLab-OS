"""
HomeLab OS — Download Manager Service

Manages download queues, tracks progress, maps storage destinations,
and handles cleanup rules.
"""

from __future__ import annotations

import os
from typing import Any, Dict, List, Optional
from sqlalchemy.orm import Session

from app.core.base_service import BaseService
from app.core.homelab_core import HomelabCore
from app.core.event_bus import Event
from app.models.download import DownloadTask
from app.services.downloads.events import DownloadEvents


class DownloadService(BaseService):
    """Enforces active download queue allocations and status tracking."""

    def __init__(self) -> None:
        self._download_dir = "/opt/homelab/downloads"

    @property
    def name(self) -> str:
        return "downloads"

    def initialize(self) -> None:
        """Startup configuration checks."""
        try:
            os.makedirs(self._download_dir, exist_ok=True)
        except OSError:
            pass

    def shutdown(self) -> None:
        """Shutdown hook."""
        pass

    def health(self) -> Dict[str, Any]:
        """Telemetry health checks."""
        return {
            "status": "healthy",
            "message": "Download manager is operational."
        }

    # ------------------------------------------------------------------
    # Download Operations
    # ------------------------------------------------------------------

    def enqueue_download(self, db: Session, url: str, destination: Optional[str] = None) -> DownloadTask:
        """Enqueue a new network download task."""
        file_name = url.split("/")[-1] or "downloaded_file"
        target_path = os.path.join(destination or self._download_dir, file_name)

        task = DownloadTask(
            url=url,
            file_path=target_path,
            status="PENDING",
            progress=0.0,
            total_size=100 * 1024 * 1024,  # 100MB (mock)
            downloaded_size=0
        )
        db.add(task)
        db.commit()
        db.refresh(task)

        # Dispatch start event
        core = HomelabCore.instance()
        core.event_bus.publish(
            Event(
                name=DownloadEvents.STARTED,
                source=self.name,
                payload={"task_id": task.id, "url": url}
            )
        )

        # Simulate completion
        task.status = "COMPLETED"
        task.progress = 100.0
        task.downloaded_size = task.total_size
        db.commit()

        core.event_bus.publish(
            Event(
                name=DownloadEvents.COMPLETED,
                source=self.name,
                payload={"task_id": task.id, "file_path": target_path}
            )
        )
        return task

    def get_downloads(self, db: Session) -> List[DownloadTask]:
        """List current download tasks."""
        return db.query(DownloadTask).all()

    def get_download(self, db: Session, task_id: str) -> Optional[DownloadTask]:
        """Get details for a single download task."""
        return db.query(DownloadTask).filter(DownloadTask.id == task_id).first()
