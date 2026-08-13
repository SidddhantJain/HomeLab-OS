"""
HomeLab OS v2.0 — Multi-Node Cluster REST API & Compose Stacks Test Suite
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app as fastapi_app
from app.services.compose_catalog import ComposeCatalogService
from app.services.network_tunnel import NetworkTunnelService
from app.core.homelab_core import HomelabCore
from app.core.database import engine, Base
import app.models  # Ensures all models are registered

Base.metadata.create_all(bind=engine)



@pytest.fixture
def client():
    HomelabCore.reset()
    with TestClient(fastapi_app) as c:
        yield c



def test_cluster_nodes_endpoint(client):
    """Tests GET /api/v1/cluster/nodes endpoint."""
    res = client.get("/api/v1/cluster/nodes")
    assert res.status_code == 200
    assert isinstance(res.json(), list)


def test_cluster_health_endpoint(client):
    """Tests GET /api/v1/cluster/health endpoint."""
    res = client.get("/api/v1/cluster/health")
    assert res.status_code == 200
    data = res.json()
    assert "total_nodes" in data
    assert "raft_quorum_healthy" in data


def test_cluster_pairing_handshake(client):
    """Tests server pairing request and approval lifecycle."""
    # 1. Request pairing token
    req_res = client.post(
        "/api/v1/cluster/pair/request",
        json={"target_node_name": "inspiron-5558-sec", "source_ip": "192.168.0.181"}
    )
    assert req_res.status_code == 200
    token_data = req_res.json()
    token = token_data["pairing_token"]
    assert token is not None

    # 2. Approve pairing token
    approve_res = client.post(
        "/api/v1/cluster/pair/approve",
        json={
            "pairing_token": token,
            "node_name": "inspiron-5558-sec",
            "hostname": "inspiron-secondary",
            "ip_address": "192.168.0.181",
            "role": "SECONDARY"
        }
    )
    assert approve_res.status_code == 200
    approved_data = approve_res.json()
    assert approved_data["node_name"] == "inspiron-5558-sec"
    assert "mtls_token" in approved_data


def test_compose_catalog_stacks():
    """Tests ComposeCatalogService stack generation."""
    stacks = ComposeCatalogService.get_all_stacks()
    assert len(stacks) >= 3

    media_stack = ComposeCatalogService.get_stack_by_id("media_suite")
    assert media_stack is not None
    assert media_stack["name"] == "Ultimate Home Media Suite"

    yaml_out = ComposeCatalogService.generate_docker_compose_yaml("media_suite")
    assert "jellyfin" in yaml_out
    assert "qbittorrent" in yaml_out


def test_network_tunnel_service():
    """Tests Cloudflare Tunnels and WireGuard Mesh creation."""
    service = NetworkTunnelService()
    tunnel = service.create_cloudflare_tunnel("media-tunnel", "media.homelab.local", "http://localhost:8096")
    assert tunnel["tunnel_name"] == "media-tunnel"
    assert tunnel["status"] == "ACTIVE"

    peer = service.generate_wireguard_peer("mobile-client")
    assert peer["peer_name"] == "mobile-client"
    assert peer["status"] == "CONNECTED"
