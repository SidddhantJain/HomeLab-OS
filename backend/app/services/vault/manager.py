"""
HomeLab OS — Vault Manager

Coordinates locking, unlocking, active lifecycle checking,
and directory mapping for the secure private vault.
"""

from __future__ import annotations

import os
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session

from app.models.vault import VaultMetadata
from app.services.vault.lifecycle import VaultLifecycle, VaultState
from app.services.vault.encryption import VaultEncryptionManager


class VaultManager:
    """Orchestrates secure vault access, status updates, and LUKS locks."""

    def __init__(self, size_gb: int = 100, mount_point: str = "/mnt/vault") -> None:
        self.size_gb = size_gb
        self.mount_point = mount_point
        self._encryption = VaultEncryptionManager()
        self._lifecycle = VaultLifecycle(VaultState.LOCKED)

    @property
    def state(self) -> VaultState:
        return self._lifecycle.state

    def get_status(self, db: Session) -> Dict[str, Any]:
        """Query and return active vault parameters."""
        meta = db.query(VaultMetadata).order_by(VaultMetadata.created_at.desc()).first()
        if not meta:
            meta = VaultMetadata(
                status=self._lifecycle.state.value,
                capacity=float(self.size_gb),
                mount_location=self.mount_point
            )
            db.add(meta)
            db.commit()
            db.refresh(meta)

        return {
            "status": self._lifecycle.state.value,
            "capacity": meta.capacity,
            "mount_location": meta.mount_location,
            "encryption_type": meta.encryption_type,
            "last_unlock_time": meta.last_unlock_time
        }

    def unlock(self, db: Session, password: str) -> bool:
        """Unlock the encrypted container mapping."""
        if self._lifecycle.state != VaultState.LOCKED:
            return True

        self._lifecycle.transition(VaultState.UNLOCKING)
        self._encryption.create_vault_container(self.size_gb)

        # Attempt to open LUKS container
        success = self._encryption.open_luks(password)
        if not success:
            # Revert to LOCKED state
            self._lifecycle.transition(VaultState.LOCKED)
            return False

        # Attempt to format if first-time (simulated for dev envs)
        self._lifecycle.transition(VaultState.UNLOCKED)

        # Update database metadata state
        meta = db.query(VaultMetadata).order_by(VaultMetadata.created_at.desc()).first()
        if meta:
            meta.status = VaultState.UNLOCKED.value
            from datetime import datetime, timezone
            meta.last_unlock_time = datetime.now(timezone.utc)
            db.commit()

        # Ensure mount point exists
        try:
            os.makedirs(self.mount_point, exist_ok=True)
        except OSError:
            pass

        return True

    def lock(self, db: Session) -> bool:
        """Lock and close the encrypted vault container."""
        if self._lifecycle.state == VaultState.LOCKED:
            return True

        self._lifecycle.transition(VaultState.LOCKING)
        success = self._encryption.close_luks()

        if success:
            self._lifecycle.transition(VaultState.LOCKED)
            meta = db.query(VaultMetadata).order_by(VaultMetadata.created_at.desc()).first()
            if meta:
                meta.status = VaultState.LOCKED.value
                db.commit()
            return True

        # Fallback to current state if failed to close
        self._lifecycle.transition(VaultState.UNLOCKED)
        return False
class VaultEvents:
    UNLOCK_STARTED = "vault.unlock_started"
    UNLOCKED = "vault.unlocked"
    LOCKED = "vault.locked"
    FAILED_UNLOCK = "vault.failed_unlock"
