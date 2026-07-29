"""HAL — Memory metrics abstraction.

Provides host-independent access to RAM and swap utilisation.
"""

from __future__ import annotations

from typing import Any


def get_memory_info() -> dict[str, Any]:
    """Return RAM and swap utilisation.

    Keys: total_mb, available_mb, used_mb, percent,
          swap_total_mb, swap_used_mb, swap_percent.
    """
    try:
        import psutil

        vm = psutil.virtual_memory()
        sw = psutil.swap_memory()
        return {
            "total_mb": round(vm.total / (1024 ** 2), 1),
            "available_mb": round(vm.available / (1024 ** 2), 1),
            "used_mb": round(vm.used / (1024 ** 2), 1),
            "percent": vm.percent,
            "swap_total_mb": round(sw.total / (1024 ** 2), 1),
            "swap_used_mb": round(sw.used / (1024 ** 2), 1),
            "swap_percent": sw.percent,
        }
    except ImportError:
        return {
            "total_mb": 0, "available_mb": 0, "used_mb": 0, "percent": 0,
            "swap_total_mb": 0, "swap_used_mb": 0, "swap_percent": 0,
        }
