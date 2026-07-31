from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.homelab_core import HomelabCore
from app.services.monitoring.service import MonitoringService

router = APIRouter(prefix="/monitoring", tags=["Monitoring & Observability"])


class ThresholdConfig(BaseModel):
    metric_name: str
    limit: float


def get_monitoring_service() -> MonitoringService:
    return HomelabCore.instance().get_service("monitoring")


@router.get("/status")
def get_monitoring_status(
    db: Session = Depends(get_db),
    service: MonitoringService = Depends(get_monitoring_service)
):
    return service.collect_and_record(db)


@router.get("/history")
def get_monitoring_history(
    metric_name: str = Query(..., description="Name of the metric to query"),
    limit: int = Query(50, ge=1, le=500),
    db: Session = Depends(get_db),
    service: MonitoringService = Depends(get_monitoring_service)
):
    history = service.history_store.get_history(db, metric_name, limit)
    return [
        {
            "id": h.id,
            "metric_name": h.metric_name,
            "value": h.metric_value,
            "timestamp": h.timestamp
        } for h in history
    ]


@router.get("/services")
def get_monitored_services(
    service: MonitoringService = Depends(get_monitoring_service)
):
    return service.get_service_statuses()


@router.post("/threshold")
def set_monitoring_threshold(
    config: ThresholdConfig,
    service: MonitoringService = Depends(get_monitoring_service)
):
    service.thresholds.default_thresholds[config.metric_name] = config.limit
    return {
        "status": "updated",
        "metric_name": config.metric_name,
        "new_threshold": config.limit
    }
