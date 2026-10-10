from __future__ import annotations

from pathlib import Path
from typing import Optional, Tuple


def discover_fan_input() -> Optional[Tuple[str, Path]]:
    for hwmon in sorted(Path("/sys/class/hwmon").glob("hwmon*")):
        fan_input = hwmon / "fan1_input"
        if not fan_input.exists():
            continue
        name_file = hwmon / "name"
        name = "unknown"
        if name_file.exists():
            try:
                name = name_file.read_text().strip()
            except OSError:
                pass
        return name, fan_input
    return None


def fan_rpm() -> Optional[int]:
    discovered = discover_fan_input()
    if discovered is None:
        return None
    _, fan_input = discovered
    try:
        return int(fan_input.read_text().strip())
    except (OSError, ValueError):
        return None
