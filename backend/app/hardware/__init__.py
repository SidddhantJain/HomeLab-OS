"""
HomeLab OS — Hardware Abstraction Layer (HAL)

Provides a unified Python interface over host hardware, insulating
all platform services from OS-specific system calls.

Sub-modules:
    cpu         — Processor usage, frequencies, and core counts.
    memory      — RAM and swap utilisation.
    storage     — Physical disk enumeration, mount points, and SMART status.
    network     — Network interface listing and throughput.
    battery     — Battery charge percentage and AC power status.
    temperature — Thermal sensor readings and fan speed (if available).
    power       — Power profiles and energy consumption estimates.
"""
