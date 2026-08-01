"""
HomeLab OS — Network Management Center Service Implementation
"""

from __future__ import annotations

from typing import Any, Dict, List
from sqlalchemy.orm import Session
from app.core.base_service import BaseService
from app.core.homelab_core import HomelabCore
from app.core.event_bus import Event
from app.services.network.discovery import NetworkDiscoveryEngine
from app.services.network.topology import NetworkTopologyEngine
from app.services.network.actions import NetworkActionsExecutor
from app.services.network.emergency import EmergencyHotspotManager
from app.services.network.events import NetworkEvents
from app.models.network import NetworkDevice, DeviceAlias, NetworkHistory, NetworkEvent


class NetworkService(BaseService):
    """Orchestrates network discovery, device inventory, topology, and emergency recovery."""

    def __init__(self) -> None:
        self.discovery = NetworkDiscoveryEngine()
        self.topology = NetworkTopologyEngine()
        self.actions = NetworkActionsExecutor()
        self.emergency = EmergencyHotspotManager()

    @property
    def name(self) -> str:
        return "network"

    def initialize(self) -> None:
        pass

    def shutdown(self) -> None:
        pass

    def health(self) -> Dict[str, Any]:
        return {
            "status": "healthy",
            "message": "Network Management Center Service is active."
        }

    def scan_and_sync_inventory(self, db: Session) -> List[NetworkDevice]:
        discovered = self.discovery.discover_devices()
        synced_devices = []

        for item in discovered:
            device = db.query(NetworkDevice).filter(NetworkDevice.mac_address == item["mac_address"]).first()
            if not device:
                device = NetworkDevice(
                    ip_address=item["ip_address"],
                    mac_address=item["mac_address"],
                    hostname=item["hostname"],
                    friendly_name=item["friendly_name"],
                    vendor=item["vendor"],
                    operating_system=item["operating_system"],
                    connection_type=item["connection_type"],
                    is_online=item["is_online"]
                )
                db.add(device)
            else:
                device.ip_address = item["ip_address"]
                device.is_online = item["is_online"]

            synced_devices.append(device)

        db.commit()
        return db.query(NetworkDevice).all()

    def set_friendly_name(self, db: Session, mac_address: str, friendly_name: str) -> NetworkDevice:
        device = db.query(NetworkDevice).filter(NetworkDevice.mac_address == mac_address).first()
        if device:
            device.friendly_name = friendly_name

        alias = db.query(DeviceAlias).filter(DeviceAlias.mac_address == mac_address).first()
        if not alias:
            alias = DeviceAlias(mac_address=mac_address, friendly_name=friendly_name)
            db.add(alias)
        else:
            alias.friendly_name = friendly_name

        db.commit()
        if device:
            db.refresh(device)
        return device

    def get_topology(self) -> Dict[str, Any]:

        return self.topology.build_topology_graph()
