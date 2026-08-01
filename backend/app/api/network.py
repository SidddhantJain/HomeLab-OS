from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.homelab_core import HomelabCore
from app.services.network.service import NetworkService

router = APIRouter(prefix="/network", tags=["Network Management Center"])


class FriendlyNameReq(BaseModel):
    mac_address: str
    friendly_name: str


class ActionReq(BaseModel):
    target: str


def get_network_service() -> NetworkService:
    return HomelabCore.instance().get_service("network")


@router.get("/devices")
def list_network_devices(
    db: Session = Depends(get_db),
    service: NetworkService = Depends(get_network_service)
):
    devices = service.scan_and_sync_inventory(db)
    return [
        {
            "id": d.id,
            "ip_address": d.ip_address,
            "mac_address": d.mac_address,
            "hostname": d.hostname,
            "friendly_name": d.friendly_name,
            "vendor": d.vendor,
            "operating_system": d.operating_system,
            "connection_type": d.connection_type,
            "is_online": d.is_online
        } for d in devices
    ]


@router.post("/devices/friendly-name")
def set_friendly_name(
    req: FriendlyNameReq,
    db: Session = Depends(get_db),
    service: NetworkService = Depends(get_network_service)
):
    return service.set_friendly_name(db, req.mac_address, req.friendly_name)


@router.get("/topology")
def get_network_topology(
    service: NetworkService = Depends(get_network_service)
):
    return service.get_topology()


@router.post("/actions/ping")
def ping_device(
    req: ActionReq,
    service: NetworkService = Depends(get_network_service)
):
    return service.actions.ping_device(req.target)


@router.post("/actions/wol")
def send_wol_packet(
    req: ActionReq,
    service: NetworkService = Depends(get_network_service)
):
    return service.actions.send_wol(req.target)


@router.post("/emergency/toggle")
def toggle_emergency_hotspot(
    connected: bool,
    service: NetworkService = Depends(get_network_service)
):
    return service.emergency.handle_connectivity_change(connected)
