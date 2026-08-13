import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Boolean, Integer, Float, JSON
from app.core.database import Base


class ClusterNode(Base):
    """Represents a paired physical or virtual server node within the HomeLab OS super-cluster."""
    __tablename__ = "cluster_nodes"
    __table_args__ = {'extend_existing': True}

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    node_name = Column(String(100), nullable=False, unique=True)
    hostname = Column(String(100), nullable=False)
    ip_address = Column(String(45), nullable=False)
    mac_address = Column(String(17), nullable=True)
    role = Column(String(20), default="WORKER", nullable=False)  # PRIMARY, SECONDARY, WORKER
    status = Column(String(20), default="ONLINE", nullable=False)  # ONLINE, OFFLINE, DEGRADED, PAIRING
    
    cpu_cores = Column(Integer, default=4, nullable=False)
    ram_total_mb = Column(Integer, default=8192, nullable=False)
    storage_total_gb = Column(Float, default=500.0, nullable=False)
    
    mtls_token = Column(String(255), nullable=True)
    cluster_group = Column(String(50), default="Default", nullable=False)
    joined_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    last_heartbeat = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


class NodePairingRequest(Base):
    """Manages pairing handshakes and token validation for 1-click server mergers."""
    __tablename__ = "node_pairing_requests"
    __table_args__ = {'extend_existing': True}

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    pairing_token = Column(String(64), unique=True, nullable=False)
    source_ip = Column(String(45), nullable=False)
    target_node_name = Column(String(100), nullable=False)
    status = Column(String(20), default="PENDING", nullable=False)  # PENDING, APPROVED, REJECTED, EXPIRED
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    expires_at = Column(DateTime, nullable=False)


class NodeHeartbeat(Base):
    """Records real-time telemetry metrics and latency samples for cluster node monitoring."""
    __tablename__ = "node_heartbeats"
    __table_args__ = {'extend_existing': True}

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    node_id = Column(String(36), nullable=False)
    cpu_usage_pct = Column(Float, default=0.0, nullable=False)
    ram_usage_pct = Column(Float, default=0.0, nullable=False)
    disk_usage_pct = Column(Float, default=0.0, nullable=False)
    ping_latency_ms = Column(Float, default=1.0, nullable=False)
    active_containers_count = Column(Integer, default=0, nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


class ClusterGroup(Base):
    """Logical grouping for cluster server nodes (e.g., Storage Nodes, GPU Transcode Nodes)."""
    __tablename__ = "cluster_groups"
    __table_args__ = {'extend_existing': True}

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(255), nullable=True)
    tags = Column(JSON, default=list, nullable=False)

