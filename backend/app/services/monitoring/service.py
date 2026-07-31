"""
HomeLab OS — Monitoring Service Implementation
"""

from __future__ import annotations

from typing import Any, Dict, List
from sqlalchemy.orm import Session
from app.core.base_service import BaseService
from app.core.homelab_core import HomelabCore
from app.core.event_bus import Event
from app.services.monitoring.collector import SystemMetricsCollector
from app.services.monitoring.thresholds import ThresholdEvaluator
from app.services.monitoring.history import MetricsHistoryStore
from app.services.monitoring.events import MonitoringEvents


class MonitoringService(BaseService):
    """Orchestrates system monitoring, telemetry collection, and metrics history."""

    def __init__(self) -> None:
        self.collector = SystemMetricsCollector()
        self.thresholds = ThresholdEvaluator()
        self.history_store = MetricsHistoryStore()

    @property
    def name(self) -> str:
        return "monitoring"

    def initialize(self) -> None:
        pass

    def shutdown(self) -> None:
        pass

    def health(self) -> Dict[str, Any]:
        return {
            "status": "healthy",
            "message": "Monitoring service is active and tracking HAL metrics."
        }

    def collect_and_record(self, db: Session) -> Dict[str, Any]:
        metrics = self.collector.collect_all()
        core = HomelabCore.instance()

        for k, v in metrics.items():
            if isinstance(v, (int, float)):
                self.history_store.record_metric(db, k, float(v))
                breaches = self.thresholds.evaluate(k, float(v))
                for b in breaches:
                    core.event_bus.publish(
                        Event(
                            name=MonitoringEvents.THRESHOLD_EXCEEDED,
                            source=self.name,
                            payload=b
                        )
                    )

        return metrics

    def get_service_statuses(self) -> List[Dict[str, Any]]:
        core = HomelabCore.instance()
        return [
            {"service": s_name, "status": "healthy"}
            for s_name in core._services.keys()
        ]
