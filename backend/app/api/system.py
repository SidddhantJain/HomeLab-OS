from fastapi import APIRouter
from app.schemas.system import SystemStatusResponse

router = APIRouter(prefix="/system", tags=["System Management"])


@router.get("/status", response_model=SystemStatusResponse)
def get_system_status():
    return SystemStatusResponse(
        status="running",
        server_name="Dell Inspiron 5558",
        cpu=18.4,
        ram=48.2,
        temperature=44.5,
        uptime="12 days, 4 hours"
    )


@router.post("/maintenance")
def trigger_maintenance():
    return {
        "status": "started",
        "action": "system_maintenance",
        "message": "Routine maintenance task initiated in background."
    }
