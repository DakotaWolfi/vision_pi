from __future__ import annotations

import math
import time
from typing import Optional, Tuple

import cv2
import numpy as np

try:
    from picamera2 import Picamera2
except ImportError:  # pragma: no cover - depends on Pi runtime
    Picamera2 = None


class CameraSource:
    def read(self) -> Optional[np.ndarray]:
        raise NotImplementedError

    def close(self) -> None:
        return


class PiCameraSource(CameraSource):
    def __init__(self, camera_num: int, size: Tuple[int, int]) -> None:
        if Picamera2 is None:
            raise RuntimeError("Picamera2 is unavailable")
        self.picam = Picamera2(camera_num)
        config = self.picam.create_preview_configuration(main={"size": size, "format": "RGB888"}, buffer_count=3)
        self.picam.configure(config)
        self.picam.start()

    def read(self) -> Optional[np.ndarray]:
        frame = self.picam.capture_array()
        # Picamera2 RGB888 buffers are BGR byte-ordered for OpenCV.
        # The old conversion swapped red and blue a second time.
        return frame

    def close(self) -> None:
        self.picam.stop()


class WiFiEyeSource(CameraSource):
    def __init__(self, stream_url: str, size: Tuple[int, int], timeout_s: float = 2.0) -> None:
        self.size = size
        self.stream_url = stream_url
        self.timeout_s = timeout_s
        self.cap = cv2.VideoCapture(stream_url)
        self.last_ok_s = 0.0

    def read(self) -> Optional[np.ndarray]:
        ok, frame = self.cap.read()
        if not ok:
            if time.time() - self.last_ok_s > self.timeout_s:
                self.cap.release()
                self.cap = cv2.VideoCapture(self.stream_url)
            return None
        self.last_ok_s = time.time()
        return cv2.resize(frame, self.size)

    def close(self) -> None:
        self.cap.release()


class MockCameraSource(CameraSource):
    def __init__(self, label: str, size: Tuple[int, int]) -> None:
        self.label = label
        self.w, self.h = size
        self.t0 = time.time()

    def read(self) -> Optional[np.ndarray]:
        frame = np.zeros((self.h, self.w, 3), dtype=np.uint8)
        t = time.time() - self.t0
        color = int(90 + 70 * math.sin(t))
        frame[:, :] = (color, 30, 150 - color // 2)
        cv2.putText(frame, self.label, (20, 44), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)
        return frame
