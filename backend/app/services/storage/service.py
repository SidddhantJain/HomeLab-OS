"""
HomeLab OS — Storage Service

Platform coordinator integration point for all storage features.
Implements the BaseService interface.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from sqlalchemy.orm import Session

from app.core.base_service import BaseService
from app.core.homelab_core import HomelabCore
from app.core.event_bus import Event
from app.services.storage.detector import StorageDetector
from app.services.storage.manager import StorageManager
from app.services.storage.health import StorageHealthAnalyzer
from app.services.storage.models import StorageDevice, StoragePartition, StorageMount, StorageHealthRecord
from app.services.storage.events import StorageEvents


class StorageService(BaseService):
    """Orchestrates hardware storage, SMART checks, mounts, and alerts."""

    def __init__(self) -> None:
        self._detector = StorageDetector()
        self._manager = StorageManager()
        self._analyzer = StorageHealthAnalyzer()

    @property
    def name(self) -> str:
        return "storage"

    def initialize(self) -> None:
        """Called once during platform startup to setup configurations and detect disks."""
        # Initial scan is triggered during boot cycle
        core = HomelabCore.instance()
        core.event_bus.publish(
            Event(
                name=StorageEvents.DETECTED,
                source=self.name,
                payload={"message": "Storage service initialized"}
            )
        )

    def shutdown(self) -> None:
        """Called once during platform shutdown."""
        pass

    def health(self) -> Dict[str, Any]:
        """Aggregate and report storage health metrics."""
        return {
            "status": "healthy",
            "message": "Storage sub-system operating normally"
        }

    # ------------------------------------------------------------------
    # Storage Operations
    # ------------------------------------------------------------------

    def sync_devices(self, db: Session) -> List[StorageDevice]:
        """Scan physical hardware layout and reconcile database records."""
        detected = self._detector.detect_devices()
        synced_devices: List[StorageDevice] = []

        for info in detected:
            # Check if device is already registered by UUID
            dev = db.query(StorageDevice).filter(StorageDevice.uuid == info["uuid"]).first()
            if not dev:
                dev = StorageDevice(
                    device_name=info["device_name"],
                    uuid=info["uuid"],
                    filesystem=info["filesystem"],
                    capacity=info["capacity"],
                    device_type=info["device_type"],
                    status="active"
                )
                db.add(dev)
                db.commit()
                db.refresh(dev)

            # Ensure health record is current
            h_data = self._analyzer.analyze_health(dev.device_name)
            record = StorageHealthRecord(
                device_id=dev.id,
                smart_status=h_data["smart_status"],
                temperature_c=h_data["temperature_c"],
                bad_sectors=h_data["bad_sectors"],
                read_error_rate=h_data["read_error_rate"],
                write_error_rate=h_data["write_error_rate"],
                power_on_hours=h_data["power_on_hours"]
            )
            db.add(record)

            # Update partition structures if not set up
            partition = db.query(StoragePartition).filter(StoragePartition.device_id == dev.id).first()
            if not partition:
                partition = StoragePartition(
                    device_id=dev.id,
                    partition_name=f"{dev.device_name}p1",
                    uuid=dev.uuid,
                    filesystem=dev.filesystem,
                    capacity=dev.capacity,
                    mount_point=info["mount_location"],
                    used_space=info["used_space"],
                    free_space=info["free_space"]
                )
                db.add(partition)

            db.commit()
            synced_devices.append(dev)

        return synced_devices

    def get_devices(self, db: Session) -> List[StorageDevice]:
        """Retrieve all registered storage devices, synchronizing first if empty."""
        devices = db.query(StorageDevice).all()
        if not devices:
            return self.sync_devices(db)
        return devices

    def get_device(self, db: Session, device_id: str) -> Optional[StorageDevice]:
        """Retrieve details for a single device by ID."""
        return db.query(StorageDevice).filter(StorageDevice.id == device_id).first()

    def get_health_records(self, db: Session) -> List[StorageHealthRecord]:
        """Get latest health records for all devices."""
        devices = self.get_devices(db)
        latest_records: List[StorageHealthRecord] = []
        for d in devices:
            record = db.query(StorageHealthRecord).filter(
                StorageHealthRecord.device_id == d.id
            ).order_by(StorageHealthRecord.recorded_at.desc()).first()
            if record:
                latest_records.append(record)
        return latest_records

    def mount_device(self, db: Session, device_id: str, mount_point: str) -> Dict[str, Any]:
        """Mount a device and dispatch a storage.mounted event."""
        device = self.get_device(db, device_id)
        if not device:
            raise KeyError(f"Device '{device_id}' does not exist.")

        mount = self._manager.mount(db, device, mount_point)
        # Update device status
        device.status = "active"
        db.commit()

        # Update partition record
        partition = db.query(StoragePartition).filter(StoragePartition.device_id == device.id).first()
        if partition:
            partition.mount_point = mount_point
            db.commit()

        # Dispatch event
        core = HomelabCore.instance()
        core.event_bus.publish(
            Event(
                name=StorageEvents.MOUNTED,
                source=self.name,
                payload={
                    "device_id": device.id,
                    "device_name": device.device_name,
                    "mount_point": mount_point
                }
            )
        )
        return {
            "status": "mounted",
            "device_id": device.id,
            "mount_point": mount_point,
            "message": f"Storage device '{device.device_name}' mounted successfully."
        }

    def unmount_device(self, db: Session, device_id: str) -> Dict[str, Any]:
        """Unmount a device and dispatch a storage.unmounted event."""
        device = self.get_device(db, device_id)
        if not device:
            raise KeyError(f"Device '{device_id}' does not exist.")

        success = self._manager.unmount(db, device)
        if not success:
            raise ValueError(f"Device '{device_id}' is not mounted.")

        # Update partition record
        partition = db.query(StoragePartition).filter(StoragePartition.device_id == device.id).first()
        if partition:
            partition.mount_point = None
            db.commit()

        # Dispatch event
        core = HomelabCore.instance()
        core.event_bus.publish(
            Event(
                name=StorageEvents.UNMOUNTED,
                source=self.name,
                payload={
                    "device_id": device.id,
                    "device_name": device.device_name
                }
            )
        )
        return {
            "status": "unmounted",
            "device_id": device.id,
            "message": f"Storage device '{device.device_name}' unmounted successfully."
        }
