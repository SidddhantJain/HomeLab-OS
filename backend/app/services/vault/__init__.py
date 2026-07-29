"""
HomeLab OS — Vault Service Integration
"""

from app.services.vault.service import VaultService
from app.services.vault.events import VaultEvents

__all__ = ["VaultService", "VaultEvents"]
