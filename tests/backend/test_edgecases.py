"""
HomeLab OS v2.0 — Edge Case Quality & Resilience Test Suite

Tests edge cases including expired tokens, corrupted payloads, duplicate node registrations,
missing required fields, zero resource capacity, and non-existent compose stack IDs.
"""

import pytest
from datetime import datetime, timezone, timedelta
from fastapi.testclient import TestClient
from app.main import app as fastapi_app
from app.core.homelab_core import HomelabCore
from app.core.database import engine, Base, SessionLocal
from app.models.cluster import NodePairingRequest, ClusterNode
from app.services.compose_catalog import ComposeCatalogService
from app.services.network_tunnel import NetworkTunnelService

Base.metadata.create_all(bind=engine)


@pytest.fixture
def client():
    HomelabCore.reset()
    with TestClient(fastapi_app) as c:
        yield c


def test_edgecase_expired_pairing_token(client):
    """Verifies that an expired pairing token cannot be approved."""
    db = SessionLocal()
    try:
        expired_req = NodePairingRequest(
            pairing_token="expired_token_1234567890abcdef1234567890abcdef",
            source_ip="192.168.0.200",
            target_node_name="node-expired",
            status="PENDING",
            expires_at=datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(minutes=10)
        )
        db.add(expired_req)
        db.commit()
    finally:
        db.close()

    approve_res = client.post(
        "/api/v1/cluster/pair/approve",
        json={
            "pairing_token": "expired_token_1234567890abcdef1234567890abcdef",
            "node_name": "node-expired",
            "hostname": "expired-host",
            "ip_address": "192.168.0.200"
        }
    )
    assert approve_res.status_code == 400
    assert "Invalid or expired" in approve_res.json()["detail"]


def test_edgecase_invalid_pairing_token(client):
    """Verifies response when non-existent pairing token is provided."""
    res = client.post(
        "/api/v1/cluster/pair/approve",
        json={
            "pairing_token": "non_existent_token_xyz999",
            "node_name": "ghost-node",
            "hostname": "ghost",
            "ip_address": "10.0.0.99"
        }
    )
    assert res.status_code == 400


def test_edgecase_duplicate_node_pairing(client):
    """Verifies that duplicate server pairing requests are handled gracefully."""
    req1 = client.post(
        "/api/v1/cluster/pair/request",
        json={"target_node_name": "node-unique-1", "source_ip": "192.168.0.150"}
    )
    assert req1.status_code == 200
    token1 = req1.json()["pairing_token"]

    app1 = client.post(
        "/api/v1/cluster/pair/approve",
        json={
            "pairing_token": token1,
            "node_name": "node-unique-1",
            "hostname": "host-unique-1",
            "ip_address": "192.168.0.150"
        }
    )
    assert app1.status_code == 200

    # Attempting to reuse same approved token should fail
    app2 = client.post(
        "/api/v1/cluster/pair/approve",
        json={
            "pairing_token": token1,
            "node_name": "node-unique-1",
            "hostname": "host-unique-1",
            "ip_address": "192.168.0.150"
        }
    )
    assert app2.status_code == 400


def test_edgecase_nonexistent_compose_stack():
    """Verifies ComposeCatalogService handles non-existent stack lookup safely."""
    stack = ComposeCatalogService.get_stack_by_id("non_existent_stack_999")
    assert stack is None

    yaml_out = ComposeCatalogService.generate_docker_compose_yaml("non_existent_stack_999")
    assert yaml_out is None or yaml_out == ""


def test_edgecase_heartbeat_unknown_node(client):
    """Verifies heartbeat endpoint handles heartbeats from unregistered server nodes."""
    res = client.post(
        "/api/v1/cluster/heartbeat",
        json={
            "node_name": "unregistered-ghost-node-99",
            "cpu_pct": 50.0,
            "ram_pct": 50.0,
            "disk_pct": 50.0,
            "ping_latency_ms": 5.0,
            "active_containers_count": 0
        }
    )
    assert res.status_code == 404

