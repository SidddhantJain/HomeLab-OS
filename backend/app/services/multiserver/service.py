"""
HomeLab OS — Multi-Server Management Service
"""

from __future__ import annotations

from typing import Any, Dict, List
from sqlalchemy.orm import Session
from app.core.base_service import BaseService
from app.models.multiserver import ManagedServer


class MultiServerService(BaseService):
    """Manages multi-server definitions, profiles, and connectivity."""

    @property
    def name(self) -> str:
        return "multiserver"

    def initialize(self) -> None:
        pass

    def shutdown(self) -> None:
        pass

    def health(self) -> Dict[str, Any]:
        return {
            "status": "healthy",
            "message": "Multi-Server Management Service is active."
        }

    def list_servers(self, db: Session) -> List[ManagedServer]:
        servers = db.query(ManagedServer).all()
        if not servers:
            default_srv = ManagedServer(
                name="Primary HomeLab Server",
                host="127.0.0.1",
                port=8000,
                group_name="Home",
                location="Local Machine",
                is_favorite=True,
                is_trusted=True
            )
            db.add(default_srv)
            db.commit()
            servers = db.query(ManagedServer).all()
        return servers

    def add_server(self, db: Session, name: str, host: str, port: int = 8000, group_name: str = "Home") -> ManagedServer:
        srv = ManagedServer(name=name, host=host, port=port, group_name=group_name)
        db.add(srv)
        db.commit()
        db.refresh(srv)
        return srv
