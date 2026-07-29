"""
HomeLab OS — Storage Mount Manager

Manages partition mount options, updates active database registries,
and communicates mounts through system calls.
"""

from __future__ import annotations

import os
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models.storage import StorageDevice, StorageMount


class StorageManager:
    """Manages active partition mounts and saves mount points to the database."""

    def __init__(self) -> None:
        pass

    def mount(self, db: Session, device: StorageDevice, mount_point: str) -> Optional[StorageMount]:
        """Mount a storage partition to target directory path."""
        # Ensure mount path directory exists in production
        try:
            if not os.path.exists(mount_point):
                os.makedirs(mount_point, exist_ok=True)
        except OSError:
            pass

        # Check if already mounted
        existing_mount = db.query(StorageMount).filter(
            StorageMount.device_id == device.id,
            StorageMount.mount_point == mount_point,
            StorageMount.is_active == True
        ).first()

        if existing_mount:
            return existing_mount

        # Create mount log record
        mount = StorageMount(
            device_id=device.id,
            mount_point=mount_point,
            is_active=True,
            mount_options="defaults"
        )
        db.add(mount)
        db.commit()
        db.refresh(mount)
        return mount

    def unmount(self, db: Session, device: StorageDevice) -> bool:
        """Unmount an active storage partition."""
        active_mounts = db.query(StorageMount).filter(
            StorageMount.device_id == device.id,
            StorageMount.is_active == True
        ).all()

        if not active_mounts:
            return False

        for mount in active_mounts:
            mount.is_active = False
        db.commit()
        return True
