import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Boolean
from app.core.database import Base


class PowerSchedule(Base):
    __tablename__ = "power_schedule"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    action = Column(String(50), nullable=False)  # sleep, wake, shutdown
    cron_expression = Column(String(50), nullable=False)  # e.g., "0 0 * * *"
    enabled = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
