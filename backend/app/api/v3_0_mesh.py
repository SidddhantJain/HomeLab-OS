from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from app.hardware.mesh_network import mesh_engine

router = APIRouter(prefix="/mesh", tags=["Zero-Trust Mesh Network Overlay"])


@router.get("/status", response_model=Dict[str, Any])
def get_mesh_network_status():
    """Retrieve WireGuard / Tailscale zero-trust mesh overlay network state."""
    return mesh_engine.get_mesh_status()


@router.post("/peer/add")
def add_mesh_peer_device(device_name: str, public_key: str = ""):
    """Pair and register a new peer device into zero-trust mesh network."""
    if not device_name:
        raise HTTPException(status_code=400, detail="device_name parameter is required.")
    return mesh_engine.add_mesh_peer(device_name, public_key)
