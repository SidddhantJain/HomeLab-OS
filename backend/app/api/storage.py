from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.homelab_core import HomelabCore
from app.services.storage.service import StorageService

router = APIRouter(prefix="/storage", tags=["Storage Management"])


def get_storage_service() -> StorageService:
    core = HomelabCore.instance()
    return core.get_service("storage")


@router.get("/devices")
def list_storage_devices(
    db: Session = Depends(get_db),
    service: StorageService = Depends(get_storage_service)
) -> List[Dict[str, Any]]:
    devices = service.get_devices(db)
    result = []
    for d in devices:
        result.append({
            "id": d.id,
            "name": d.device_name,
            "uuid": d.uuid,
            "filesystem": d.filesystem,
            "capacity_gb": d.capacity,
            "type": d.device_type,
            "status": d.status
        })
    return result


@router.get("/devices/{id}")
def get_device_details(
    id: str,
    db: Session = Depends(get_db),
    service: StorageService = Depends(get_storage_service)
):
    device = service.get_device(db, id)
    if not device:
        raise HTTPException(status_code=404, detail=f"Device '{id}' not found.")
    return {
        "id": device.id,
        "name": device.device_name,
        "uuid": device.uuid,
        "filesystem": device.filesystem,
        "capacity_gb": device.capacity,
        "type": device.device_type,
        "status": device.status,
        "created_at": device.created_at
    }


@router.get("/health")
def get_storage_health(
    db: Session = Depends(get_db),
    service: StorageService = Depends(get_storage_service)
):
    records = service.get_health_records(db)
    health_status = "healthy"
    details = []
    
    for r in records:
        if r.smart_status != "PASSED":
            health_status = "degraded"
        details.append({
            "device_id": r.device_id,
            "smart_status": r.smart_status,
            "temperature_c": r.temperature_c,
            "bad_sectors": r.bad_sectors
        })
        
    return {
        "status": health_status,
        "records": details
    }


@router.post("/mount/{id}")
def mount_storage(
    id: str,
    mount_point: str = "/mnt/homelab-storage",
    db: Session = Depends(get_db),
    service: StorageService = Depends(get_storage_service)
):
    try:
        return service.mount_device(db, id, mount_point)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/unmount/{id}")
def unmount_storage(
    id: str,
    db: Session = Depends(get_db),
    service: StorageService = Depends(get_storage_service)
):
    try:
        return service.unmount_device(db, id)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

