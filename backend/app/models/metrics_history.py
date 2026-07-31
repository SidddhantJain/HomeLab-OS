import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Float, JSON
from app.core.database import Base


class MetricsHistory(Base):
    __tablename__ = "metrics_history"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    metric_name = Column(String(100), nullable=False, index=True)
    metric_value = Column(Float, nullable=False)
    tags = Column(JSON, nullable=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False, index=True)
