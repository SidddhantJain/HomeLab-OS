"""HAL — Storage / disk metrics abstraction.

Enumerates physical block devices, mount points, and usage statistics.
"""

from __future__ import annotations

from typing import Any


def get_storage_info() -> list[dict[str, Any]]:
    """Return a list of mounted partitions with usage data.

    Each dict: device, mountpoint, fstype, total_gb, used_gb, free_gb, percent.
    """
    try:
        import psutil

        partitions = psutil.disk_partitions(all=False)
        result: list[dict[str, Any]] = []
        for p in partitions:
            try:
                usage = psutil.disk_usage(p.mountpoint)
                result.append({
                    "device": p.device,
                    "mountpoint": p.mountpoint,
                    "fstype": p.fstype,
                    "total_gb": round(usage.total / (1024 ** 3), 2),
                    "used_gb": round(usage.used / (1024 ** 3), 2),
                    "free_gb": round(usage.free / (1024 ** 3), 2),
                    "percent": usage.percent,
                })
            except PermissionError:
                continue
        return result
    except ImportError:
        return []
