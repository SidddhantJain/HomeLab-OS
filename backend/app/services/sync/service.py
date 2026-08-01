"""
HomeLab OS — Synchronization Service
"""

from __future__ import annotations

from typing import Any, Dict
from sqlalchemy.orm import Session
from app.core.base_service import BaseService
from app.models.sync import SyncState


class SyncService(BaseService):
    """Synchronizes user preferences, tokens, and server lists across devices."""

    @property
    def name(self) -> str:
        return "sync"

    def initialize(self) -> None:
        pass

    def shutdown(self) -> None:
        pass

    def health(self) -> Dict[str, Any]:
        return {
            "status": "healthy",
            "message": "Synchronization Service is active."
        }

    def sync_payload(self, db: Session, device_id: str, sync_key: str, payload: Dict[str, Any]) -> SyncState:
        st = db.query(SyncState).filter(SyncState.device_id == device_id, SyncState.sync_key == sync_key).first()
        if not st:
            st = SyncState(device_id=device_id, sync_key=sync_key, payload=payload)
            db.add(st)
        else:
            st.payload = payload
        db.commit()
        db.refresh(st)
        return st
