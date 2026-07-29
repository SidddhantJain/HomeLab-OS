import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Float, Boolean
from app.core.database import Base


class VaultMetadata(Base):
    __tablename__ = "vault_metadata"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    status = Column(String(50), default="LOCKED", nullable=False)  # LOCKED, UNLOCKING, UNLOCKED, LOCKING
    capacity = Column(Float, nullable=False)  # in GB
    mount_location = Column(String(255), nullable=False)
    encryption_type = Column(String(50), default="LUKS2", nullable=False)
    last_unlock_time = Column(DateTime, nullable=True)
    unlock_failure_count = Column(DateTime, nullable=True)  # track issues or keep simple
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
