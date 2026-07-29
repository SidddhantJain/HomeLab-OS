import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Float, Integer, ForeignKey
from app.core.database import Base


class Snapshot(Base):
    __tablename__ = "snapshots"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    workspace_id = Column(String(36), ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False)
    created_time = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    size = Column(Float, default=0.0, nullable=False)  # in GB
    status = Column(String(50), default="CREATED", nullable=False)
    retention_cycle = Column(Integer, default=1, nullable=False)
