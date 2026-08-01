"""
HomeLab OS — Docker Management Service Integration
"""

from __future__ import annotations

from typing import Any, Dict, List
from sqlalchemy.orm import Session
from app.core.base_service import BaseService
from app.services.docker.manager import DockerManager


class DockerService(BaseService):
    """Integrates Docker container monitoring and lifecycle management."""

    def __init__(self) -> None:
        self.manager = DockerManager()

    @property
    def name(self) -> str:
        return "docker"

    def initialize(self) -> None:
        pass

    def shutdown(self) -> None:
        pass

    def health(self) -> Dict[str, Any]:
        return {
            "status": "healthy",
            "message": "Docker Management Service is active."
        }

    def list_containers(self, db: Session) -> List[Dict[str, Any]]:
        return self.manager.list_containers(db)

    def restart_container(self, db: Session, container_id: str) -> Dict[str, Any]:
        return self.manager.restart_container(db, container_id)

    def get_logs(self, container_id: str) -> str:
        return self.manager.get_container_logs(container_id)
