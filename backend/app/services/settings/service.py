"""
HomeLab OS — Settings Center & Configuration Manager Service
"""

from __future__ import annotations

from typing import Any, Dict
from sqlalchemy.orm import Session
from app.core.base_service import BaseService
from app.models.settings import UserSettings


class SettingsService(BaseService):
    """Manages centralized user settings and system configurations."""

    @property
    def name(self) -> str:
        return "settings"

    def initialize(self) -> None:
        pass

    def shutdown(self) -> None:
        pass

    def health(self) -> Dict[str, Any]:
        return {
            "status": "healthy",
            "message": "Settings Center Service is active."
        }

    def get_settings(self, db: Session, user_id: str = "default_user") -> UserSettings:
        st = db.query(UserSettings).filter(UserSettings.user_id == user_id).first()
        if not st:
            st = UserSettings(
                user_id=user_id,
                theme="dark",
                language="en",
                timezone="UTC",
                dashboard_layout={"columns": 3, "widgets": ["system", "network", "storage"]},
                preferences={"notifications_enabled": True}
            )
            db.add(st)
            db.commit()
            db.refresh(st)
        return st

    def update_settings(self, db: Session, user_id: str = "default_user", theme: str = None, language: str = None, timezone: str = None) -> UserSettings:
        st = self.get_settings(db, user_id)
        if theme:
            st.theme = theme
        if language:
            st.language = language
        if timezone:
            st.timezone = timezone
        db.commit()
        db.refresh(st)
        return st
