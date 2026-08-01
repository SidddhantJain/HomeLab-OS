from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.homelab_core import HomelabCore
from app.services.multiserver.service import MultiServerService

router = APIRouter(prefix="/multiserver", tags=["Multi-Server Management"])


class AddServerReq(BaseModel):
    name: str
    host: str
    port: Optional[int] = 8000
    group_name: Optional[str] = "Home"


def get_multiserver_service() -> MultiServerService:
    return HomelabCore.instance().get_service("multiserver")


@router.get("")
def list_managed_servers(
    db: Session = Depends(get_db),
    service: MultiServerService = Depends(get_multiserver_service)
):
    servers = service.list_servers(db)
    return [
        {
            "id": s.id,
            "name": s.name,
            "host": s.host,
            "port": s.port,
            "group_name": s.group_name,
            "location": s.location,
            "is_favorite": s.is_favorite,
            "is_trusted": s.is_trusted,
            "last_connected": s.last_connected
        } for s in servers
    ]


@router.post("")
def add_managed_server(
    req: AddServerReq,
    db: Session = Depends(get_db),
    service: MultiServerService = Depends(get_multiserver_service)
):
    return service.add_server(db, req.name, req.host, req.port, req.group_name)
