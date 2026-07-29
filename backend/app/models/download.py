import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Float, Integer
from app.core.database import Base


class DownloadTask(Base):
    __tablename__ = "download_tasks"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    url = Column(String(500), nullable=False)
    file_path = Column(String(255), nullable=False)
    status = Column(String(50), default="PENDING", nullable=False)  # PENDING, RUNNING, COMPLETED, FAILED
    progress = Column(Float, default=0.0, nullable=False)  # 0.0 to 100.0
    total_size = Column(Integer, default=0, nullable=False)  # in Bytes
    downloaded_size = Column(Integer, default=0, nullable=False)  # in Bytes
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
