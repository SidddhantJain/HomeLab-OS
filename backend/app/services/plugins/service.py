"""
HomeLab OS — Plugin Marketplace Foundation Service
"""

from __future__ import annotations

from typing import Any, Dict, List
from sqlalchemy.orm import Session
from app.core.base_service import BaseService
from app.models.plugin import PluginMetadata


class PluginService(BaseService):
    """Manages plugin lifecycles, version compatibility, and permission scopes."""

    @property
    def name(self) -> str:
        return "plugins"

    def initialize(self) -> None:
        pass

    def shutdown(self) -> None:
        pass

    def health(self) -> Dict[str, Any]:
        return {
            "status": "healthy",
            "message": "Plugin Manager Service is active."
        }

    def list_plugins(self, db: Session) -> List[PluginMetadata]:
        return db.query(PluginMetadata).all()

    def register_plugin(self, db: Session, plugin_id: str, name: str, version: str = "1.0.0", author: str = "HomeLab Ecosystem", description: str = "", permissions: List[str] = None) -> PluginMetadata:
        plug = db.query(PluginMetadata).filter(PluginMetadata.plugin_id == plugin_id).first()
        if not plug:
            plug = PluginMetadata(
                plugin_id=plugin_id,
                name=name,
                version=version,
                author=author,
                description=description,
                enabled=True,
                permissions=permissions or []
            )
            db.add(plug)
            db.commit()
            db.refresh(plug)
        return plug
