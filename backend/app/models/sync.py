import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, JSON
from app.core.database import Base


class SyncState(Base):
    __tablename__ = "sync_state"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    device_id = Column(String(100), nullable=False)
    sync_key = Column(String(100), nullable=False)
    payload = Column(JSON, nullable=True)
    synced_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
