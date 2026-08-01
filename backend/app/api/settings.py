from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.homelab_core import HomelabCore
from app.services.settings.service import SettingsService

router = APIRouter(prefix="/settings", tags=["Settings Center"])


class SettingsUpdateReq(BaseModel):
    theme: Optional[str] = None
    language: Optional[str] = None
    timezone: Optional[str] = None


def get_settings_service() -> SettingsService:
    return HomelabCore.instance().get_service("settings")


@router.get("")
def get_user_settings(
    db: Session = Depends(get_db),
    service: SettingsService = Depends(get_settings_service)
):
    return service.get_settings(db)


@router.put("")
def update_user_settings(
    req: SettingsUpdateReq,
    db: Session = Depends(get_db),
    service: SettingsService = Depends(get_settings_service)
):
    return service.update_settings(db, theme=req.theme, language=req.language, timezone=req.timezone)
