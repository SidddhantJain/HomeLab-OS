"""HAL — Network interface abstraction.

Enumerates NICs, IP addresses, and real-time throughput counters.
"""

from __future__ import annotations

from typing import Any


def get_network_info() -> list[dict[str, Any]]:
    """Return a list of network interfaces with addresses and I/O counters.

    Each dict: name, addresses (list), bytes_sent, bytes_recv, is_up.
    """
    try:
        import psutil

        addrs = psutil.net_if_addrs()
        stats = psutil.net_if_stats()
        io = psutil.net_io_counters(pernic=True)
        result: list[dict[str, Any]] = []
        for name, addr_list in addrs.items():
            nic_io = io.get(name)
            result.append({
                "name": name,
                "addresses": [a.address for a in addr_list],
                "is_up": stats[name].isup if name in stats else False,
                "bytes_sent": nic_io.bytes_sent if nic_io else 0,
                "bytes_recv": nic_io.bytes_recv if nic_io else 0,
            })
        return result
    except ImportError:
        return []
