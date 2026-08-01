"""
HomeLab OS — Unified Activity Timeline Service
"""

from __future__ import annotations

from typing import Any, Dict, List
from sqlalchemy.orm import Session
from app.core.base_service import BaseService
from app.models.activity import ActivityTimeline


class ActivityService(BaseService):
    """Records and retrieves system-wide activity timeline events."""

    @property
    def name(self) -> str:
        return "activity"

    def initialize(self) -> None:
        pass

    def shutdown(self) -> None:
        pass

    def health(self) -> Dict[str, Any]:
        return {
            "status": "healthy",
            "message": "Activity Timeline Service is active."
        }

    def record_event(self, db: Session, event_type: str, title: str, description: str = "", category: str = "system", severity: str = "info", details: Dict[str, Any] = None) -> ActivityTimeline:
        act = ActivityTimeline(
            event_type=event_type,
            title=title,
            description=description,
            category=category,
            severity=severity,
            details=details
        )
        db.add(act)
        db.commit()
        db.refresh(act)
        return act

    def get_timeline(self, db: Session, limit: int = 50) -> List[ActivityTimeline]:
        acts = db.query(ActivityTimeline).order_by(ActivityTimeline.timestamp.desc()).limit(limit).all()
        if not acts:
            self.record_event(db, "system.boot", "HomeLab OS Platform Booted", "All Phase 1-6 core services initialized.", "system", "info")
            acts = db.query(ActivityTimeline).order_by(ActivityTimeline.timestamp.desc()).limit(limit).all()
        return acts
