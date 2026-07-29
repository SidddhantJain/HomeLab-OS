"""
HomeLab OS — Telemetry Framework

Provides a unified telemetry collector. Services report health status,
warnings, metrics, and errors through this central registry.
"""

from __future__ import annotations

import threading
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


class TelemetryCollector:
    """Thread-safe telemetry and health collector for HomeLab OS.

    Usage:
        telemetry = TelemetryCollector()
        telemetry.record_metric("cpu_usage", 42.5, tags={"core": "all"})
        telemetry.record_alert("high_temp", "CPU temperature exceeds 80C", severity="critical")
    """

    def __init__(self) -> None:
        self._metrics: List[Dict[str, Any]] = []
        self._alerts: List[Dict[str, Any]] = []
        self._service_healths: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.Lock()

    def record_metric(self, name: str, value: Any, tags: Optional[Dict[str, str]] = None) -> None:
        """Record a single telemetry metric measurement."""
        with self._lock:
            self._metrics.append({
                "name": name,
                "value": value,
                "tags": tags or {},
                "timestamp": datetime.now(timezone.utc)
            })
            # Cap metrics in memory to prevent leak
            if len(self._metrics) > 1000:
                self._metrics.pop(0)

    def record_alert(self, key: str, message: str, severity: str = "warning") -> None:
        """Record a system alert."""
        with self._lock:
            self._alerts.append({
                "key": key,
                "message": message,
                "severity": severity,
                "timestamp": datetime.now(timezone.utc),
                "resolved": False
            })
            if len(self._alerts) > 100:
                self._alerts.pop(0)

    def update_service_health(self, service_name: str, health_data: Dict[str, Any]) -> None:
        """Update cached health status for a specific service."""
        with self._lock:
            self._service_healths[service_name] = {
                "health": health_data,
                "last_update": datetime.now(timezone.utc)
            }

    def get_health_report(self) -> Dict[str, Any]:
        """Aggregate health status of all registered services."""
        with self._lock:
            overall_status = "healthy"
            for s_data in self._service_healths.values():
                status = s_data.get("health", {}).get("status", "unknown")
                if status == "unhealthy":
                    overall_status = "unhealthy"
                    break
                elif status == "degraded" and overall_status == "healthy":
                    overall_status = "degraded"

            return {
                "status": overall_status,
                "services": self._service_healths,
                "timestamp": datetime.now(timezone.utc)
            }

    def get_recent_metrics(self, count: int = 100) -> List[Dict[str, Any]]:
        """Get the most recent metric records."""
        with self._lock:
            return list(self._metrics[-count:])

    def get_active_alerts(self) -> List[Dict[str, Any]]:
        """Get list of unresolved active alerts."""
        with self._lock:
            return [a for a in self._alerts if not a.get("resolved", False)]
