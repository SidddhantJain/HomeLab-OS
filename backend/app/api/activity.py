from fastapi import APIRouter, Depends
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.homelab_core import HomelabCore
from app.services.activity.service import ActivityService

router = APIRouter(prefix="/activity", tags=["Activity Timeline"])


def get_activity_service() -> ActivityService:
    return HomelabCore.instance().get_service("activity")


@router.get("")
def get_activity_timeline(
    limit: int = 50,
    db: Session = Depends(get_db),
    service: ActivityService = Depends(get_activity_service)
):
    acts = service.get_timeline(db, limit)
    return [
        {
            "id": a.id,
            "event_type": a.event_type,
            "title": a.title,
            "description": a.description,
            "category": a.category,
            "severity": a.severity,
            "timestamp": a.timestamp
        } for a in acts
    ]
