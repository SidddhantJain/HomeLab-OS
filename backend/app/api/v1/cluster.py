"""
HomeLab OS v2.0 — Multi-Node Clustering REST API Endpoints

Provides API routes for 1-click server pairing, node management, Raft consensus checks,
and remote telemetry heartbeat ingestion.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.cluster import ClusterService

router = APIRouter(prefix="/cluster", tags=["Multi-Node Cluster"])


class PairingRequestPayload(BaseModel):
    target_node_name: str
    source_ip: str


class PairingApprovePayload(BaseModel):
    pairing_token: str
    node_name: str
    hostname: str
    ip_address: str
    role: Optional[str] = "WORKER"


class HeartbeatPayload(BaseModel):
    node_name: str
    cpu_pct: float
    ram_pct: float
    disk_pct: float
    ping_latency_ms: float
    active_containers_count: int


@router.get("/nodes")
def list_cluster_nodes(db: Session = Depends(get_db)):
    """Returns all registered physical and virtual server nodes in cluster."""
    service = ClusterService(db)
    nodes = service.get_cluster_nodes()
    return [{"id": n.id, "node_name": n.node_name, "hostname": n.hostname, "ip_address": n.ip_address, "role": n.role, "status": n.status, "ram_total_mb": n.ram_total_mb} for n in nodes]


@router.get("/health")
def get_cluster_health(db: Session = Depends(get_db)):
    """Returns Raft quorum health consensus metrics across all cluster nodes."""
    service = ClusterService(db)
    return service.evaluate_cluster_health()


@router.post("/pair/request")
def request_server_pairing(payload: PairingRequestPayload, db: Session = Depends(get_db)):
    """Generates a secure 15-minute pairing token for merging physical servers."""
    service = ClusterService(db)
    req = service.generate_pairing_token(payload.target_node_name, payload.source_ip)
    return {
        "pairing_token": req.pairing_token,
        "status": req.status,
        "expires_at": req.expires_at.isoformat()
    }


@router.post("/pair/approve")
def approve_server_pairing(payload: PairingApprovePayload, db: Session = Depends(get_db)):
    """Approves server pairing token and joins new physical node into cluster pool."""
    service = ClusterService(db)
    node = service.approve_pairing(
        pairing_token=payload.pairing_token,
        node_name=payload.node_name,
        hostname=payload.hostname,
        ip_address=payload.ip_address,
        role=payload.role
    )
    if not node:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired pairing token"
        )
    return {
        "message": "Node successfully paired into super-server cluster",
        "node_id": node.id,
        "node_name": node.node_name,
        "mtls_token": node.mtls_token
    }


@router.post("/heartbeat")
def record_node_heartbeat(payload: HeartbeatPayload, db: Session = Depends(get_db)):
    """Ingests periodic telemetry heartbeat from a paired cluster node."""
    service = ClusterService(db)
    success = service.ingest_heartbeat(
        node_name=payload.node_name,
        cpu_pct=payload.cpu_pct,
        ram_pct=payload.ram_pct,
        disk_pct=payload.disk_pct,
        latency_ms=payload.ping_latency_ms,
        container_count=payload.active_containers_count
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_44_NOT_FOUND if hasattr(status, 'HTTP_44_NOT_FOUND') else 404,
            detail="Node not registered in cluster"
        )
    return {"status": "heartbeat_acknowledged"}
