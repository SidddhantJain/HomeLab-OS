import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, JSON
from app.core.database import Base


class ActivityTimeline(Base):
    __tablename__ = "activity_timeline"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    event_type = Column(String(100), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(String(500), nullable=True)
    category = Column(String(50), default="system", nullable=False)
    severity = Column(String(20), default="info", nullable=False)
    details = Column(JSON, nullable=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
