from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.homelab_core import HomelabCore
from app.services.workflow.service import WorkflowService

router = APIRouter(prefix="/workflow", tags=["Automation Workflow Engine"])


class WorkflowCreate(BaseModel):
    name: str
    trigger_type: str
    actions: List[Any]
    conditions: Optional[Dict[str, Any]] = None


def get_workflow_service() -> WorkflowService:
    return HomelabCore.instance().get_service("workflow")


@router.get("")
def list_workflows(
    db: Session = Depends(get_db),
    service: WorkflowService = Depends(get_workflow_service)
):
    jobs = service.get_workflows(db)
    return [
        {
            "id": j.id,
            "name": j.name,
            "trigger_type": j.trigger_type,
            "enabled": j.enabled,
            "created_at": j.created_at
        } for j in jobs
    ]


@router.post("")
def create_workflow(
    req: WorkflowCreate,
    db: Session = Depends(get_db),
    service: WorkflowService = Depends(get_workflow_service)
):
    try:
        return service.create_workflow(db, req.name, req.trigger_type, req.actions, req.conditions)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{job_id}/execute")
def execute_workflow_manually(
    job_id: str,
    db: Session = Depends(get_db),
    service: WorkflowService = Depends(get_workflow_service)
):
    try:
        return service.execute_job(db, job_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
