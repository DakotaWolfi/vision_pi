from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple

import cv2
import numpy as np

from visionpi.config import AppConfig
from visionpi.display.calibration import apply_eye_calibration

from .sources import CameraSource, MockCameraSource, PiCameraSource, WiFiEyeSource


@dataclass
class CameraConfig:
    width: int = 1280
    height: int = 720
    wifi_eye_1: str = ""
    wifi_eye_2: str = ""


class CameraManager:
    def __init__(self, config: CameraConfig, app_config: AppConfig) -> None:
        self.config = config
        self.app_config = app_config
        self.size = (config.width, config.height)
        self._sources: Dict[str, CameraSource] = {}

        self._sources["Left"] = self._open_pi_source(0, "Left")
        self._sources["Right"] = self._open_pi_source(1, "Right")
        self._sources["WiFi Eye 1"] = self._open_wifi_source(config.wifi_eye_1, "WiFi Eye 1")
        self._sources["WiFi Eye 2"] = self._open_wifi_source(config.wifi_eye_2, "WiFi Eye 2")

    def _open_pi_source(self, idx: int, label: str) -> CameraSource:
        try:
            return PiCameraSource(idx, self.size)
        except Exception:
            return MockCameraSource(f"{label} mock", self.size)

    def _open_wifi_source(self, url: str, label: str) -> CameraSource:
        if not url:
            return MockCameraSource(f"{label} not configured", self.size)
        try:
            return WiFiEyeSource(url, self.size)
        except Exception:
            return MockCameraSource(f"{label} unavailable", self.size)

    def _safe_read(self, label: str) -> np.ndarray:
        frame = self._sources[label].read()
        if frame is None:
            frame = np.zeros((self.config.height, self.config.width, 3), dtype=np.uint8)
            cv2.putText(frame, f"{label} no signal", (20, 44), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (100, 100, 255), 2)
        return frame

    def compose(self, source_name: str) -> np.ndarray:
        left_frame = self._safe_read("Left")
        right_frame = self._safe_read("Right")

        left_frame = apply_eye_calibration(
            left_frame,
            self.app_config.calibration["left"],
            (self.config.width, self.config.height),
        )
        right_frame = apply_eye_calibration(
            right_frame,
            self.app_config.calibration["right"],
            (self.config.width, self.config.height),
        )

        if source_name == "Left":
            return cv2.resize(left_frame, (self.config.width, self.config.height))
        if source_name == "Right":
            return cv2.resize(right_frame, (self.config.width, self.config.height))
        if source_name == "WiFi Eye 1":
            return cv2.resize(self._safe_read("WiFi Eye 1"), (self.config.width, self.config.height))
        if source_name == "WiFi Eye 2":
            return cv2.resize(self._safe_read("WiFi Eye 2"), (self.config.width, self.config.height))

        left_half = cv2.resize(left_frame, (self.config.width // 2, self.config.height))
        right_half = cv2.resize(right_frame, (self.config.width // 2, self.config.height))
        return np.hstack([left_half, right_half])

    def close(self) -> None:
        for source in self._sources.values():
            source.close()
