"""
HomeLab OS — Monitoring Metrics History Store
"""

from __future__ import annotations

from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.models.metrics_history import MetricsHistory


class MetricsHistoryStore:
    """Manages storing and querying metric histories from the database."""

    def record_metric(self, db: Session, metric_name: str, metric_value: float, tags: Dict[str, Any] = None) -> MetricsHistory:
        rec = MetricsHistory(
            metric_name=metric_name,
            metric_value=metric_value,
            tags=tags or {}
        )
        db.add(rec)
        db.commit()
        db.refresh(rec)
        return rec

    def get_history(self, db: Session, metric_name: str, limit: int = 50) -> List[MetricsHistory]:
        return db.query(MetricsHistory).filter(
            MetricsHistory.metric_name == metric_name
        ).order_by(MetricsHistory.timestamp.desc()).limit(limit).all()
