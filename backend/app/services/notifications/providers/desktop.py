"""
HomeLab OS — Desktop / Browser Notification Provider Scaffolding
"""

from typing import Dict, Any


class DesktopNotifier:
    """Triggers system desktop or browser alerts."""

    def __init__(self, enabled: bool = True) -> None:
        self.enabled = enabled

    def send(self, title: str, message: str) -> bool:
        if not self.enabled:
            return False
        print(f"[DesktopNotifier] Display alert '{title}': {message}")
        return True
