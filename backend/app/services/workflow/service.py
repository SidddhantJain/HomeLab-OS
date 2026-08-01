"""
HomeLab OS — Automation Workflow Service
"""

from __future__ import annotations

from typing import Any, Dict, List
from sqlalchemy.orm import Session
from app.core.base_service import BaseService
from app.models.workflow import WorkflowJob, WorkflowHistory
from app.services.workflow.engine import WorkflowEngine


class WorkflowService(BaseService):
    """Integrates workflow jobs, condition evaluations, and action triggers."""

    def __init__(self) -> None:
        self.engine = WorkflowEngine()

    @property
    def name(self) -> str:
        return "workflow"

    def initialize(self) -> None:
        pass

    def shutdown(self) -> None:
        pass

    def health(self) -> Dict[str, Any]:
        return {
            "status": "healthy",
            "message": "Workflow Engine is operational."
        }

    def create_workflow(self, db: Session, name: str, trigger_type: str, actions: List[Any], conditions: Dict[str, Any] = None) -> WorkflowJob:
        job = WorkflowJob(
            name=name,
            trigger_type=trigger_type,
            conditions=conditions or {},
            actions=actions,
            enabled=True
        )
        db.add(job)
        db.commit()
        db.refresh(job)
        return job

    def execute_job(self, db: Session, job_id: str, context: Dict[str, Any] = None) -> WorkflowHistory:
        job = db.query(WorkflowJob).filter(WorkflowJob.id == job_id).first()
        if not job:
            raise ValueError(f"WorkflowJob '{job_id}' not found.")
        return self.engine.run_workflow(db, job, context)

    def get_workflows(self, db: Session) -> List[WorkflowJob]:
        return db.query(WorkflowJob).all()
