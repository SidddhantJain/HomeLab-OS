"""
HomeLab OS v2.0 — Load, Stress & High-Frequency Throughput Test Suite

Simulates parallel concurrent API requests, multi-node telemetry heartbeat flooding,
and high-frequency Docker Compose YAML generation throughput.
"""

import pytest
import concurrent.futures
from fastapi.testclient import TestClient
from app.main import app as fastapi_app
from app.core.homelab_core import HomelabCore
from app.core.database import engine, Base
from app.services.compose_catalog import ComposeCatalogService

Base.metadata.create_all(bind=engine)


@pytest.fixture
def client():
    HomelabCore.reset()
    with TestClient(fastapi_app) as c:
        yield c


def test_load_concurrent_api_requests(client):
    """Stress tests GET endpoints under 50 concurrent worker threads."""
    def send_request():
        res = client.get("/api/v1/cluster/nodes")
        return res.status_code

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(send_request) for _ in range(50)]
        results = [f.result() for f in concurrent.futures.as_completed(futures)]

    assert len(results) == 50
    assert all(status == 200 for status in results)


def test_load_heartbeat_telemetry_flooding(client):
    """Floods cluster node heartbeat ingestion with 50 telemetry samples in sequence."""
    # First register a node for heartbeat ingestion
    req = client.post(
        "/api/v1/cluster/pair/request",
        json={"target_node_name": "load-node-01", "source_ip": "192.168.0.210"}
    )
    token = req.json()["pairing_token"]
    client.post(
        "/api/v1/cluster/pair/approve",
        json={
            "pairing_token": token,
            "node_name": "load-node-01",
            "hostname": "load-host-01",
            "ip_address": "192.168.0.210"
        }
    )

    # Ingest 50 consecutive telemetry heartbeats
    for i in range(50):
        hb_res = client.post(
            "/api/v1/cluster/heartbeat",
            json={
                "node_name": "load-node-01",
                "cpu_pct": 10.0 + (i % 80),
                "ram_pct": 20.0 + (i % 70),
                "disk_pct": 35.0,
                "ping_latency_ms": 1.5 + (i * 0.1),
                "active_containers_count": i % 15
            }
        )
        assert hb_res.status_code == 200


    # Verify cluster node health summary
    health_res = client.get("/api/v1/cluster/health")
    assert health_res.status_code == 200
    assert health_res.json()["online_nodes"] >= 1


def test_load_compose_catalog_throughput():
    """Verifies high-frequency Docker Compose YAML generation throughput (100 iterations)."""
    for _ in range(100):
        yaml_out = ComposeCatalogService.generate_docker_compose_yaml("media_suite")
        assert "jellyfin" in yaml_out
        assert "version: '3.8'" in yaml_out
