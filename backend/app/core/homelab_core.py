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
        self._services: dict[str, object] = {}

        # Wire state transitions into the event bus automatically.
        self.state_machine.on_change(self._on_state_change)

        # Register default services
        self._register_default_services()

    def _register_default_services(self) -> None:
        from app.services.storage import StorageService
        self.register_service("storage", StorageService())

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
