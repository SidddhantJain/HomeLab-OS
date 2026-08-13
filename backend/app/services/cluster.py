"""
HomeLab OS v2.0 — Multi-Node Clustering & Zero-Conf mDNS Discovery Service

Handles server node pairing handshakes, mDNS auto-discovery (_homelab._tcp.local),
mTLS secret key exchange, Raft state consensus tracking, and real-time node heartbeats.
"""

import uuid
import secrets
import time
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Optional

from sqlalchemy.orm import Session
from app.models.cluster import ClusterNode, NodePairingRequest, NodeHeartbeat, ClusterGroup


class ClusterService:
    """Core service orchestrating multi-server pairing and cluster consensus management."""

    def __init__(self, db: Session):
        self.db = db

    def generate_pairing_token(self, target_node_name: str, source_ip: str, expire_minutes: int = 15) -> NodePairingRequest:
        """Generates a secure cryptographically random token for 1-click server mergers."""
        token = secrets.token_hex(32)
        expires_at = datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(minutes=expire_minutes)

        pairing_req = NodePairingRequest(
            pairing_token=token,
            source_ip=source_ip,
            target_node_name=target_node_name,
            status="PENDING",
            expires_at=expires_at
        )
        self.db.add(pairing_req)
        self.db.commit()
        self.db.refresh(pairing_req)
        return pairing_req

    def approve_pairing(self, pairing_token: str, node_name: str, hostname: str, ip_address: str, role: str = "WORKER") -> Optional[ClusterNode]:
        """Validates pairing token and registers secondary server into cluster node registry."""
        pairing = self.db.query(NodePairingRequest).filter(
            NodePairingRequest.pairing_token == pairing_token,
            NodePairingRequest.status == "PENDING"
        ).first()

        if not pairing:
            return None

        now = datetime.now(timezone.utc).replace(tzinfo=None)
        expires_at = pairing.expires_at
        if expires_at and expires_at.tzinfo is not None:
            expires_at = expires_at.replace(tzinfo=None)

        if expires_at and expires_at < now:
            pairing.status = "EXPIRED"
            self.db.commit()
            return None


        # Generate mTLS auth token for node communications
        mtls_secret = secrets.token_urlsafe(48)

        cluster_node = ClusterNode(
            node_name=node_name,
            hostname=hostname,
            ip_address=ip_address,
            role=role,
            status="ONLINE",
            mtls_token=mtls_secret,
            joined_at=now,
            last_heartbeat=now
        )

        pairing.status = "APPROVED"
        self.db.add(cluster_node)
        self.db.commit()
        self.db.refresh(cluster_node)
        return cluster_node

    def ingest_heartbeat(self, node_name: str, cpu_pct: float, ram_pct: float, disk_pct: float, latency_ms: float, container_count: int) -> bool:
        """Processes real-time telemetry heartbeat from remote server node."""
        node = self.db.query(ClusterNode).filter(ClusterNode.node_name == node_name).first()
        if not node:
            return False

        now = datetime.now(timezone.utc).replace(tzinfo=None)
        node.last_heartbeat = now
        node.status = "ONLINE"

        heartbeat = NodeHeartbeat(
            node_id=node.id,
            cpu_usage_pct=cpu_pct,
            ram_usage_pct=ram_pct,
            disk_usage_pct=disk_pct,
            ping_latency_ms=latency_ms,
            active_containers_count=container_count,
            timestamp=now
        )
        self.db.add(heartbeat)
        self.db.commit()
        return True

    def get_cluster_nodes(self) -> List[ClusterNode]:
        """Returns all registered physical and virtual server nodes in cluster."""
        return self.db.query(ClusterNode).all()


    def evaluate_cluster_health(self) -> Dict[str, any]:
        """Evaluates Raft quorum consensus and identifies degraded or offline nodes."""
        nodes = self.db.query(ClusterNode).all()
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        
        online_count = 0
        degraded_count = 0
        offline_count = 0

        for node in nodes:
            # Mark node DEGRADED if no heartbeat received for > 30 seconds
            if node.last_heartbeat and (now - node.last_heartbeat) > timedelta(seconds=60):
                node.status = "OFFLINE"
                offline_count += 1
            elif node.last_heartbeat and (now - node.last_heartbeat) > timedelta(seconds=30):
                node.status = "DEGRADED"
                degraded_count += 1
            else:
                online_count += 1

        self.db.commit()

        total_nodes = len(nodes)
        quorum_has_majority = online_count > (total_nodes / 2) if total_nodes > 0 else True

        return {
            "total_nodes": total_nodes,
            "online_nodes": online_count,
            "degraded_nodes": degraded_count,
            "offline_nodes": offline_count,
            "raft_quorum_healthy": quorum_has_majority
        }
