from __future__ import annotations

import time
from typing import Dict


class StatusCollector:
    def __init__(self) -> None:
        self._last_frame_s = time.time()
        self.fps = 0.0

    def update_fps(self) -> None:
        now = time.time()
        dt = max(1e-3, now - self._last_frame_s)
        self.fps = 1.0 / dt
        self._last_frame_s = now

    def snapshot(self, camera_name: str) -> Dict[str, str]:
        return {
            "cpu_temp": "--",
            "fan_rpm": "--",
            "fps": f"{self.fps:4.1f}",
            "camera": camera_name,
            "collar": "disconnected",
        }
