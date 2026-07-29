"""HAL — Power profile abstraction.

Estimates host energy consumption and exposes power-management profiles.
"""

from __future__ import annotations

from typing import Any


def get_power_info() -> dict[str, Any]:
    """Return basic power profile information.

    Keys: profile (str), estimated_watts (float).
    Full implementation requires ``powerprofilesctl`` on Ubuntu 24.04.
    """
    return {
        "profile": "balanced",
        "estimated_watts": 0.0,
        "note": "Full power-profile integration requires Ubuntu 24.04 host.",
    }
