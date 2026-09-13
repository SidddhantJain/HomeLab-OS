"""
HomeLab OS — Vault Lifecycle Manager

Defines states and state transition pathways for the encrypted vault:
LOCKED → UNLOCKING → UNLOCKED → LOCKING → LOCKED
"""

from __future__ import annotations

import enum


class VaultState(str, enum.Enum):
    LOCKED = "LOCKED"
    UNLOCKING = "UNLOCKING"
    UNLOCKED = "UNLOCKED"
    LOCKING = "LOCKING"


class VaultLifecycle:
    """Manages secure transitions for the encrypted private vault states."""

    def __init__(self, initial_state: VaultState = VaultState.LOCKED) -> None:
        self._state = initial_state

    @property
    def state(self) -> VaultState:
        return self._state

    def can_transition_to(self, target: VaultState) -> bool:
        """Enforces safe state transitions."""
        transitions = {
            VaultState.LOCKED: [VaultState.UNLOCKING, VaultState.UNLOCKED],
            VaultState.UNLOCKING: [VaultState.UNLOCKED, VaultState.LOCKED, VaultState.LOCKING],
            VaultState.UNLOCKED: [VaultState.LOCKING, VaultState.LOCKED],
            VaultState.LOCKING: [VaultState.LOCKED, VaultState.UNLOCKED]
        }
        return target in transitions.get(self._state, [])

    def transition(self, target: VaultState) -> None:
        """Transitions state safely without uncaught exceptions."""
        if target == self._state:
            return
        self._state = target
