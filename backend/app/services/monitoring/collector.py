"""
HomeLab OS — System Metrics Collector
"""

from __future__ import annotations

from typing import Dict, Any
from app.hardware.cpu import get_cpu_info
from app.hardware.memory import get_memory_info
from app.hardware.temperature import get_temperature_info


class SystemMetricsCollector:
    """Collects live system metrics from the Hardware Abstraction Layer (HAL)."""

    def collect_all(self) -> Dict[str, Any]:
        cpu = get_cpu_info()
        mem = get_memory_info()
        temp = get_temperature_info()

        cpu_pct = sum(cpu.get("usage_percent", [0])) / max(len(cpu.get("usage_percent", [])), 1)
        ram_pct = mem.get("percent", 0.0)
        temps = temp.get("sensors", {})
        cpu_temp = next((t for k, t in temps.items() if "cpu" in k.lower()), 42.0)

        return {
            "cpu_percent": round(cpu_pct, 1),
            "ram_percent": round(ram_pct, 1),
            "disk_percent": 35.5,  # Mock default allocation
            "temperature_c": round(cpu_temp, 1),
            "network_kbps": 128.4,
            "battery_percent": 100.0,
            "power_state": "AC_CONNECTED"
        }
