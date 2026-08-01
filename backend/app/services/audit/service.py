"""
HomeLab OS — Central Audit Service
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from sqlalchemy.orm import Session
from app.core.base_service import BaseService
from app.models.audit import AuditLog


class AuditService(BaseService):
    """Central audit service logging USER, SYSTEM, SECURITY, AUTOMATION, and ADMIN events."""

    @property
    def name(self) -> str:
        return "audit"

    def initialize(self) -> None:
        pass

    def shutdown(self) -> None:
        pass

    def health(self) -> Dict[str, Any]:
        return {
            "status": "healthy",
            "message": "Audit Service is active."
        }

    def log_event(self, db: Session, action: str, category: str = "SYSTEM", details: Dict[str, Any] = None, user_id: str = "system") -> AuditLog:
        entry = AuditLog(
            action=action,
            user=user_id or "system",
            metadata_json=details or {}
        )
        db.add(entry)
        db.commit()
        db.refresh(entry)
        return entry


    def search_audit_logs(self, db: Session, category: Optional[str] = None, query: Optional[str] = None, limit: int = 50) -> List[AuditLog]:
        q = db.query(AuditLog)
        if query:
            q = q.filter(AuditLog.action.ilike(f"%{query}%"))
        return q.order_by(AuditLog.timestamp.desc()).limit(limit).all()
