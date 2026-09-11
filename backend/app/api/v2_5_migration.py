from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from app.hardware.migration import migration_engine

router = APIRouter(prefix="/cluster/migration", tags=["Cluster Live Migration"])


@router.post("/start")
def start_live_migration(workload_id: str, target_node_ip: str, workload_type: str = "container"):
    """Initiate live container or VM migration to target cluster node."""
    if not workload_id or not target_node_ip:
        raise HTTPException(status_code=400, detail="Workload ID and target node IP are required.")

    return migration_engine.initiate_migration(workload_id, target_node_ip, workload_type)


@router.get("/status/{migration_id}")
def get_migration_status(migration_id: str):
    """Retrieve progress status of live migration task."""
    res = migration_engine.get_migration_status(migration_id)
    if res.get("status") == "NOT_FOUND":
        raise HTTPException(status_code=404, detail=f"Migration task '{migration_id}' not found.")
    return res


@router.get("/list", response_model=List[Dict[str, Any]])
def list_active_migrations():
    """List all active and recent cluster workload migrations."""
    return migration_engine.list_migrations()
