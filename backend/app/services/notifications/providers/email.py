"""
HomeLab OS — Email Notification Provider Scaffolding
"""

from typing import Dict, Any


class EmailNotifier:
    """Dispatches email notifications when enabled in config."""

    def __init__(self, enabled: bool = False) -> None:
        self.enabled = enabled

    def send(self, subject: str, message: str, recipient: str = None) -> bool:
        if not self.enabled:
            return False
        # Dispatches email via SMTP client
        print(f"[EmailNotifier] Sent email '{subject}' to {recipient or 'admin'}")
        return True
