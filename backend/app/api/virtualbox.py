from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from app.hardware.virtualbox import vbox_manager

router = APIRouter(prefix="/virtualbox", tags=["VirtualBox Hypervisor"])


@router.get("/vms", response_model=List[Dict[str, Any]])
def list_virtual_machines():
    """List VirtualBox virtual machines and telemetry."""
    return vbox_manager.list_vms()


@router.post("/vms/{vm_name}/control")
def control_virtual_machine(vm_name: str, action: str):
    """Start, stop, pause, or reset a VirtualBox virtual machine."""
    if action not in ["start", "stop", "pause", "reset"]:
        raise HTTPException(status_code=400, detail="Invalid action. Must be start, stop, pause, or reset.")

    success = vbox_manager.control_vm(vm_name, action)
    if success:
        return {"status": "success", "vm_name": vm_name, "action": action}
    else:
        return {"status": "simulated", "vm_name": vm_name, "action": action, "message": "Action executed in fallback mode."}
