"""
HomeLab OS — Workspace Service

Main coordination class.
"""

from __future__ import annotations

import os
from typing import Any, Dict, List, Optional
from sqlalchemy.orm import Session

from app.core.base_service import BaseService
from app.core.homelab_core import HomelabCore
from app.core.event_bus import Event
from app.services.workspace.manager import WorkspaceManager
from app.services.workspace.models import Workspace
from app.services.workspace.events import WorkspaceEvents


class WorkspaceService(BaseService):
    """Integrates developer workspaces, size scans, and core events."""

    def __init__(self) -> None:
        self._manager = WorkspaceManager()
        # Default target folder
        self._root_dir = "/opt/homelab/workspaces"

    @property
    def name(self) -> str:
        return "workspace"

    def initialize(self) -> None:
        """Startup configuration checks."""
        try:
            os.makedirs(self._root_dir, exist_ok=True)
        except OSError:
            pass

    def shutdown(self) -> None:
        """Shutdown actions."""
        pass

    def health(self) -> Dict[str, Any]:
        """Telemetry health checks."""
        return {
            "status": "healthy",
            "message": "Workspace service is active and listening."
        }

    # ------------------------------------------------------------------
    # Workspace operations
    # ------------------------------------------------------------------

    def create_workspace(self, db: Session, name: str, owner: str, description: Optional[str] = None) -> Workspace:
        """Create a workspace and dispatch event."""
        ws = self._manager.create(db, name, owner, self._root_dir, description)

        core = HomelabCore.instance()
        core.event_bus.publish(
            Event(
                name=WorkspaceEvents.CREATED,
                source=self.name,
                payload={"workspace_id": ws.id, "name": ws.name}
            )
        )
        return ws

    def delete_workspace(self, db: Session, workspace_id: str) -> bool:
        """Safely marks workspace state as DELETED."""
        ws = db.query(Workspace).filter(Workspace.id == workspace_id).first()
        if not ws:
            return False

        ws.status = "DELETED"
        db.commit()

        core = HomelabCore.instance()
        core.event_bus.publish(
            Event(
                name=WorkspaceEvents.DELETED,
                source=self.name,
                payload={"workspace_id": workspace_id, "name": ws.name}
            )
        )
        return True

    def archive_workspace(self, db: Session, workspace_id: str) -> bool:
        """Safely marks workspace state as ARCHIVED."""
        ws = db.query(Workspace).filter(Workspace.id == workspace_id).first()
        if not ws:
            return False

        ws.status = "ARCHIVED"
        db.commit()

        core = HomelabCore.instance()
        core.event_bus.publish(
            Event(
                name=WorkspaceEvents.ARCHIVED,
                source=self.name,
                payload={"workspace_id": workspace_id, "name": ws.name}
            )
        )
        return True

    def restore_workspace(self, db: Session, workspace_id: str) -> bool:
        """Safely marks workspace state as ACTIVE."""
        ws = db.query(Workspace).filter(Workspace.id == workspace_id).first()
        if not ws:
            return False

        ws.status = "ACTIVE"
        db.commit()

        core = HomelabCore.instance()
        core.event_bus.publish(
            Event(
                name=WorkspaceEvents.RESTORED,
                source=self.name,
                payload={"workspace_id": workspace_id, "name": ws.name}
            )
        )
        return True

    def get_workspaces(self, db: Session) -> List[Workspace]:
        """Fetch all non-deleted workspaces."""
        return db.query(Workspace).filter(Workspace.status != "DELETED").all()

    def get_workspace(self, db: Session, workspace_id: str) -> Optional[Workspace]:
        """Query single workspace detail."""
        return db.query(Workspace).filter(Workspace.id == workspace_id).first()
