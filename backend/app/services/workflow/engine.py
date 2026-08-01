"""
HomeLab OS — Workflow Conditions & Execution Engine
"""

from __future__ import annotations

from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from app.models.workflow import WorkflowJob, WorkflowHistory
from app.services.workflow.actions import WorkflowActionExecutor


class WorkflowConditionsEvaluator:
    """Evaluates IF conditions prior to executing workflow THEN actions."""

    def evaluate(self, conditions: Dict[str, Any], context: Dict[str, Any]) -> bool:
        if not conditions:
            return True
        # E.g., check disk usage > 90%
        field = conditions.get("field")
        op = conditions.get("operator", ">")
        limit = conditions.get("value")

        actual = context.get(field)
        if actual is None or limit is None:
            return True

        if op == ">":
            return actual > limit
        elif op == ">=":
            return actual >= limit
        elif op == "<":
            return actual < limit
        elif op == "==":
            return actual == limit
        return True


class WorkflowEngine:
    """Manages workflow job executions and records history."""

    def __init__(self) -> None:
        self.evaluator = WorkflowConditionsEvaluator()
        self.executor = WorkflowActionExecutor()

    def run_workflow(self, db: Session, job: WorkflowJob, context: Dict[str, Any] = None) -> WorkflowHistory:
        context = context or {}
        passed = self.evaluator.evaluate(job.conditions or {}, context)

        status = "SKIPPED"
        details = {}

        if passed:
            results = []
            for act in job.actions:
                act_name = act.get("name") if isinstance(act, dict) else str(act)
                payload = act.get("payload", {}) if isinstance(act, dict) else {}
                res = self.executor.execute(act_name, payload)
                results.append({"action": act_name, "success": res})
            status = "SUCCESS"
            details = {"actions_executed": results}

        hist = WorkflowHistory(
            workflow_id=job.id,
            status=status,
            details=details
        )
        db.add(hist)
        db.commit()
        db.refresh(hist)
        return hist
