import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    status = Column(String(50), default="CREATED", nullable=False)  # CREATED, ACTIVE, ARCHIVED, DELETED
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    metadata_rel = relationship("ProjectMetadata", back_populates="project", cascade="all, delete-orphan", uselist=False)


class ProjectMetadata(Base):
    __tablename__ = "project_metadata"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, unique=True)
    language = Column(String(50), nullable=True)
    framework = Column(String(50), nullable=True)
    repository = Column(String(255), nullable=True)
    runtime = Column(String(50), nullable=True)
    storage = Column(String(255), nullable=True)

    project = relationship("Project", back_populates="metadata_rel")
