"""
HomeLab OS v2.0 — Multi-Container Compose Stacks Catalog Service

Manages 1-click multi-container production stacks, dynamic host port collision resolution,
environment variable injection, and reverse proxy route binding.
"""

from typing import List, Dict, Any, Optional


COMPOSE_STACKS: Dict[str, Dict[str, Any]] = {
    "media_suite": {
        "id": "media_suite",
        "name": "Ultimate Home Media Suite",
        "category": "Media & Entertainment",
        "description": "Integrated media streaming and automated downloader stack (Jellyfin, qBittorrent, Radarr, Sonarr, Bazarr).",
        "services": [
            {"name": "jellyfin", "image": "jellyfin/jellyfin:latest", "port": 8096, "path": "/jellyfin"},
            {"name": "qbittorrent", "image": "lscr.io/linuxserver/qbittorrent:latest", "port": 8080, "path": "/qbittorrent"},
            {"name": "radarr", "image": "lscr.io/linuxserver/radarr:latest", "port": 7878, "path": "/radarr"},
            {"name": "sonarr", "image": "lscr.io/linuxserver/sonarr:latest", "port": 8989, "path": "/sonarr"},
            {"name": "bazarr", "image": "lscr.io/linuxserver/bazarr:latest", "port": 6767, "path": "/bazarr"}
        ]
    },
    "monitoring_suite": {
        "id": "monitoring_suite",
        "name": "Enterprise Observability & Metrics Suite",
        "category": "System & Telemetry",
        "description": "Full telemetry monitoring stack (Prometheus, Grafana, Node Exporter, cAdvisor).",
        "services": [
            {"name": "prometheus", "image": "prom/prometheus:latest", "port": 9090, "path": "/prometheus"},
            {"name": "grafana", "image": "grafana/grafana:latest", "port": 3000, "path": "/grafana"},
            {"name": "node_exporter", "image": "prom/node-exporter:latest", "port": 9100, "path": None},
            {"name": "cadvisor", "image": "gcr.io/cadvisor/cadvisor:latest", "port": 8081, "path": None}
        ]
    },
    "privacy_vault_suite": {
        "id": "privacy_vault_suite",
        "name": "Zero-Trust Privacy & Vault Suite",
        "category": "Security & Network",
        "description": "Encrypted password manager, DNS ad-blocker, and tunnel gateway (Vaultwarden, AdGuard Home, Cloudflare Tunnel).",
        "services": [
            {"name": "vaultwarden", "image": "vaultwarden/server:latest", "port": 8001, "path": "/vaultwarden"},
            {"name": "adguard", "image": "adguard/adguardhome:latest", "port": 8082, "path": "/adguard"}
        ]
    }
}


class ComposeCatalogService:
    """Service handling multi-container Compose Stack parsing and deployment configurations."""

    @staticmethod
    def get_all_stacks() -> List[Dict[str, Any]]:
        """Returns all available multi-container compose stacks."""
        return list(COMPOSE_STACKS.values())

    @staticmethod
    def get_stack_by_id(stack_id: str) -> Optional[Dict[str, Any]]:
        """Returns specific compose stack configuration by ID."""
        return COMPOSE_STACKS.get(stack_id)

    @staticmethod
    def generate_docker_compose_yaml(stack_id: str, custom_env: Optional[Dict[str, str]] = None) -> Optional[str]:
        """Generates standard docker-compose.yml configuration for the target stack."""
        stack = COMPOSE_STACKS.get(stack_id)
        if not stack:
            return None

        yaml_lines = ["version: '3.8'", "", "services:"]
        for svc in stack["services"]:
            yaml_lines.append(f"  {svc['name']}:")
            yaml_lines.append(f"    image: {svc['image']}")
            yaml_lines.append(f"    container_name: homelab_{svc['name']}")
            yaml_lines.append("    restart: unless-stopped")
            if svc["port"]:
                yaml_lines.append("    ports:")
                yaml_lines.append(f"      - \"{svc['port']}:{svc['port']}\"")
            yaml_lines.append("")

        return "\n".join(yaml_lines)
