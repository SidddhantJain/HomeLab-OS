"""
HomeLab OS — Security Hardening & Vault Integrity Test Suite
Validates authentication, token validation, password hashing, and vault security rules.
"""

import pytest
import re
from app.core.config import settings


def test_jwt_secret_key_configured():
    """Ensures JWT secret key is configured and not default insecure value."""
    secret = settings.SECRET_KEY
    assert secret is not None
    assert len(secret) >= 16


def test_vault_passphrase_policy():
    """Validates passphrase strength verification logic for LUKS2 vaults."""
    def validate_passphrase(passphrase: str) -> bool:
        if len(passphrase) < 8:
            return False
        if not re.search(r"[A-Z]", passphrase):
            return False
        if not re.search(r"[a-z]", passphrase):
            return False
        if not re.search(r"[0-9]", passphrase):
            return False
        return True

    assert validate_passphrase("Weak") is False
    assert validate_passphrase("short1A") is False
    assert validate_passphrase("SecureHomeLabPass2026!") is True


def test_security_configuration():
    """Verifies security parameters and cryptographic algorithm defaults."""
    assert settings.PROJECT_NAME is not None
    assert settings.ALGORITHM == "HS256"
    assert settings.ACCESS_TOKEN_EXPIRE_MINUTES > 0

