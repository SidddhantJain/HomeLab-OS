"""
HomeLab OS — Platform Event Subscribers

Wires central subscribers to the Event Bus to handle audit logging,
telemetry updates, and status notifications.
"""

from __future__ import annotations

from datetime import datetime, timezone
from app.core.event_bus import Event
from app.core.database import SessionLocal
from app.models.audit import AuditLog
from app.core.telemetry import TelemetryCollector


def wire_event_subscribers(event_bus: object, telemetry: TelemetryCollector) -> None:
    """Register all system-wide pub/sub event listeners."""

    # 1. Audit Logger Subscriber
    def audit_logger_handler(event: Event) -> None:
        action_map = {
            "vault.unlocked": "USER_UNLOCK_VAULT",
            "vault.locked": "USER_LOCK_VAULT",
            "storage.mounted": "STORAGE_MOUNT",
            "storage.unmounted": "STORAGE_UNMOUNT",
            "storage.health_warning": "HEALTH_WARNING"
        }

        action = action_map.get(event.name)
        if not action:
            return

        db = SessionLocal()
        try:
            log_entry = AuditLog(
                action=action,
                user=event.payload.get("user", "system"),
                metadata_json=event.payload
            )
            db.add(log_entry)
            db.commit()
        except Exception as exc:  # noqa: BLE001
            print(f"[EventSubscribers] Audit log failed: {exc}")
        finally:
            db.close()

    # 2. Telemetry Metrics Subscriber
    def telemetry_metrics_handler(event: Event) -> None:
        if event.name == "storage.mounted":
            telemetry.record_metric("storage.mount_status", 1.0, tags={"device": event.payload.get("device_name", "unknown")})
        elif event.name == "storage.unmounted":
            telemetry.record_metric("storage.mount_status", 0.0, tags={"device": event.payload.get("device_name", "unknown")})
        elif event.name == "vault.unlocked":
            telemetry.record_metric("vault.lock_status", 1.0)
        elif event.name == "vault.locked":
            telemetry.record_metric("vault.lock_status", 0.0)
        elif event.name == "vault.failed_unlock":
            telemetry.record_metric("vault.unlock_failures", 1.0)

    # Register handlers
    event_bus.subscribe("vault.*", audit_logger_handler)
    event_bus.subscribe("storage.*", audit_logger_handler)
    event_bus.subscribe("vault.*", telemetry_metrics_handler)
    event_bus.subscribe("storage.*", telemetry_metrics_handler)
