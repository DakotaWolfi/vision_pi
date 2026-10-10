from __future__ import annotations

from pathlib import Path
from typing import Optional


def battery_percent() -> Optional[int]:
    base = Path("/sys/class/power_supply")
    if not base.exists():
        return None
    for supply in sorted(base.iterdir()):
        cap = supply / "capacity"
        if not cap.exists():
            continue
        try:
            return int(cap.read_text().strip())
        except (OSError, ValueError):
            continue
    return None


def power_summary() -> str:
    pct = battery_percent()
    if pct is None:
        return "external"
    return f"{pct}%"
