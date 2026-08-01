"""
HomeLab OS — Docker Application Catalog Service
"""

from __future__ import annotations

from typing import Any, Dict, List
from sqlalchemy.orm import Session
from app.core.base_service import BaseService
from app.models.catalog import AppCatalogItem


class CatalogService(BaseService):
    """Provides application catalog templates for self-hosted Docker workloads."""

    DEFAULT_TEMPLATES = [
        {"template_id": "immich", "name": "Immich", "category": "Photos & Media", "icon_url": "/icons/immich.svg", "description": "High performance self-hosted photo and video backup solution.", "default_ports": ["2283:2283"]},
        {"template_id": "jellyfin", "name": "Jellyfin", "category": "Photos & Media", "icon_url": "/icons/jellyfin.svg", "description": "The Free Software Media System.", "default_ports": ["8096:8096"]},
        {"template_id": "nextcloud", "name": "Nextcloud", "category": "Productivity", "icon_url": "/icons/nextcloud.svg", "description": "A safe home for all your data.", "default_ports": ["8080:80"]},
        {"template_id": "vaultwarden", "name": "Vaultwarden", "category": "Security", "icon_url": "/icons/vaultwarden.svg", "description": "Unofficial Bitwarden compatible server in Rust.", "default_ports": ["8081:80"]},
        {"template_id": "gitea", "name": "Gitea", "category": "Development", "icon_url": "/icons/gitea.svg", "description": "Git with a cup of tea.", "default_ports": ["3000:3000", "222:22"]},
        {"template_id": "grafana", "name": "Grafana", "category": "Monitoring", "icon_url": "/icons/grafana.svg", "description": "Operational dashboards for your infrastructure.", "default_ports": ["3001:3000"]},
        {"template_id": "prometheus", "name": "Prometheus", "category": "Monitoring", "icon_url": "/icons/prometheus.svg", "description": "Monitoring system and time series database.", "default_ports": ["9090:9090"]},
        {"template_id": "pihole", "name": "Pi-hole", "category": "Networking", "icon_url": "/icons/pihole.svg", "description": "Network-wide Ad Blocking.", "default_ports": ["53:53/udp", "8082:80"]},
        {"template_id": "homeassistant", "name": "Home Assistant", "category": "Automation", "icon_url": "/icons/homeassistant.svg", "description": "Open source home automation that puts local control first.", "default_ports": ["8123:8123"]}
    ]

    @property
    def name(self) -> str:
        return "catalog"

    def initialize(self) -> None:
        pass

    def shutdown(self) -> None:
        pass

    def health(self) -> Dict[str, Any]:
        return {
            "status": "healthy",
            "message": "App Catalog Service is active."
        }

    def list_catalog_templates(self, db: Session) -> List[Dict[str, Any]]:
        # Sync default templates to db if empty
        items = db.query(AppCatalogItem).all()
        if not items:
            for t in self.DEFAULT_TEMPLATES:
                item = AppCatalogItem(
                    template_id=t["template_id"],
                    name=t["name"],
                    category=t["category"],
                    icon_url=t["icon_url"],
                    description=t["description"],
                    default_ports=t["default_ports"]
                )
                db.add(item)
            db.commit()
            items = db.query(AppCatalogItem).all()

        return [
            {
                "template_id": i.template_id,
                "name": i.name,
                "category": i.category,
                "icon_url": i.icon_url,
                "description": i.description,
                "default_ports": i.default_ports
            } for i in items
        ]
