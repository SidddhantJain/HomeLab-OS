from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.homelab_core import HomelabCore
from app.services.remote.service import RemoteManagementService

router = APIRouter(prefix="/remote", tags=["Remote Control Layer"])


class RemoteCommandReq(BaseModel):
    command: str
    confirmation: Optional[bool] = True


class TerminalCommandReq(BaseModel):
    command: str


def get_remote_service() -> RemoteManagementService:
    return HomelabCore.instance().get_service("remote")


@router.get("/status")
def get_remote_server_status():
    return {
        "server": "Dell Inspiron 5558",
        "status": "running",
        "uptime": "15 days",
        "cpu": "22%",
        "ram": "45%"
    }


@router.post("/command")
def execute_remote_cmd(
    req: RemoteCommandReq,
    db: Session = Depends(get_db),
    service: RemoteManagementService = Depends(get_remote_service)
):
    try:
        return service.execute_remote_command(db, req.command)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/terminal")
def execute_terminal_cmd(
    req: TerminalCommandReq,
    service: RemoteManagementService = Depends(get_remote_service)
):
    return service.terminal.execute_terminal_command(req.command)
