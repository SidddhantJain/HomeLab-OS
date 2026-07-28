from fastapi import APIRouter
from typing import List, Dict, Any

router = APIRouter(prefix="/projects", tags=["Project Workspace"])


@router.get("")
def list_projects() -> List[Dict[str, Any]]:
    return [
        {
            "id": "proj-1",
            "name": "HomeLab OS",
            "language": "Python / JavaScript",
            "framework": "FastAPI & React",
            "status": "active",
            "path": "/mnt/storage/projects/homelab-os"
        }
    ]


@router.post("")
def create_project(project_data: Dict[str, Any]):
    return {
        "status": "created",
        "project": project_data
    }


@router.post("/{project_id}/backup")
def trigger_project_backup(project_id: str):
    return {
        "status": "started",
        "project_id": project_id,
        "job_id": "job-bk-001"
    }


@router.post("/{project_id}/snapshot")
def create_project_snapshot(project_id: str):
    return {
        "status": "completed",
        "project_id": project_id,
        "snapshot_id": "snap-001"
    }
