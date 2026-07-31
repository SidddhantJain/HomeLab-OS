import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, JSON
from app.core.database import Base


class UpdateHistory(Base):
    __tablename__ = "update_history"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    from_version = Column(String(50), nullable=False)
    to_version = Column(String(50), nullable=False)
    status = Column(String(50), default="COMPLETED", nullable=False)  # COMPLETED, ROLLED_BACK, FAILED
    details = Column(JSON, nullable=True)
    performed_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
