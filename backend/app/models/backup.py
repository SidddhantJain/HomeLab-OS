import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime
from app.core.database import Base


class BackupJob(Base):
    __tablename__ = "backup_jobs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    source = Column(String(255), nullable=False)
    destination = Column(String(255), nullable=False)
    status = Column(String(50), default="PENDING", nullable=False)  # PENDING, RUNNING, COMPLETED, FAILED
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    completed_at = Column(DateTime, nullable=True)
