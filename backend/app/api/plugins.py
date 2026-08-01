from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.homelab_core import HomelabCore
from app.services.plugins.service import PluginService

router = APIRouter(prefix="/plugins", tags=["Plugin Marketplace Foundation"])


class PluginRegisterReq(BaseModel):
    plugin_id: str
    name: str
    version: Optional[str] = "1.0.0"
    author: Optional[str] = "HomeLab OS"
    description: Optional[str] = ""
    permissions: Optional[List[str]] = None


def get_plugin_service() -> PluginService:
    return HomelabCore.instance().get_service("plugins")


@router.get("")
def list_plugins(
    db: Session = Depends(get_db),
    service: PluginService = Depends(get_plugin_service)
):
    plugins = service.list_plugins(db)
    return [
        {
            "id": p.id,
            "plugin_id": p.plugin_id,
            "name": p.name,
            "version": p.version,
            "enabled": p.enabled,
            "author": p.author
        } for p in plugins
    ]


@router.post("/register")
def register_plugin(
    req: PluginRegisterReq,
    db: Session = Depends(get_db),
    service: PluginService = Depends(get_plugin_service)
):
    return service.register_plugin(db, req.plugin_id, req.name, req.version, req.author, req.description, req.permissions)
