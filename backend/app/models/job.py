import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Float, JSON
from app.core.database import Base


class BackgroundJob(Base):
    __tablename__ = "background_jobs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    job_type = Column(String(50), nullable=False)  # backup, download, update, snapshot, workflow
    status = Column(String(20), default="QUEUED", nullable=False)  # QUEUED, RUNNING, COMPLETED, FAILED
    progress_pct = Column(Float, default=0.0, nullable=False)
    error_message = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    completed_at = Column(DateTime, nullable=True)
