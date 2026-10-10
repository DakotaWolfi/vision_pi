from __future__ import annotations

import time
from typing import Dict

from .fan import fan_rpm
from .power import power_summary
from .thermal import cpu_temp_c
from .wifi import wifi_summary


class StatusCollector:
    def __init__(self) -> None:
        self._last_frame_s = time.time()
        self._last_sample_s = 0.0
        self.sample_interval_s = 1.0
        self.fps = 0.0
        self.cpu_temp = "--"
        self.fan = "--"
        self.wifi = "--"
        self.power = "--"

    def update_fps(self) -> None:
        now = time.time()
        dt = max(1e-3, now - self._last_frame_s)
        self.fps = 1.0 / dt
        self._last_frame_s = now

    def _refresh_telemetry(self) -> None:
        now = time.time()
        if now - self._last_sample_s < self.sample_interval_s:
            return
        self._last_sample_s = now

        temp_c = cpu_temp_c()
        self.cpu_temp = f"{temp_c:4.1f}C" if temp_c is not None else "--"

        rpm = fan_rpm()
        self.fan = f"{rpm} rpm" if rpm is not None else "--"

        self.wifi = wifi_summary()
        self.power = power_summary()

    def snapshot(self, camera_name: str, collar_state: str = "disconnected", collar_battery: str = "--") -> Dict[str, str]:
        self._refresh_telemetry()
        return {
            "cpu_temp": self.cpu_temp,
            "fan_rpm": self.fan,
            "fps": f"{self.fps:4.1f}",
            "camera": camera_name,
            "wifi": self.wifi,
            "power": self.power,
            "collar": collar_state,
            "collar_battery": collar_battery,
        }
