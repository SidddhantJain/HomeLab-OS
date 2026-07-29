"""
HomeLab OS — Project Intelligence Service

Main coordination class.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from sqlalchemy.orm import Session

from app.core.base_service import BaseService
from app.core.homelab_core import HomelabCore
from app.core.event_bus import Event
from app.services.projects.manager import ProjectManager
from app.services.projects.snapshot.manager import SnapshotManager
from app.services.projects.models import Project, Snapshot
from app.services.projects.events import ProjectEvents


class ProjectService(BaseService):
    """Integrates project registries and workspace snapshots with core events."""

    def __init__(self) -> None:
        self._manager = ProjectManager()
        self._snapshot = SnapshotManager()

    @property
    def name(self) -> str:
        return "projects"

    def initialize(self) -> None:
        """Startup hook."""
        pass

    def shutdown(self) -> None:
        """Shutdown hook."""
        pass

    def health(self) -> Dict[str, Any]:
        """Telemetry health checks."""
        return {
            "status": "healthy",
            "message": "Projects service is active."
        }

    # ------------------------------------------------------------------
    # Project operations
    # ------------------------------------------------------------------

    def register_project(self, db: Session, name: str, path: str, description: Optional[str] = None) -> Project:
        """Register a new project and publish event."""
        p = self._manager.register_project(db, name, path, description)

        core = HomelabCore.instance()
        core.event_bus.publish(
            Event(
                name=ProjectEvents.CREATED,
                source=self.name,
                payload={"project_id": p.id, "name": p.name}
            )
        )
        return p

    def get_projects(self, db: Session) -> List[Project]:
        """Fetch all projects."""
        return self._manager.get_projects(db)

    def get_project(self, db: Session, project_id: str) -> Optional[Project]:
        """Query project details."""
        return self._manager.get_project(db, project_id)

    # ------------------------------------------------------------------
    # Snapshot operations
    # ------------------------------------------------------------------

    def create_snapshot(self, db: Session, workspace_id: str) -> Snapshot:
        """Create a workspace partition snapshot."""
        return self._snapshot.create_snapshot(db, workspace_id)

    def restore_snapshot(self, db: Session, snapshot_id: str) -> bool:
        """Restore a snapshot target state."""
        return self._snapshot.restore_snapshot(db, snapshot_id)

    def get_snapshots(self, db: Session, workspace_id: str) -> List[Snapshot]:
        """List snapshot history for a workspace."""
        return db.query(Snapshot).filter(Snapshot.workspace_id == workspace_id).all()
