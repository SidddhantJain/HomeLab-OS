import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Boolean, JSON
from app.core.database import Base


class PluginMetadata(Base):
    __tablename__ = "plugins_metadata"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    plugin_id = Column(String(100), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    version = Column(String(50), default="1.0.0", nullable=False)
    author = Column(String(100), nullable=True)
    description = Column(String(500), nullable=True)
    enabled = Column(Boolean, default=True, nullable=False)
    permissions = Column(JSON, nullable=True)
    installed_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
