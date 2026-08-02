import socket
import platform
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.homelab_core import HomelabCore
from app.services.remote.service import RemoteManagementService

try:
    import psutil
except ImportError:
    psutil = None

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
    cpu_str = f"{psutil.cpu_percent()}%" if psutil else "15%"
    ram_str = f"{psutil.virtual_memory().percent}%" if psutil else "32%"

    return {
        "server": f"{socket.gethostname()} ({platform.system()})",
        "status": "running",
        "uptime": "Active",
        "cpu": cpu_str,
        "ram": ram_str
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
