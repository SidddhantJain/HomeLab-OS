"""
HomeLab OS v2.0 — End-to-End (E2E) Full Platform Integration Workflow Test Suite

Tests full multi-node lifecycle:
1. Secondary node pairing request & mTLS token approval.
2. Real-time telemetry heartbeat ingestion & Raft quorum evaluation.
3. Multi-container Compose stack generation (Media Suite).
4. Differential block snapshot sync (zfs/btrfs zstd compressed backup).
5. WireGuard mesh network peer key generation & Cloudflare tunnel binding.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app as fastapi_app
from app.core.homelab_core import HomelabCore
from app.core.database import engine, Base
from app.services.compose_catalog import ComposeCatalogService
from app.services.disaster_recovery import DisasterRecoveryService
from app.services.network_tunnel import NetworkTunnelService

Base.metadata.create_all(bind=engine)


@pytest.fixture
def client():
    HomelabCore.reset()
    with TestClient(fastapi_app) as c:
        yield c


def test_full_v2_e2e_platform_workflow(client):
    """Executes full End-to-End HomeLab OS v2.0 multi-node lifecycle scenario."""
    # ------------------------------------------------------------------
    # Step 1: Pair a new secondary server node into cluster
    # ------------------------------------------------------------------
    req_res = client.post(
        "/api/v1/cluster/pair/request",
        json={"target_node_name": "dell-inspiron-5558-secondary", "source_ip": "192.168.0.181"}
    )
    assert req_res.status_code == 200
    token = req_res.json()["pairing_token"]
    assert token is not None

    approve_res = client.post(
        "/api/v1/cluster/pair/approve",
        json={
            "pairing_token": token,
            "node_name": "dell-inspiron-5558-secondary",
            "hostname": "inspiron-secondary",
            "ip_address": "192.168.0.181",
            "role": "SECONDARY"
        }
    )
    assert approve_res.status_code == 200
    paired_node = approve_res.json()
    assert paired_node["node_name"] == "dell-inspiron-5558-secondary"
    assert "mtls_token" in paired_node

    # ------------------------------------------------------------------
    # Step 2: Ingest telemetry heartbeat & verify Raft quorum health
    # ------------------------------------------------------------------
    hb_res = client.post(
        "/api/v1/cluster/heartbeat",
        json={
            "node_name": "dell-inspiron-5558-secondary",
            "cpu_pct": 24.5,
            "ram_pct": 42.0,
            "disk_pct": 18.2,
            "ping_latency_ms": 1.2,
            "active_containers_count": 8
        }
    )
    assert hb_res.status_code == 200


    health_res = client.get("/api/v1/cluster/health")
    assert health_res.status_code == 200
    health_data = health_res.json()
    assert health_data["total_nodes"] >= 1
    assert health_data["raft_quorum_healthy"] is True

    # ------------------------------------------------------------------
    # Step 3: Deploy 100+ App Marketplace Compose Stack (Media Suite)
    # ------------------------------------------------------------------
    stacks = ComposeCatalogService.get_all_stacks()
    assert len(stacks) >= 3

    compose_yaml = ComposeCatalogService.generate_docker_compose_yaml("media_suite")
    assert "jellyfin" in compose_yaml
    assert "qbittorrent" in compose_yaml

    # ------------------------------------------------------------------
    # Step 4: Perform Differential Block Snapshot Replication
    # ------------------------------------------------------------------
    dr_service = DisasterRecoveryService()
    sync_record = dr_service.trigger_differential_block_sync(
        source_dataset="rpool/homelab/data",
        target_node_ip="192.168.0.181",
        mode="btrfs"
    )
    assert sync_record["status"] == "COMPLETED"
    assert sync_record["target_node_ip"] == "192.168.0.181"

    # ------------------------------------------------------------------
    # Step 5: Setup Cloudflare Tunnel & WireGuard Overlay Mesh Network
    # ------------------------------------------------------------------
    tunnel_service = NetworkTunnelService()
    tunnel = tunnel_service.create_cloudflare_tunnel("e2e-media", "media.homelab.local", "http://localhost:8096")
    assert tunnel["status"] == "ACTIVE"

    peer = tunnel_service.generate_wireguard_peer("android-client-01")
    assert peer["status"] == "CONNECTED"
    assert peer["peer_name"] == "android-client-01"
