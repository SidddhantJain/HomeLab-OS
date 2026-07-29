"""HAL — Temperature sensor abstraction.

Reads thermal zone data (CPU, GPU, chassis) and fan RPM if available.
"""

from __future__ import annotations

from typing import Any


def get_temperature_info() -> dict[str, Any]:
    """Return temperature sensor readings and fan speeds.

    Keys: sensors (dict of label → current_temp_c), fans (dict of label → rpm).
    """
    try:
        import psutil

        temps = psutil.sensors_temperatures() or {}
        fans = psutil.sensors_fans() or {}
        return {
            "sensors": {
                f"{chip}.{entry.label or idx}": entry.current
                for chip, entries in temps.items()
                for idx, entry in enumerate(entries)
            },
            "fans": {
                f"{chip}.{entry.label or idx}": entry.current
                for chip, entries in fans.items()
                for idx, entry in enumerate(entries)
            },
        }
    except (ImportError, AttributeError):
        return {"sensors": {}, "fans": {}}
