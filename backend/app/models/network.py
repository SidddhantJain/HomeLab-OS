import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Float, Boolean, Integer, JSON, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class NetworkDevice(Base):
    __tablename__ = "network_devices"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    ip_address = Column(String(50), nullable=False, index=True)
    mac_address = Column(String(50), nullable=False, unique=True, index=True)
    hostname = Column(String(100), nullable=True)
    friendly_name = Column(String(100), nullable=True)
    vendor = Column(String(100), nullable=True)
    operating_system = Column(String(100), nullable=True)
    connection_type = Column(String(50), default="Ethernet", nullable=False)  # Ethernet, Wi-Fi
    last_seen = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    signal_strength = Column(Integer, nullable=True)  # dBm or percentage
    is_online = Column(Boolean, default=True, nullable=False)

    history = relationship("NetworkHistory", back_populates="device", cascade="all, delete-orphan")


class NetworkInterface(Base):
    __tablename__ = "network_interfaces"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(50), nullable=False, unique=True)
    mac_address = Column(String(50), nullable=True)
    ip_address = Column(String(50), nullable=True)
    status = Column(String(20), default="UP", nullable=False)
    speed_mbps = Column(Integer, default=1000, nullable=False)


class NetworkHistory(Base):
    __tablename__ = "network_history"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    device_id = Column(String(36), ForeignKey("network_devices.id", ondelete="CASCADE"), nullable=False)
    latency_ms = Column(Float, default=1.5, nullable=False)
    packet_loss_pct = Column(Float, default=0.0, nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    device = relationship("NetworkDevice", back_populates="history")


class DeviceAlias(Base):
    __tablename__ = "device_aliases"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    mac_address = Column(String(50), nullable=False, unique=True)
    friendly_name = Column(String(100), nullable=False)


class NetworkEvent(Base):
    __tablename__ = "network_events"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    event_type = Column(String(100), nullable=False)  # device.online, device.offline, alert, mac.changed
    device_id = Column(String(36), nullable=True)
    message = Column(String(500), nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
