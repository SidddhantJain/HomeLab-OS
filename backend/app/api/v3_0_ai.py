from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from app.hardware.ai_copilot import ai_copilot

router = APIRouter(prefix="/ai", tags=["Local AI Infrastructure Copilot"])


@router.post("/query")
def query_local_ai(prompt: str):
    """Execute natural language query against Local AI Copilot."""
    if not prompt:
        raise HTTPException(status_code=400, detail="prompt parameter is required.")
    return ai_copilot.query_copilot(prompt)


@router.post("/diagnose/container")
def diagnose_container_logs(container_name: str, log_snippet: str = "ERROR: connection refused on port 8080"):
    """Perform automated AI root-cause analysis on container error logs."""
    if not container_name:
        raise HTTPException(status_code=400, detail="container_name parameter is required.")
    return ai_copilot.diagnose_container_logs(container_name, log_snippet)
