"""
HomeLab OS — Webhook Notification Provider Scaffolding
"""

from typing import Dict, Any


class WebhookNotifier:
    """Dispatches webhook POST payloads when enabled."""

    def __init__(self, enabled: bool = False, webhook_url: str = None) -> None:
        self.enabled = enabled
        self.webhook_url = webhook_url

    def send(self, payload: Dict[str, Any]) -> bool:
        if not self.enabled:
            return False
        print(f"[WebhookNotifier] POST payload to {self.webhook_url}: {payload}")
        return True
