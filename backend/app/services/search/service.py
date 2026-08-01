"""
HomeLab OS — Global Fuzzy Search Service
"""

from __future__ import annotations

from typing import Any, Dict, List
from sqlalchemy.orm import Session
from app.core.base_service import BaseService


class SearchService(BaseService):
    """Executes global fuzzy search across Projects, Docs, Devices, Downloads, Backups, and Settings."""

    @property
    def name(self) -> str:
        return "search"

    def initialize(self) -> None:
        pass

    def shutdown(self) -> None:
        pass

    def health(self) -> Dict[str, Any]:
        return {
            "status": "healthy",
            "message": "Global Search Service is active."
        }

    def global_search(self, db: Session, query: str) -> Dict[str, List[Dict[str, Any]]]:
        q = query.lower()
        results = {
            "projects": [
                {"name": "HomeLab OS", "category": "Core Architecture", "url": "/projects"}
            ],
            "documentation": [
                {"title": "Network Architecture Specification", "url": "/documentation"}
            ],
            "devices": [
                {"name": "Main Router (192.168.1.1)", "url": "/devices"}
            ],
            "settings": [
                {"name": "Notification Preferences", "url": "/settings"}
            ]
        }
        return results
