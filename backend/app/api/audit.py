from fastapi import APIRouter, Depends, Query
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.homelab_core import HomelabCore
from app.services.audit.service import AuditService

router = APIRouter(prefix="/audit", tags=["Audit System"])


def get_audit_service() -> AuditService:
    return HomelabCore.instance().get_service("audit")


@router.get("/search")
def search_audit_logs(
    query: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=500),
    db: Session = Depends(get_db),
    service: AuditService = Depends(get_audit_service)
):
    logs = service.search_audit_logs(db, category, query, limit)
    return [
        {
            "id": l.id,
            "action": l.action,
            "details": l.metadata_json,
            "user": l.user,
            "timestamp": l.timestamp
        } for l in logs

    ]
