from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Optional


def _read_temp_from_sysfs() -> Optional[float]:
    zones = sorted(Path("/sys/class/thermal").glob("thermal_zone*"))
    for zone in zones:
        temp_path = zone / "temp"
        type_path = zone / "type"
        if not temp_path.exists():
            continue
        try:
            raw = int(temp_path.read_text().strip())
            c = raw / 1000.0 if raw > 1000 else float(raw)
            zone_type = type_path.read_text().strip().lower() if type_path.exists() else ""
            if "cpu" in zone_type or "soc" in zone_type:
                return c
            if c > 0:
                fallback = c
                # Keep scanning for a more specific CPU/SOC zone.
        except (OSError, ValueError):
            continue
    try:
        return fallback  # type: ignore[name-defined]
    except Exception:
        return None


def _read_temp_from_vcgencmd() -> Optional[float]:
    try:
        out = subprocess.check_output(["vcgencmd", "measure_temp"], text=True, timeout=0.4).strip()
        # Format: temp=54.8'C
        if "=" in out:
            value = out.split("=", 1)[1].split("'", 1)[0]
            return float(value)
    except Exception:
        return None
    return None


def cpu_temp_c() -> Optional[float]:
    value = _read_temp_from_sysfs()
    if value is not None:
        return value
    return _read_temp_from_vcgencmd()
