"""
HomeLab OS — Threshold Evaluator
"""

from __future__ import annotations

from typing import Dict, Any, List


class ThresholdEvaluator:
    """Evaluates metrics against defined operational warning thresholds."""

    def __init__(self) -> None:
        self.default_thresholds = {
            "cpu_percent": 90.0,
            "ram_percent": 95.0,
            "disk_percent": 90.0,
            "temperature_c": 80.0
        }

    def evaluate(self, metric_name: str, value: float) -> List[Dict[str, Any]]:
        breaches = []
        limit = self.default_thresholds.get(metric_name)
        if limit is not None and value > limit:
            breaches.append({
                "metric": metric_name,
                "value": value,
                "limit": limit,
                "severity": "CRITICAL" if value > (limit + 5) else "WARNING"
            })
        return breaches
