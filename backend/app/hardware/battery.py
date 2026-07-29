"""HAL — Battery status abstraction.

Reports battery charge level and AC adapter status on laptop hardware.
"""

from __future__ import annotations

from typing import Any, Optional


def get_battery_info() -> Optional[dict[str, Any]]:
    """Return battery status or ``None`` if no battery is present.

    Keys: percent, power_plugged, secs_left.
    """
    try:
        import psutil

        batt = psutil.sensors_battery()
        if batt is None:
            return None
        return {
            "percent": batt.percent,
            "power_plugged": batt.power_plugged,
            "secs_left": batt.secsleft if batt.secsleft != psutil.POWER_TIME_UNLIMITED else -1,
        }
    except ImportError:
        return None
