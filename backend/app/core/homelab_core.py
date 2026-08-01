"""
HomeLab OS — Core Platform Coordinator

The HomeLab Core is the central orchestrator that initialises, registers,
and manages every platform service.  All services communicate through the
Core's Event Bus rather than referencing each other directly.

Responsibilities:
    • Maintain a registry of all platform services.
    • Own the global Event Bus and Server State Machine instances.
    • Coordinate startup and shutdown sequences.
    • Expose health and telemetry aggregation points.

Architecture:

    HomeLab Core
        ├── Event Bus
        ├── Server State Machine
        ├── Service Registry
        │     ├── Authentication Service
        │     ├── Storage Service
        │     ├── Vault Service
        │     ├── Project Service
        │     ├── Workspace Manager
        │     ├── Update Service
        │     ├── Scheduler Service
        │     ├── Notification Service
        │     ├── Monitoring Service
        │     ├── Automation Service
        │     ├── Hardware Service
        │     └── Plugin Manager
        ├── Telemetry Collector
        └── Configuration Manager
"""

from __future__ import annotations

from typing import Optional

from app.core.event_bus import EventBus, Event
from app.core.server_state import ServerState, ServerStateMachine
from app.core.telemetry import TelemetryCollector
from app.core.scheduler import Scheduler, ScheduleMode


class HomelabCore:
    """Singleton coordinator for the HomeLab OS platform.

    Usage:
        core = HomelabCore.instance()
        core.event_bus.publish(Event(name="system.ready", source="core"))
    """

    _instance: Optional["HomelabCore"] = None

    def __init__(self) -> None:
        self.event_bus = EventBus()
        self.state_machine = ServerStateMachine(initial=ServerState.BOOTING)
        self.telemetry = TelemetryCollector()
        self.scheduler = Scheduler()
        self._services: dict[str, object] = {}

        # Wire state transitions into the event bus automatically.
        self.state_machine.on_change(self._on_state_change)

        # Register default services
        self._register_default_services()

        # Wire event subscribers
        from app.core.event_subscribers import wire_event_subscribers
        wire_event_subscribers(self.event_bus, self.telemetry)

        # Register default scheduled jobs
        self._register_default_jobs()

    def _register_default_services(self) -> None:
        from app.services.storage import StorageService
        from app.services.vault import VaultService
        from app.services.workspace import WorkspaceService
        from app.services.projects import ProjectService
        from app.services.backup import BackupService
        from app.services.automation import AutomationService
        from app.services.documentation import DocumentationService
        from app.services.downloads import DownloadService
        from app.services.notifications import NotificationService
        from app.services.monitoring import MonitoringService
        from app.services.alerts import AlertService
        self.register_service("storage", StorageService())
        self.register_service("vault", VaultService())
        self.register_service("workspace", WorkspaceService())
        self.register_service("projects", ProjectService())
        self.register_service("backup", BackupService())
        self.register_service("automation", AutomationService())
        self.register_service("documentation", DocumentationService())
        self.register_service("downloads", DownloadService())
        self.register_service("notifications", NotificationService())
        self.register_service("monitoring", MonitoringService())
        self.register_service("alerts", AlertService())





    def _register_default_jobs(self) -> None:
        # Task 10: Storage Health Scan (run every 24 hours)
        self.scheduler.register(
            name="Storage Health Scan",
            service="storage",
            mode=ScheduleMode.INTERVAL,
            interval_seconds=86400,
            callback=self._run_storage_health_scan
        )

        # Task 10: Vault Reminder (checks unlocked status durations)
        self.scheduler.register(
            name="Vault Reminder",
            service="vault",
            mode=ScheduleMode.INTERVAL,
            interval_seconds=3600,
            callback=self._run_vault_reminder_check
        )

        # Task 10: Snapshot Retention Prep
        self.scheduler.register(
            name="Snapshot Retention Prep",
            service="storage",
            mode=ScheduleMode.INTERVAL,
            interval_seconds=86400,
            callback=self._run_snapshot_retention_prep
        )

    def _run_storage_health_scan(self) -> None:
        # Trigger storage sync
        from app.core.database import SessionLocal
        db = SessionLocal()
        try:
            storage_svc = self.get_service("storage")
            if hasattr(storage_svc, "sync_devices"):
                storage_svc.sync_devices(db)
        except Exception as exc:
            print(f"[HomelabCore] Storage health scan job failed: {exc}")
        finally:
            db.close()

    def _run_vault_reminder_check(self) -> None:
        from app.core.database import SessionLocal
        from app.models.vault import VaultMetadata
        db = SessionLocal()
        try:
            meta = db.query(VaultMetadata).order_by(VaultMetadata.created_at.desc()).first()
            if meta and meta.status == "UNLOCKED" and meta.last_unlock_time:
                from datetime import datetime, timezone
                elapsed = datetime.now(timezone.utc) - meta.last_unlock_time
                if elapsed.total_seconds() > 43200: # 12 hours
                    self.event_bus.publish(
                        Event(
                            name="vault.unlocked_reminder_warning",
                            source="homelab_core",
                            payload={"message": "Vault has been left unlocked for over 12 hours."}
                        )
                    )
        except Exception as exc:
            print(f"[HomelabCore] Vault reminder job failed: {exc}")
        finally:
            db.close()

    def _run_snapshot_retention_prep(self) -> None:
        # Placeholder for delete after X cycles
        pass



    @classmethod
    def instance(cls) -> "HomelabCore":
        """Return the global HomelabCore singleton (created on first call)."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @classmethod
    def reset(cls) -> None:
        """Reset the singleton (primarily for testing)."""
        cls._instance = None

    # ------------------------------------------------------------------
    # Service Registry
    # ------------------------------------------------------------------

    def register_service(self, name: str, service: object) -> None:
        """Register a service instance under *name*."""
        if name in self._services:
            raise ValueError(f"Service '{name}' is already registered.")
        self._services[name] = service

    def get_service(self, name: str) -> object:
        """Return the registered service for *name*."""
        if name not in self._services:
            raise KeyError(f"Service '{name}' is not registered.")
        return self._services[name]

    @property
    def registered_services(self) -> list[str]:
        """List the names of all registered services."""
        return list(self._services.keys())

    # ------------------------------------------------------------------
    # Lifecycle helpers
    # ------------------------------------------------------------------

    def startup(self) -> None:
        """Perform the platform startup sequence."""
        self.state_machine.transition(ServerState.STARTING)
        self.event_bus.publish(Event(name="core.starting", source="homelab_core"))

        # Initialize registered services
        for name, service in list(self._services.items()):
            if hasattr(service, "initialize"):
                service.initialize()

        self.state_machine.transition(ServerState.RUNNING)
        self.event_bus.publish(Event(name="core.running", source="homelab_core"))

    def shutdown(self) -> None:
        """Perform the platform shutdown sequence."""
        self.state_machine.transition(ServerState.SHUTTING_DOWN)
        self.event_bus.publish(Event(name="core.shutting_down", source="homelab_core"))

        # Shutdown registered services
        for name, service in list(self._services.items()):
            if hasattr(service, "shutdown"):
                service.shutdown()

        self.state_machine.transition(ServerState.OFFLINE)
        self.event_bus.publish(Event(name="core.offline", source="homelab_core"))

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _on_state_change(self, previous: ServerState, current: ServerState) -> None:
        """Broadcast a state-change event whenever the server transitions."""
        self.event_bus.publish(
            Event(
                name="server.state_changed",
                source="homelab_core",
                payload={"previous": previous.value, "current": current.value},
            )
        )
