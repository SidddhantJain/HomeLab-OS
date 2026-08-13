"""
HomeLab OS — Multi-Node Clustering Database Models Test Suite
Validates ClusterNode, NodePairingRequest, NodeHeartbeat, and ClusterGroup models.
"""

import pytest
from datetime import datetime, timezone, timedelta
from app.core.database import SessionLocal, engine, Base
from app.models.cluster import ClusterNode, NodePairingRequest, NodeHeartbeat, ClusterGroup


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_cluster_node_creation(setup_db):
    db = setup_db
    node = ClusterNode(
        node_name="inspiron-5558-primary",
        hostname="inspiron-5558",
        ip_address="192.168.0.180",
        mac_address="00:11:22:33:44:55",
        role="PRIMARY",
        status="ONLINE",
        cpu_cores=4,
        ram_total_mb=8192,
        storage_total_gb=500.0,
        cluster_group="Core Cluster"
    )
    db.add(node)
    db.commit()
    db.refresh(node)

    assert node.id is not None
    assert node.node_name == "inspiron-5558-primary"
    assert node.role == "PRIMARY"
    assert node.status == "ONLINE"
    assert node.ram_total_mb == 8192


def test_node_pairing_request_expiration(setup_db):
    db = setup_db
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    expires = now + timedelta(minutes=15)
    
    pairing = NodePairingRequest(
        pairing_token="sec_token_1234567890abcdef",
        source_ip="192.168.0.181",
        target_node_name="rpi4-node-02",
        status="PENDING",
        expires_at=expires
    )
    db.add(pairing)
    db.commit()
    db.refresh(pairing)

    assert pairing.pairing_token == "sec_token_1234567890abcdef"
    assert pairing.status == "PENDING"
    assert pairing.expires_at >= now



def test_node_heartbeat_telemetry(setup_db):
    db = setup_db
    hb = NodeHeartbeat(
        node_id="node_uuid_123",
        cpu_usage_pct=24.5,
        ram_usage_pct=42.1,
        disk_usage_pct=65.0,
        ping_latency_ms=1.2,
        active_containers_count=12
    )
    db.add(hb)
    db.commit()
    db.refresh(hb)

    assert hb.cpu_usage_pct == 24.5
    assert hb.active_containers_count == 12


def test_cluster_group_tagging(setup_db):
    db = setup_db
    group = ClusterGroup(
        name="Media Nodes",
        description="High GPU transcode capability server nodes",
        tags=["gpu", "quicksync", "jellyfin"]
    )
    db.add(group)
    db.commit()
    db.refresh(group)

    assert group.name == "Media Nodes"
    assert "quicksync" in group.tags
