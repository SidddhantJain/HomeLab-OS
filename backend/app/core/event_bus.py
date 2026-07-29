"""
HomeLab OS — Internal Event Bus

A lightweight, in-process publish/subscribe event system that decouples
platform services.  Instead of services calling one another directly,
they emit events through the bus and interested subscribers react.

Design goals:
    • Zero external dependencies (no Redis/Kafka required at this stage).
    • Thread-safe publishing and subscription.
    • Typed event payloads via dataclass conventions.
    • Wildcard subscription support (e.g. ``storage.*``).

Future: the bus can be backed by Redis Pub/Sub for multi-process or
multi-node deployments without changing the publishing API.
"""

from __future__ import annotations

import threading
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable
from fnmatch import fnmatch


@dataclass(frozen=True)
class Event:
    """Standard event envelope transmitted through the bus.

    Attributes:
        name:      Dot-delimited event identifier (e.g. ``storage.device.mounted``).
        source:    Name of the originating service.
        timestamp: UTC timestamp of event creation.
        payload:   Arbitrary data associated with the event.
    """

    name: str
    source: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    payload: dict[str, Any] = field(default_factory=dict)


EventHandler = Callable[[Event], None]


class EventBus:
    """Central event bus for inter-service communication.

    Usage:
        bus = EventBus()
        bus.subscribe("storage.*", on_storage_event)
        bus.publish(Event(name="storage.device.mounted", source="storage_service"))
    """

    def __init__(self) -> None:
        self._handlers: list[tuple[str, EventHandler]] = []
        self._lock = threading.Lock()
        self._event_log: list[Event] = []

    def subscribe(self, pattern: str, handler: EventHandler) -> None:
        """Subscribe *handler* to events matching *pattern*.

        *pattern* supports glob-style wildcards via ``fnmatch``:
        ``"storage.*"`` matches ``"storage.mount"`` and ``"storage.health"``.
        ``"*"`` matches every event.
        """
        with self._lock:
            self._handlers.append((pattern, handler))

    def unsubscribe(self, handler: EventHandler) -> None:
        """Remove all subscriptions for the given *handler*."""
        with self._lock:
            self._handlers = [(p, h) for p, h in self._handlers if h is not handler]

    def publish(self, event: Event) -> None:
        """Publish *event* to all matching subscribers.

        Handlers are called synchronously in subscription order.
        Exceptions in individual handlers are caught and logged so that
        one failing subscriber cannot break the event chain.
        """
        with self._lock:
            self._event_log.append(event)
            matching = [(p, h) for p, h in self._handlers if fnmatch(event.name, p)]

        for _pattern, handler in matching:
            try:
                handler(event)
            except Exception as exc:  # noqa: BLE001
                # In production this would route to a structured logger.
                print(f"[EventBus] Handler error for '{event.name}': {exc}")

    @property
    def event_log(self) -> list[Event]:
        """Return a copy of all published events (useful for diagnostics)."""
        return list(self._event_log)

    def clear_log(self) -> None:
        """Clear the internal event log."""
        with self._lock:
            self._event_log.clear()
