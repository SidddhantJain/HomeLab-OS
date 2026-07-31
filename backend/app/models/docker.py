import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, JSON
from app.core.database import Base


class DockerService(Base):
    __tablename__ = "docker_services"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    container_id = Column(String(64), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    image = Column(String(255), nullable=False)
    status = Column(String(50), default="running", nullable=False)
    ports = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
