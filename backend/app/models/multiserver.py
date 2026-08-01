import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Boolean, Integer, JSON
from app.core.database import Base


class ManagedServer(Base):
    __tablename__ = "managed_servers"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    host = Column(String(100), nullable=False)
    port = Column(Integer, default=8000, nullable=False)
    group_name = Column(String(50), default="Home", nullable=False)
    location = Column(String(100), default="Local Network", nullable=False)
    is_favorite = Column(Boolean, default=False, nullable=False)
    is_trusted = Column(Boolean, default=True, nullable=False)
    last_connected = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


class ServerGroup(Base):
    __tablename__ = "server_groups"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(255), nullable=True)


class ServerProfile(Base):
    __tablename__ = "server_profiles"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    profile_name = Column(String(50), nullable=False)
    api_token = Column(String(255), nullable=True)


class ServerConnection(Base):
    __tablename__ = "server_connections"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    server_id = Column(String(36), nullable=False)
    status = Column(String(20), default="CONNECTED", nullable=False)
    latency_ms = Column(Integer, default=1, nullable=False)


class ServerCertificate(Base):
    __tablename__ = "server_certificates"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    fingerprint = Column(String(255), unique=True, nullable=False)
    issued_to = Column(String(100), nullable=False)
