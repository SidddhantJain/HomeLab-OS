"""
HomeLab OS — Unified Migration Framework

Coordinates versioned schema migrations across all platform dimensions, including
relational database schemas (Alembic), YAML configuration changes, Docker environment profiles,
installed plugins, physical storage mount definitions, and vault security setups.
"""

from __future__ import annotations

import enum
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional


class MigrationScope(str, enum.Enum):
    """The system boundary that a migration operates upon."""

    DATABASE = "database"
    CONFIG = "config"
    DOCKER = "docker"
    PLUGIN = "plugin"
    STORAGE = "storage"
    VAULT = "vault"


@dataclass
class MigrationJob:
    """Represents a migration script target."""

    version: str
    scope: MigrationScope
    description: str
    up_action: Callable[[], bool]
    down_action: Callable[[], bool]
    applied_at: Optional[datetime] = None


class MigrationManager:
    """Unified coordinator for platform structural migrations.

    Usage:
        mm = MigrationManager()
        mm.register_migration(
            version="1.0.1",
            scope=MigrationScope.CONFIG,
            description="Add SMART scan intervals",
            up_action=upgrade_config,
            down_action=downgrade_config
        )
        mm.apply_all()
    """

    def __init__(self) -> None:
        self._migrations: List[MigrationJob] = []
        self._history: List[Dict[str, Any]] = []

    def register_migration(
        self,
        version: str,
        scope: MigrationScope,
        description: str,
        up_action: Callable[[], bool],
        down_action: Callable[[], bool]
    ) -> None:
        """Register an upgrade/downgrade migration step."""
        job = MigrationJob(
            version=version,
            scope=scope,
            description=description,
            up_action=up_action,
            down_action=down_action
        )
        self._migrations.append(job)
        # Sort chronologically by version string
        self._migrations.sort(key=lambda x: x.version)

    def apply_all(self) -> List[MigrationJob]:
        """Apply all outstanding unapplied migrations."""
        applied: List[MigrationJob] = []
        for m in self._migrations:
            if m.applied_at is None:
                success = False
                try:
                    success = m.up_action()
                except Exception as exc:  # noqa: BLE001
                    print(f"[MigrationManager] Migration {m.version} failed: {exc}")

                if success:
                    m.applied_at = datetime.now(timezone.utc)
                    self._history.append({
                        "version": m.version,
                        "scope": m.scope.value,
                        "action": "up",
                        "timestamp": m.applied_at
                    })
                    applied.append(m)
        return applied

    @property
    def migrations(self) -> List[MigrationJob]:
        """Get list of registered migrations."""
        return list(self._migrations)

    @property
    def history(self) -> List[Dict[str, Any]]:
        """Get history of applied actions."""
        return list(self._history)
