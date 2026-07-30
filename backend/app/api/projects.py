from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.homelab_core import HomelabCore
from app.services.projects.service import ProjectService

router = APIRouter(prefix="/projects", tags=["Project Workspace"])


class ProjectCreate(BaseModel):
    name: str
    path: str
    description: Optional[str] = None


def get_project_service() -> ProjectService:
    return HomelabCore.instance().get_service("projects")


@router.get("")
def list_projects(
    db: Session = Depends(get_db),
    service: ProjectService = Depends(get_project_service)
) -> List[Dict[str, Any]]:
    projects = service.get_projects(db)
    result = []
    for p in projects:
        meta = p.metadata_rel
        result.append({
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "language": meta.language if meta else "unknown",
            "framework": meta.framework if meta else "unknown",
            "status": p.status,
            "path": meta.storage if meta else "unknown"
        })
    return result


@router.post("")
def create_project(
    req: ProjectCreate,
    db: Session = Depends(get_db),
    service: ProjectService = Depends(get_project_service)
):
    try:
        return service.register_project(db, req.name, req.path, req.description)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{project_id}/snapshot")
def create_project_snapshot(
    project_id: str,
    db: Session = Depends(get_db),
    service: ProjectService = Depends(get_project_service)
):
    try:
        snap = service.create_snapshot(db, project_id)  # Using project_id as virtual workspace boundary
        return {
            "status": "completed",
            "project_id": project_id,
            "snapshot_id": snap.id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{project_id}/snapshots")
def get_project_snapshots(
    project_id: str,
    db: Session = Depends(get_db),
    service: ProjectService = Depends(get_project_service)
):
    return service.get_snapshots(db, project_id)


@router.post("/snapshots/{snapshot_id}/restore")
def restore_project_snapshot(
    snapshot_id: str,
    db: Session = Depends(get_db),
    service: ProjectService = Depends(get_project_service)
):
    success = service.restore_snapshot(db, snapshot_id)
    if not success:
        raise HTTPException(status_code=404, detail="Snapshot not found.")
    return {"status": "restored"}

