import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Boolean, JSON, ForeignKey
from app.core.database import Base


class RemoteDevice(Base):
    __tablename__ = "remote_devices"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    device_id = Column(String(100), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    public_key = Column(String(500), nullable=True)
    role = Column(String(50), default="REMOTE_VIEWER", nullable=False)  # REMOTE_ADMIN, REMOTE_OPERATOR, REMOTE_VIEWER
    last_seen = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    is_trusted = Column(Boolean, default=False, nullable=False)


class RemoteSession(Base):
    __tablename__ = "remote_sessions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), nullable=False)
    device_id = Column(String(100), nullable=False)
    ip_address = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    last_activity = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    is_expired = Column(Boolean, default=False, nullable=False)


class RemoteCommand(Base):
    __tablename__ = "remote_commands"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    command_name = Column(String(100), nullable=False)
    executed_by = Column(String(100), nullable=False)
    status = Column(String(50), default="COMPLETED", nullable=False)
    output = Column(String(1000), nullable=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


class RemoteAuditLog(Base):
    __tablename__ = "remote_audit_logs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user = Column(String(100), nullable=False)
    device = Column(String(100), nullable=False)
    action = Column(String(100), nullable=False)
    ip_address = Column(String(50), nullable=True)
    result = Column(String(50), default="SUCCESS", nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


class FileOperation(Base):
    __tablename__ = "file_operations"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    operation_type = Column(String(50), nullable=False)  # upload, download, move, delete, archive
    file_path = Column(String(500), nullable=False)
    user = Column(String(100), nullable=False)
    status = Column(String(50), default="SUCCESS", nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


class DeviceKey(Base):
    __tablename__ = "device_keys"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    device_id = Column(String(100), nullable=False)
    key_type = Column(String(50), default="TOTP_SECRET", nullable=False)
    secret_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
