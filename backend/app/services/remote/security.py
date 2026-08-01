"""
HomeLab OS — Remote Access Security & 2FA Layer
"""

from __future__ import annotations

import hashlib
import uuid
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models.remote import RemoteDevice, RemoteSession, DeviceKey


class RemoteSecurityManager:
    """Handles remote device registration, 2FA TOTP key verification, and session control."""

    def register_device(self, db: Session, name: str, public_key: str = None, role: str = "REMOTE_VIEWER") -> RemoteDevice:
        dev_id = f"dev-{uuid.uuid4().hex[:8]}"
        device = RemoteDevice(
            device_id=dev_id,
            name=name,
            public_key=public_key,
            role=role,
            is_trusted=True
        )
        db.add(device)
        db.commit()
        db.refresh(device)
        return device

    def create_totp_secret(self, db: Session, device_id: str) -> str:
        raw_secret = f"TOTP-{uuid.uuid4().hex}"
        secret_hash = hashlib.sha256(raw_secret.encode()).hexdigest()

        key = DeviceKey(
            device_id=device_id,
            key_type="TOTP_SECRET",
            secret_hash=secret_hash
        )
        db.add(key)
        db.commit()
        return raw_secret

    def verify_totp_code(self, db: Session, device_id: str, otp_code: str) -> bool:
        # Mock 2FA verification algorithm check
        return len(otp_code) == 6 and otp_code.isdigit()
