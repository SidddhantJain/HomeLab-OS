"""
HomeLab OS — Emergency Network Recovery & Hotspot System
"""

from typing import Dict, Any


class EmergencyHotspotManager:
    """Manages emergency AP hotspot failover when primary Wi-Fi/WAN connection drops."""

    def __init__(self) -> None:
        self.hotspot_active = False
        self.ssid = "HomeLab-Emergency-Recovery"
        self.password = "homelab-recovery-pass"

    def handle_connectivity_change(self, is_primary_connected: bool) -> Dict[str, Any]:
        if not is_primary_connected and not self.hotspot_active:
            self.hotspot_active = True
            print(f"[EmergencyHotspot] Primary connection lost! Enabling recovery AP '{self.ssid}'")
            return {
                "status": "HOTSPOT_ENABLED",
                "ssid": self.ssid,
                "message": "Emergency recovery Wi-Fi hotspot active."
            }
        elif is_primary_connected and self.hotspot_active:
            self.hotspot_active = False
            print("[EmergencyHotspot] Primary connection restored. Disabling recovery AP.")
            return {
                "status": "HOTSPOT_DISABLED",
                "message": "Recovery hotspot disabled."
            }

        return {
            "status": "HOTSPOT_ACTIVE" if self.hotspot_active else "NORMAL",
            "ssid": self.ssid if self.hotspot_active else None
        }
