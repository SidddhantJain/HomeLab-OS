from fastapi import APIRouter
from app.schemas.system import SystemStatusResponse
from app.core.homelab_core import HomelabCore
from app.hardware.cpu import get_cpu_info
from app.hardware.memory import get_memory_info
from app.hardware.temperature import get_temperature_info

router = APIRouter(prefix="/system", tags=["System Management"])


@router.get("/status", response_model=SystemStatusResponse)
def get_system_status():
    core = HomelabCore.instance()
    cpu_data = get_cpu_info()
    mem_data = get_memory_info()
    temp_data = get_temperature_info()

    # Get cpu/ram percentages and temp values
    cpu_percent = sum(cpu_data.get("usage_percent", [0])) / max(len(cpu_data.get("usage_percent", [])), 1)
    ram_percent = mem_data.get("percent", 0.0)
    
    # Try finding CPU temperature
    temperatures = temp_data.get("sensors", {})
    cpu_temp = next((t for k, t in temperatures.items() if "cpu" in k.lower()), 40.0)

    return SystemStatusResponse(
        status=core.state_machine.state.value.lower(),
        server_name="Dell Inspiron 5558",
        cpu=round(cpu_percent, 1),
        ram=round(ram_percent, 1),
        temperature=round(cpu_temp, 1),
        uptime="12 days, 4 hours"
    )


@router.post("/maintenance")
def trigger_maintenance():
    core = HomelabCore.instance()
    from app.core.server_state import ServerState
    core.state_machine.transition(ServerState.MAINTENANCE)
    return {
        "status": "started",
        "action": "system_maintenance",
        "message": "Routine maintenance task initiated."
    }


@router.get("/telemetry")
def get_telemetry_metrics():
    from app.core.database import SessionLocal
    from app.models.workspace import Workspace
    from app.models.project import Project
    from app.models.snapshot import Snapshot
    from app.models.backup import BackupJob
    from app.models.download import DownloadTask
    from app.models.storage import StorageDevice

    db = SessionLocal()
    try:
        workspace_count = db.query(Workspace).filter(Workspace.status == "ACTIVE").count()
        project_count = db.query(Project).filter(Project.status == "ACTIVE").count()
        snapshot_count = db.query(Snapshot).count()
        backup_count = db.query(BackupJob).count()
        download_count = db.query(DownloadTask).filter(DownloadTask.status == "RUNNING").count()
        storage_count = db.query(StorageDevice).count()

        return {
            "workspace_usage": workspace_count,
            "project_size": project_count * 1.2, # Simulated average GB size
            "backup_status": "healthy" if backup_count > 0 else "inactive",
            "snapshot_count": snapshot_count,
            "download_activity": download_count,
            "storage_usage": storage_count
        }
    finally:
        db.close()


