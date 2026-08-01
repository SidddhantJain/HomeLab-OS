import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Float, BigInteger
from app.core.database import Base


class FileTransfer(Base):
    __tablename__ = "file_transfers"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    file_name = Column(String(255), nullable=False)
    source_path = Column(String(500), nullable=False)
    destination_path = Column(String(500), nullable=False)
    total_bytes = Column(BigInteger, default=0, nullable=False)
    transferred_bytes = Column(BigInteger, default=0, nullable=False)
    status = Column(String(20), default="IN_PROGRESS", nullable=False)
    checksum = Column(String(64), nullable=True)
    started_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
