"""Raspberry Pi thermal helpers."""

from pathlib import Path

THERMAL_ZONE = Path("/sys/class/thermal/thermal_zone0/temp")


def cpu_temp_c() -> float:
    return int(THERMAL_ZONE.read_text().strip()) / 1000.0
