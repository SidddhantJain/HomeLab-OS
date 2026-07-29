"""
HomeLab OS — Abstract Base Service

Every platform service extends this base class to guarantee a consistent
lifecycle, event registration, and health-reporting interface.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseService(ABC):
    """Abstract base class for all HomeLab OS platform services.

    Subclasses must implement:
        ``name``       — unique service identifier.
        ``initialize`` — setup logic executed during platform startup.
        ``shutdown``   — teardown logic executed during platform shutdown.
        ``health``     — return a health-check dictionary.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique identifier for the service (e.g. ``'authentication'``)."""

    @abstractmethod
    def initialize(self) -> None:
        """Called once during platform startup to set up resources."""

    @abstractmethod
    def shutdown(self) -> None:
        """Called once during platform shutdown to release resources."""

    @abstractmethod
    def health(self) -> dict[str, Any]:
        """Return a dictionary describing the service's current health.

        Expected keys: ``status`` (``'healthy'`` | ``'degraded'`` | ``'unhealthy'``),
        plus any service-specific metrics.
        """
