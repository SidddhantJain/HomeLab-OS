from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from app.hardware.hypervisor import hypervisor_hal

router = APIRouter(prefix="/v4/hypervisor", tags=["v4_0-hypervisor"])

class CreateVMRequest(BaseModel):
    name: str
    vm_type: str = "kvm"
    vcpus: int = 2
    ram_mb: int = 2048
    disk_gb: int = 20
    passthrough_pcie: Optional[List[str]] = None

class ControlVMRequest(BaseModel):
    action: str  # start, stop, pause, restart

class CreateSANPoolRequest(BaseModel):
    name: str
    raid_level: str = "RAID-Z2"
    drives: Optional[List[str]] = None

@router.get("/status")
def get_hypervisor_status() -> Dict[str, Any]:
    """Returns status of Type-1 Hypervisor subsystem and capacity."""
    return hypervisor_hal.get_hypervisor_status()

@router.get("/vms")
def list_vms() -> List[Dict[str, Any]]:
    """Returns list of microVM instances."""
    return hypervisor_hal.list_vms()

@router.post("/vms")
def create_vm(req: CreateVMRequest) -> Dict[str, Any]:
    """Provisions a new MicroVM instance."""
    return hypervisor_hal.create_vm(
        name=req.name,
        vm_type=req.vm_type,
        vcpus=req.vcpus,
        ram_mb=req.ram_mb,
        disk_gb=req.disk_gb,
        passthrough_pcie=req.passthrough_pcie
    )

@router.post("/vms/{vm_id}/control")
def control_vm(vm_id: str, req: ControlVMRequest) -> Dict[str, Any]:
    """Executes state control (start, stop, pause, restart) on a MicroVM."""
    try:
        return hypervisor_hal.control_vm(vm_id=vm_id, action=req.action)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/vms/{vm_id}")
def delete_vm(vm_id: str) -> Dict[str, Any]:
    """Deletes a MicroVM instance."""
    success = hypervisor_hal.delete_vm(vm_id=vm_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"MicroVM '{vm_id}' not found")
    return {"status": "success", "message": f"MicroVM {vm_id} deleted"}

@router.get("/pcie-devices")
def list_pcie_devices() -> List[Dict[str, Any]]:
    """Scans host hardware for PCIe devices available for passthrough."""
    return hypervisor_hal.list_pcie_devices()

@router.get("/san-pools")
def get_san_pools() -> List[Dict[str, Any]]:
    """Returns Virtual SAN storage pools."""
    return hypervisor_hal.get_san_pools()

@router.post("/san-pools")
def create_san_pool(req: CreateSANPoolRequest) -> Dict[str, Any]:
    """Creates a new Virtual SAN storage pool."""
    return hypervisor_hal.create_san_pool(
        name=req.name,
        raid_level=req.raid_level,
        drives=req.drives
    )
