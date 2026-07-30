from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.homelab_core import HomelabCore
from app.services.workspace.service import WorkspaceService

router = APIRouter(prefix="/workspaces", tags=["Workspaces"])


class WorkspaceCreate(BaseModel):
    name: str
    owner: str
    description: Optional[str] = None


def get_workspace_service() -> WorkspaceService:
    return HomelabCore.instance().get_service("workspace")


@router.get("")
def list_workspaces(
    db: Session = Depends(get_db),
    service: WorkspaceService = Depends(get_workspace_service)
):
    workspaces = service.get_workspaces(db)
    return [
        {
            "id": w.id,
            "name": w.name,
            "description": w.description,
            "owner": w.owner,
            "storage_location": w.storage_location,
            "size_gb": w.size,
            "status": w.status,
            "created_at": w.created_at
        } for w in workspaces
    ]


@router.post("")
def create_workspace(
    req: WorkspaceCreate,
    db: Session = Depends(get_db),
    service: WorkspaceService = Depends(get_workspace_service)
):
    try:
        return service.create_workspace(db, req.name, req.owner, req.description)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{id}/archive")
def archive_workspace(
    id: str,
    db: Session = Depends(get_db),
    service: WorkspaceService = Depends(get_workspace_service)
):
    success = service.archive_workspace(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="Workspace not found.")
    return {"status": "archived"}


@router.post("/{id}/restore")
def restore_workspace(
    id: str,
    db: Session = Depends(get_db),
    service: WorkspaceService = Depends(get_workspace_service)
):
    success = service.restore_workspace(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="Workspace not found.")
    return {"status": "active"}


@router.delete("/{id}")
def delete_workspace(
    id: str,
    db: Session = Depends(get_db),
    service: WorkspaceService = Depends(get_workspace_service)
):
    success = service.delete_workspace(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="Workspace not found.")
    return {"status": "deleted"}
