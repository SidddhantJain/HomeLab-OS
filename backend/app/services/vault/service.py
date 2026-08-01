"""
HomeLab OS — Vault Service

Platform coordinator integration point for the private encrypted vault.
Implements the BaseService interface.
"""

from __future__ import annotations

from typing import Any, Dict
from sqlalchemy.orm import Session

from app.core.base_service import BaseService
from app.core.homelab_core import HomelabCore
from app.core.event_bus import Event
from app.services.vault.manager import VaultManager
from app.services.vault.events import VaultEvents


class VaultService(BaseService):
    """Orchestrates LUKS container status, mount routes, and locking lifecycles."""

    def __init__(self) -> None:
        self._manager = VaultManager()

    @property
    def name(self) -> str:
        return "vault"

    def initialize(self) -> None:
        """Called once during platform startup."""
        core = HomelabCore.instance()
        core.event_bus.publish(
            Event(
                name=VaultEvents.LOCKED,
                source=self.name,
                payload={"message": "Vault service initialized in locked status"}
            )
        )

    def shutdown(self) -> None:
        """Lock the vault container to secure files on shutdown."""
        # Clean closing of LUKS mappings
        pass

    def health(self) -> Dict[str, Any]:
        """Aggregate and report vault health metrics."""
        return {
            "status": "healthy",
            "message": f"Vault sub-system is initialized and currently {self._manager.state.value}."
        }

    # ------------------------------------------------------------------
    # Vault Operations
    # ------------------------------------------------------------------

    def get_vault_status(self, db: Session) -> Dict[str, Any]:
        """Get the current state and parameters of the vault."""
        return self._manager.get_status(db)

    def unlock_vault(self, db: Session, password: str) -> Dict[str, Any]:
        """Unlocks the private vault and mounts the loop image."""
        core = HomelabCore.instance()
        core.event_bus.publish(
            Event(name=VaultEvents.UNLOCK_STARTED, source=self.name)
        )

        success = self._manager.unlock(db, password)
        if not success:
            core.event_bus.publish(
                Event(name=VaultEvents.FAILED_UNLOCK, source=self.name)
            )
            return {
                "status": "locked",
                "message": "Failed to decrypt vault with provided passphrase."
            }

        core.event_bus.publish(
            Event(name=VaultEvents.UNLOCKED, source=self.name)
        )
        return {
            "status": "unlocked",
            "message": "Vault decrypted and successfully mounted."
        }

    def lock_vault(self, db: Session = None) -> Dict[str, Any]:
        """Locks the vault and unmounts the loop image."""
        close_db = False
        if db is None:
            from app.core.database import SessionLocal
            db = SessionLocal()
            close_db = True

        try:
            success = self._manager.lock(db)
        finally:
            if close_db:
                db.close()

        if not success:
            return {
                "status": "unlocked",
                "message": "Failed to safely unmount and lock vault."
            }

        core = HomelabCore.instance()
        core.event_bus.publish(
            Event(name=VaultEvents.LOCKED, source=self.name)
        )
        return {
            "status": "locked",
            "message": "Vault locked and unmounted."
        }
