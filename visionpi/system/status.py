"""Combined system status for the HUD."""

from .fan import fan_rpm
from .thermal import cpu_temp_c


def snapshot() -> dict:
    return {
        "cpu_temp_c": cpu_temp_c(),
        "fan_rpm": fan_rpm(),
    }
