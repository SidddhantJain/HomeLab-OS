import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Float
from app.core.database import Base


class SystemMetric(Base):
    __tablename__ = "system_metrics"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    cpu_usage = Column(Float, nullable=False)
    ram_usage = Column(Float, nullable=False)
    temperature = Column(Float, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
