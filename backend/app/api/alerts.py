from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.homelab_core import HomelabCore
from app.services.alerts.service import AlertService

router = APIRouter(prefix="/alerts", tags=["Intelligent Alerts"])


class RuleCreate(BaseModel):
    name: str
    metric_name: str
    threshold: float
    comparison: Optional[str] = ">"
    severity: Optional[str] = "WARNING"


def get_alert_service() -> AlertService:
    return HomelabCore.instance().get_service("alerts")


@router.get("")
def list_alerts(
    db: Session = Depends(get_db),
    service: AlertService = Depends(get_alert_service)
):
    alerts = service.get_alerts(db)
    return [
        {
            "id": a.id,
            "key": a.key,
            "message": a.message,
            "severity": a.severity,
            "status": a.status,
            "timestamp": a.timestamp
        } for a in alerts
    ]


@router.post("/rules")
def create_alert_rule(
    req: RuleCreate,
    db: Session = Depends(get_db),
    service: AlertService = Depends(get_alert_service)
):
    try:
        return service.create_rule(db, req.name, req.metric_name, req.threshold, req.comparison, req.severity)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
