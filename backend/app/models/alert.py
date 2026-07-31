import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class AlertRule(Base):
    __tablename__ = "alert_rules"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    metric_name = Column(String(100), nullable=False)
    threshold = Column(Float, nullable=False)
    comparison = Column(String(10), default=">", nullable=False)  # >, <, >=, <=, ==
    severity = Column(String(20), default="WARNING", nullable=False)  # INFO, WARNING, CRITICAL, EMERGENCY
    enabled = Column(Boolean, default=True, nullable=False)

    alerts = relationship("Alert", back_populates="rule", cascade="all, delete-orphan")


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    rule_id = Column(String(36), ForeignKey("alert_rules.id", ondelete="SET NULL"), nullable=True)
    key = Column(String(100), nullable=False)
    message = Column(String(500), nullable=False)
    severity = Column(String(20), default="WARNING", nullable=False)
    status = Column(String(20), default="ACTIVE", nullable=False)  # ACTIVE, ACKNOWLEDGED, RESOLVED
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    resolved_at = Column(DateTime, nullable=True)

    rule = relationship("AlertRule", back_populates="alerts")
