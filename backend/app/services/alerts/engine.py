"""
HomeLab OS — Intelligent Alert Rule Evaluator & Engine
"""

from __future__ import annotations

from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from app.models.alert import Alert, AlertRule
from app.services.alerts.severity import AlertSeverity
from app.core.homelab_core import HomelabCore
from app.core.event_bus import Event
from app.services.alerts.events import AlertEvents


class AlertEngine:
    """Evaluates rules and dispatches alerts when thresholds or event triggers fire."""

    def process_metric(self, db: Session, key: str, value: float, message: str) -> Optional[Alert]:
        rules = db.query(AlertRule).filter(AlertRule.metric_name == key, AlertRule.enabled == True).all()

        for rule in rules:
            triggered = False
            if rule.comparison == ">" and value > rule.threshold:
                triggered = True
            elif rule.comparison == ">=" and value >= rule.threshold:
                triggered = True
            elif rule.comparison == "<" and value < rule.threshold:
                triggered = True
            elif rule.comparison == "==" and value == rule.threshold:
                triggered = True

            if triggered:
                alert = Alert(
                    rule_id=rule.id,
                    key=key,
                    message=f"{rule.name}: {message} (Value: {value}, Limit: {rule.threshold})",
                    severity=rule.severity,
                    status="ACTIVE"
                )
                db.add(alert)
                db.commit()
                db.refresh(alert)

                core = HomelabCore.instance()
                core.event_bus.publish(
                    Event(
                        name=AlertEvents.TRIGGERED,
                        source="alert_engine",
                        payload={"alert_id": alert.id, "severity": alert.severity, "message": alert.message}
                    )
                )
                return alert
        return None
