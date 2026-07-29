"""
HomeLab OS — Server State Machine

Defines the formal lifecycle states of the HomeLab OS server and enforces
valid transitions. All platform services should observe and react to state
changes rather than maintaining independent boolean flags.

States:
    BOOTING        → Initial hardware/OS boot sequence
    STARTING       → Core services initialising
    RUNNING        → Normal operation
    MAINTENANCE    → Scheduled maintenance window
    BACKUP         → Backup job in progress
    UPDATING       → Software update in progress
    RESTORING      → Restore from backup in progress
    SHUTTING_DOWN  → Graceful shutdown sequence
    OFFLINE        → Server powered off or unreachable
"""

from __future__ import annotations

import enum
import threading
from datetime import datetime, timezone
from typing import Callable, Optional


class ServerState(str, enum.Enum):
    """Enumeration of all valid server lifecycle states."""

    BOOTING = "BOOTING"
    STARTING = "STARTING"
    RUNNING = "RUNNING"
    MAINTENANCE = "MAINTENANCE"
    BACKUP = "BACKUP"
    UPDATING = "UPDATING"
    RESTORING = "RESTORING"
    SHUTTING_DOWN = "SHUTTING_DOWN"
    OFFLINE = "OFFLINE"


# Allowed state transitions: source → set of valid targets
_TRANSITIONS: dict[ServerState, set[ServerState]] = {
    ServerState.BOOTING: {ServerState.STARTING, ServerState.OFFLINE},
    ServerState.STARTING: {ServerState.RUNNING, ServerState.OFFLINE},
    ServerState.RUNNING: {
        ServerState.MAINTENANCE,
        ServerState.BACKUP,
        ServerState.UPDATING,
        ServerState.SHUTTING_DOWN,
    },
    ServerState.MAINTENANCE: {ServerState.RUNNING, ServerState.SHUTTING_DOWN},
    ServerState.BACKUP: {ServerState.RUNNING, ServerState.SHUTTING_DOWN},
    ServerState.UPDATING: {ServerState.RESTORING, ServerState.RUNNING, ServerState.SHUTTING_DOWN},
    ServerState.RESTORING: {ServerState.RUNNING, ServerState.SHUTTING_DOWN},
    ServerState.SHUTTING_DOWN: {ServerState.OFFLINE},
    ServerState.OFFLINE: {ServerState.BOOTING},
}

StateChangeCallback = Callable[[ServerState, ServerState], None]


class ServerStateMachine:
    """Thread-safe state machine governing the HomeLab OS server lifecycle.

    Usage:
        sm = ServerStateMachine()
        sm.on_change(my_callback)
        sm.transition(ServerState.STARTING)
    """

    def __init__(self, initial: ServerState = ServerState.BOOTING) -> None:
        self._state = initial
        self._lock = threading.Lock()
        self._listeners: list[StateChangeCallback] = []
        self._history: list[tuple[ServerState, ServerState, datetime]] = []

    @property
    def state(self) -> ServerState:
        """Return the current server state."""
        return self._state

    @property
    def history(self) -> list[tuple[ServerState, ServerState, datetime]]:
        """Return the chronological list of state transitions."""
        return list(self._history)

    def on_change(self, callback: StateChangeCallback) -> None:
        """Register a listener that is invoked on every state change."""
        self._listeners.append(callback)

    def can_transition(self, target: ServerState) -> bool:
        """Check whether a transition from the current state to *target* is allowed."""
        return target in _TRANSITIONS.get(self._state, set())

    def transition(self, target: ServerState) -> None:
        """Transition to *target* state, notifying all listeners.

        Raises:
            ValueError: If the transition is not permitted.
        """
        with self._lock:
            if not self.can_transition(target):
                raise ValueError(
                    f"Invalid state transition: {self._state.value} → {target.value}"
                )
            previous = self._state
            self._state = target
            self._history.append((previous, target, datetime.now(timezone.utc)))

        for listener in self._listeners:
            listener(previous, target)
