import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime
from app.core.database import Base


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    message = Column(String(500), nullable=False)
    severity = Column(String(50), default="INFO", nullable=False)  # INFO, WARNING, CRITICAL
    status = Column(String(50), default="UNREAD", nullable=False)  # UNREAD, READ
    read_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
