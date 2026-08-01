"""
HomeLab OS — Alert Service
"""

from __future__ import annotations

from typing import Any, Dict, List
from sqlalchemy.orm import Session
from app.core.base_service import BaseService
from app.models.alert import Alert, AlertRule
from app.services.alerts.engine import AlertEngine


class AlertService(BaseService):
    """Manages system alert rules and active alert dispatches."""

    def __init__(self) -> None:
        self.engine = AlertEngine()

    @property
    def name(self) -> str:
        return "alerts"

    def initialize(self) -> None:
        pass

    def shutdown(self) -> None:
        pass

    def health(self) -> Dict[str, Any]:
        return {
            "status": "healthy",
            "message": "Alert Service is active and evaluating rules."
        }

    def get_alerts(self, db: Session) -> List[Alert]:
        return db.query(Alert).order_by(Alert.timestamp.desc()).all()

    def create_rule(self, db: Session, name: str, metric_name: str, threshold: float, comparison: str = ">", severity: str = "WARNING") -> AlertRule:
        rule = AlertRule(
            name=name,
            metric_name=metric_name,
            threshold=threshold,
            comparison=comparison,
            severity=severity,
            enabled=True
        )
        db.add(rule)
        db.commit()
        db.refresh(rule)
        return rule
