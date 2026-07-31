import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, JSON, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class WorkflowJob(Base):
    __tablename__ = "workflow_jobs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    trigger_type = Column(String(50), nullable=False)  # time, event, threshold, manual
    trigger_config = Column(JSON, nullable=True)
    conditions = Column(JSON, nullable=True)
    actions = Column(JSON, nullable=False)  # list of action names & payloads
    enabled = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    history = relationship("WorkflowHistory", back_populates="workflow", cascade="all, delete-orphan")


class WorkflowHistory(Base):
    __tablename__ = "workflow_history"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    workflow_id = Column(String(36), ForeignKey("workflow_jobs.id", ondelete="CASCADE"), nullable=False)
    status = Column(String(20), default="SUCCESS", nullable=False)  # SUCCESS, FAILED
    execution_time = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    details = Column(JSON, nullable=True)

    workflow = relationship("WorkflowJob", back_populates="history")
