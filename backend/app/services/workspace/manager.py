"""
HomeLab OS — Workspace Manager

Manages directory sizes, workspace initialization, cloning, and state transitions.
"""

from __future__ import annotations

import os
from sqlalchemy.orm import Session
from app.models.workspace import Workspace


class WorkspaceManager:
    """Orchestrates filesystem workspaces and tracking metadata."""

    def __init__(self) -> None:
        pass

    def get_dir_size(self, path: str) -> float:
        """Calculate directory usage size in GB."""
        if not os.path.exists(path):
            return 0.0

        total_size = 0
        try:
            for dirpath, dirnames, filenames in os.walk(path):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    if not os.path.islink(fp):
                        total_size += os.path.getsize(fp)
        except OSError:
            pass

        return round(total_size / (1024 ** 3), 4)

    def create(self, db: Session, name: str, owner: str, root_dir: str, description: Optional[str] = None) -> Workspace:
        """Register and instantiate a workspace target."""
        storage_location = os.path.join(root_dir, name)
        try:
            os.makedirs(storage_location, exist_ok=True)
        except OSError:
            pass

        ws = Workspace(
            name=name,
            description=description,
            owner=owner,
            storage_location=storage_location,
            size=0.0,
            status="ACTIVE"
        )
        db.add(ws)
        db.commit()
        db.refresh(ws)
        return ws

    def clone(self, db: Session, source_ws: Workspace, clone_name: str, root_dir: str) -> Workspace:
        """Create a clone registry copy of another workspace directory."""
        clone_location = os.path.join(root_dir, clone_name)
        try:
            os.makedirs(clone_location, exist_ok=True)
        except OSError:
            pass

        ws = Workspace(
            name=clone_name,
            description=f"Clone of {source_ws.name}",
            owner=source_ws.owner,
            storage_location=clone_location,
            size=source_ws.size,
            status="ACTIVE"
        )
        db.add(ws)
        db.commit()
        db.refresh(ws)
        return ws
