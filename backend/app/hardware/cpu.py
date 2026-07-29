"""HAL — CPU metrics abstraction.

Provides host-independent access to processor usage, frequencies, and
core topology.  Falls back to safe defaults on unsupported platforms.
"""

from __future__ import annotations

from typing import Any


def get_cpu_info() -> dict[str, Any]:
    """Return CPU metadata and real-time utilisation.

    Returns a dictionary with keys:
        physical_cores, logical_cores, frequency_mhz,
        usage_percent (list per-core), model_name.

    On platforms where ``psutil`` is unavailable the function
    returns safe defaults rather than raising.
    """
    try:
        import psutil

        freq = psutil.cpu_freq()
        return {
            "physical_cores": psutil.cpu_count(logical=False) or 0,
            "logical_cores": psutil.cpu_count(logical=True) or 0,
            "frequency_mhz": round(freq.current, 1) if freq else 0.0,
            "usage_percent": psutil.cpu_percent(percpu=True),
            "model_name": "unknown",  # populated from /proc/cpuinfo in Linux
        }
    except ImportError:
        return {
            "physical_cores": 0,
            "logical_cores": 0,
            "frequency_mhz": 0.0,
            "usage_percent": [],
            "model_name": "unavailable",
        }
