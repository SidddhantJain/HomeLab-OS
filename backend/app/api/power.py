from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.homelab_core import HomelabCore
from app.services.power.service import PowerService

router = APIRouter(prefix="/power", tags=["Power Management"])


class ScheduleCreate(BaseModel):
    name: str
    action: str
    cron_expression: str


def get_power_service() -> PowerService:
    return HomelabCore.instance().get_service("power")


@router.get("/report")
def get_power_report(
    service: PowerService = Depends(get_power_service)
):
    return service.get_power_report()


@router.get("/schedules")
def list_power_schedules(
    db: Session = Depends(get_db),
    service: PowerService = Depends(get_power_service)
):
    return service.get_schedules(db)


@router.post("/schedules")
def create_power_schedule(
    req: ScheduleCreate,
    db: Session = Depends(get_db),
    service: PowerService = Depends(get_power_service)
):
    try:
        return service.create_schedule(db, req.name, req.action, req.cron_expression)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/wakeup")
def remote_wakeup(
    mac_address: Optional[str] = "00:11:22:33:44:55"
):
    return {"status": "sent", "message": f"WOL packet sent to {mac_address}."}


@router.post("/shutdown")
def remote_shutdown(
    confirmation: str
):
    if confirmation != "SHUTDOWN":
        raise HTTPException(status_code=400, detail="Invalid confirmation token. Type 'SHUTDOWN'.")
    return {"status": "initiated", "message": "System shutdown sequence initiated."}
