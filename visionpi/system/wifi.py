from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Optional


def connected_interface() -> Optional[str]:
    for iface in ("wlan0", "wlan1"):
        state = Path(f"/sys/class/net/{iface}/operstate")
        if not state.exists():
            continue
        try:
            if state.read_text().strip() == "up":
                return iface
        except OSError:
            continue
    return None


def wifi_ssid() -> Optional[str]:
    iface = connected_interface()
    if iface is None:
        return None
    try:
        out = subprocess.check_output(["iwgetid", iface, "-r"], text=True, timeout=0.4).strip()
        return out or None
    except Exception:
        return iface


def wifi_summary() -> str:
    ssid = wifi_ssid()
    if ssid:
        return ssid
    return "offline"
