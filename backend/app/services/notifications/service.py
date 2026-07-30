"""
HomeLab OS — Notification Service

Main coordination class.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from sqlalchemy.orm import Session

from app.core.base_service import BaseService
from app.core.homelab_core import HomelabCore
from app.core.event_bus import Event
from app.core.database import SessionLocal
from app.models.notification import Notification


class NotificationService(BaseService):
    """Subscribes to system events to generate user-facing dashboard alerts."""

    def __init__(self) -> None:
        pass

    @property
    def name(self) -> str:
        return "notifications"

    def initialize(self) -> None:
        """Subscribe to platform events on startup."""
        core = HomelabCore.instance()
        
        # Subscribe to all events of interest
        core.event_bus.subscribe("storage.*", self._handle_event)
        core.event_bus.subscribe("vault.*", self._handle_event)
        core.event_bus.subscribe("workspace.*", self._handle_event)
        core.event_bus.subscribe("backup.*", self._handle_event)
        core.event_bus.subscribe("snapshot.*", self._handle_event)
        core.event_bus.subscribe("download.*", self._handle_event)

    def shutdown(self) -> None:
        """Shutdown hook."""
        pass

    def health(self) -> Dict[str, Any]:
        """Telemetry health checks."""
        return {
            "status": "healthy",
            "message": "Notification service is active and listening to events."
        }

    # ------------------------------------------------------------------
    # Notification Operations
    # ------------------------------------------------------------------

    def _handle_event(self, event: Event) -> None:
        """Parse event envelope and store database alerts."""
        db = SessionLocal()
        try:
            message = f"Event '{event.name}' triggered by {event.source}."
            if event.payload and "message" in event.payload:
                message = event.payload["message"]

            # Map event domains to severities
            severity = "INFO"
            if "warning" in event.name or "failed" in event.name:
                severity = "WARNING"
            elif "critical" in event.name:
                severity = "CRITICAL"

            note = Notification(
                message=message,
                severity=severity,
                status="UNREAD"
            )
            db.add(note)
            db.commit()
        except Exception as exc:  # noqa: BLE001
            print(f"[NotificationService] Failed to record alert: {exc}")
        finally:
            db.close()

    def get_notifications(self, db: Session) -> List[Notification]:
        """Query active notification list."""
        return db.query(Notification).order_by(Notification.created_at.desc()).all()

    def mark_as_read(self, db: Session, notification_id: str) -> bool:
        """Mark a notification as read."""
        from datetime import datetime, timezone
        note = db.query(Notification).filter(Notification.id == notification_id).first()
        if not note:
            return False

        note.status = "READ"
        note.read_at = datetime.now(timezone.utc)
        db.commit()
        return True
