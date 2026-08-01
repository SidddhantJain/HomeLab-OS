"""
HomeLab Manager — Desktop Server Discovery Engine
"""

from typing import List, Dict, Any


class DesktopServerDiscovery:
    """Discovers local and remote HomeLab OS instances for HomeLab Manager."""

    def discover_instances(self) -> List[Dict[str, Any]]:
        return [
            {
                "server_id": "srv-local-01",
                "name": "Local HomeLab Server",
                "host": "127.0.0.1",
                "port": 8000,
                "version": "1.0.0",
                "status": "ONLINE"
            },
            {
                "server_id": "srv-remote-nas",
                "name": "Storage NAS HomeLab",
                "host": "192.168.1.150",
                "port": 8000,
                "version": "1.0.0",
                "status": "ONLINE"
            }
        ]
