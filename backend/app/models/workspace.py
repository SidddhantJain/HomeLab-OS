import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Float
from app.core.database import Base


class Workspace(Base):
    __tablename__ = "workspaces"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    owner = Column(String(100), nullable=False)
    storage_location = Column(String(255), nullable=False)
    size = Column(Float, default=0.0, nullable=False)  # in GB
    status = Column(String(50), default="ACTIVE", nullable=False)  # ACTIVE, ARCHIVED, DELETED, RESTORING
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
