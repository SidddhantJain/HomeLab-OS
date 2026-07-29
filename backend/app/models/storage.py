import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Integer, Float, Boolean, ForeignKey
from app.core.database import Base


class StorageDevice(Base):
    __tablename__ = "storage_devices"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    device_name = Column(String(100), nullable=False)
    uuid = Column(String(100), unique=True, nullable=True)
    filesystem = Column(String(50), nullable=True)
    capacity = Column(Float, nullable=False)  # in GB
    device_type = Column(String(50), nullable=False)  # SSD, HDD, USB, etc.
    status = Column(String(50), default="active", nullable=False)  # active, degraded, offline
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


class StoragePartition(Base):
    __tablename__ = "storage_partitions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    device_id = Column(String(36), ForeignKey("storage_devices.id", ondelete="CASCADE"), nullable=False)
    partition_name = Column(String(100), nullable=False)
    uuid = Column(String(100), unique=True, nullable=True)
    filesystem = Column(String(50), nullable=True)
    capacity = Column(Float, nullable=False)  # in GB
    mount_point = Column(String(255), nullable=True)
    used_space = Column(Float, default=0.0, nullable=False)  # in GB
    free_space = Column(Float, default=0.0, nullable=False)  # in GB
    status = Column(String(50), default="active", nullable=False)


class StorageMount(Base):
    __tablename__ = "storage_mounts"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    device_id = Column(String(36), ForeignKey("storage_devices.id", ondelete="CASCADE"), nullable=False)
    mount_point = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    mount_options = Column(String(255), default="defaults", nullable=False)
    mounted_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


class StorageHealthRecord(Base):
    __tablename__ = "storage_health_records"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    device_id = Column(String(36), ForeignKey("storage_devices.id", ondelete="CASCADE"), nullable=False)
    smart_status = Column(String(50), nullable=False)  # PASSED, FAILED, UNKNOWN
    temperature_c = Column(Integer, nullable=True)
    bad_sectors = Column(Integer, default=0, nullable=False)
    read_error_rate = Column(Float, nullable=True)
    write_error_rate = Column(Float, nullable=True)
    power_on_hours = Column(Integer, nullable=True)
    recorded_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
