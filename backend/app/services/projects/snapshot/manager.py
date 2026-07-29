"""
HomeLab OS — Project Snapshot Manager

Coordinates project loop backups, schedules snapshot runs,
and enforces automated retention policies.
"""

from __future__ import annotations

from typing import List, Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.models.snapshot import Snapshot
from app.core.homelab_core import HomelabCore
from app.core.event_bus import Event
from app.services.projects.events import SnapshotEvents


class SnapshotManager:
    """Manages snapshot history and triggers retention cleanup routines."""

    def __init__(self, keep_snapshots_limit: int = 10) -> None:
        self.keep_snapshots_limit = keep_snapshots_limit

    def create_snapshot(self, db: Session, workspace_id: str) -> Snapshot:
        """Create a new snapshot record and apply retention policies."""
        snap = Snapshot(
            workspace_id=workspace_id,
            size=0.1,  # in GB (mock)
            status="CREATED",
            retention_cycle=1
        )
        db.add(snap)
        db.commit()
        db.refresh(snap)

        # Dispatch event
        core = HomelabCore.instance()
        core.event_bus.publish(
            Event(
                name=SnapshotEvents.CREATED,
                source="snapshot_manager",
                payload={"snapshot_id": snap.id, "workspace_id": workspace_id}
            )
        )

        # Apply retention cleanup
        self.enforce_retention_policy(db, workspace_id)
        return snap

    def restore_snapshot(self, db: Session, snapshot_id: str) -> bool:
        """Restores platform state to match target snapshot version."""
        snap = db.query(Snapshot).filter(Snapshot.id == snapshot_id).first()
        if not snap:
            return False

        snap.status = "RESTORED"
        db.commit()

        # Dispatch event
        core = HomelabCore.instance()
        core.event_bus.publish(
            Event(
                name=SnapshotEvents.RESTORED,
                source="snapshot_manager",
                payload={"snapshot_id": snapshot_id, "workspace_id": snap.workspace_id}
            )
        )
        return True

    def delete_snapshot(self, db: Session, snapshot_id: str) -> bool:
        """Permanently remove snapshot registration."""
        snap = db.query(Snapshot).filter(Snapshot.id == snapshot_id).first()
        if not snap:
            return False

        db.delete(snap)
        db.commit()

        # Dispatch event
        core = HomelabCore.instance()
        core.event_bus.publish(
            Event(
                name=SnapshotEvents.DELETED,
                source="snapshot_manager",
                payload={"snapshot_id": snapshot_id}
            )
        )
        return True

    def enforce_retention_policy(self, db: Session, workspace_id: str) -> None:
        """Query snapshot counts and delete oldest records beyond limit settings."""
        snapshots = db.query(Snapshot).filter(
            Snapshot.workspace_id == workspace_id
        ).order_by(Snapshot.created_time.asc()).all()

        if len(snapshots) > self.keep_snapshots_limit:
            overflow_count = len(snapshots) - self.keep_snapshots_limit
            for i in range(overflow_count):
                self.delete_snapshot(db, snapshots[i].id)
