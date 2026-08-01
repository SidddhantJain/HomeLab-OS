import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, JSON
from app.core.database import Base


class UserSettings(Base):
    __tablename__ = "user_settings"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), nullable=False, unique=True)
    theme = Column(String(20), default="dark", nullable=False)  # dark, light, auto
    language = Column(String(10), default="en", nullable=False)
    timezone = Column(String(50), default="UTC", nullable=False)
    dashboard_layout = Column(JSON, nullable=True)
    preferences = Column(JSON, nullable=True)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
