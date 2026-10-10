#!/usr/bin/env python3
"""Known-good baseline prototype for VisionPi.

This script keeps the app logic in one place intentionally so it can serve as
an immutable baseline while the modular package implementation is verified.
"""

from __future__ import annotations

import argparse
import math
import time
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

import cv2
import mediapipe as mp
import numpy as np

try:
    from picamera2 import Picamera2
except ImportError:  # pragma: no cover - depends on Pi runtime
    Picamera2 = None


MENU_TREE = {
    "CAMERAS": ["Stereo", "Left", "Right", "WiFi Eye 1", "WiFi Eye 2"],
    "DISPLAY": ["Zoom", "Brightness", "Night Mode", "Calibration"],
    "COLLAR PET": [
        "Status",
        "Face / Expression",
        "LEDs",
        "Haptic",
        "NFC",
        "Music / Recognition",
        "PetMind",
    ],
    "SYSTEM": ["CPU temperature", "Fan RPM", "FPS", "WiFi", "Power"],
    "EXIT": [],
}


@dataclass
class PinchState:
    threshold_px: float = 26.0
    debounce_s: float = 0.33
    was_pinched: bool = False
    last_confirm_s: float = 0.0

    def update(self, distance_px: float, now_s: float) -> bool:
        pinched = distance_px < self.threshold_px
        confirmed = False
        if pinched and not self.was_pinched and now_s - self.last_confirm_s >= self.debounce_s:
            self.last_confirm_s = now_s
            confirmed = True
        self.was_pinched = pinched
        return confirmed


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
        config = self.picam.create_preview_configuration(main={"size": size, "format": "RGB888"})
        self.picam.configure(config)
        self.picam.start()

    def read(self) -> Optional[np.ndarray]:
        frame = self.picam.capture_array()
        return cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    def close(self) -> None:
        self.picam.stop()


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


class App:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.root_items = list(MENU_TREE.keys())
        self.active_root_index = 0
        self.active_sub_index = 0
        self.in_submenu = False
        self.source_name = "Stereo"

        self.left = self._open_camera(0, "Left")
        self.right = self._open_camera(1, "Right")

        self.hands = mp.solutions.hands.Hands(
            model_complexity=0,
            max_num_hands=1,
            min_detection_confidence=0.55,
            min_tracking_confidence=0.5,
        )
        self.pinch = PinchState()
        self.cursor_xy = (self.width // 2, self.height // 2)
        self.fps = 0.0
        self._last_frame_s = time.time()

    def _open_camera(self, camera_num: int, label: str) -> CameraSource:
        try:
            return PiCameraSource(camera_num, (self.width, self.height))
        except Exception:
            return MockCameraSource(f"{label} mock", (self.width, self.height))

    def _render_menu(self, frame: np.ndarray) -> None:
        box_w, box_h = 400, 360
        x0, y0 = 20, 20
        overlay = frame.copy()
        cv2.rectangle(overlay, (x0, y0), (x0 + box_w, y0 + box_h), (20, 20, 20), -1)
        frame[:] = cv2.addWeighted(overlay, 0.45, frame, 0.55, 0)

        cv2.putText(frame, "VISION", (x0 + 14, y0 + 30), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 220, 120), 2)

        if not self.in_submenu:
            for i, item in enumerate(self.root_items):
                y = y0 + 66 + i * 36
                color = (255, 240, 170) if i == self.active_root_index else (220, 220, 220)
                cv2.putText(frame, item, (x0 + 20, y), cv2.FONT_HERSHEY_SIMPLEX, 0.72, color, 2)
        else:
            root = self.root_items[self.active_root_index]
            sub_items = ["< Back"] + MENU_TREE[root]
            title = f"VISION / {root}"
            cv2.putText(frame, title, (x0 + 20, y0 + 62), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (180, 255, 200), 2)
            for i, item in enumerate(sub_items):
                y = y0 + 98 + i * 34
                color = (255, 240, 170) if i == self.active_sub_index else (220, 220, 220)
                cv2.putText(frame, item, (x0 + 24, y), cv2.FONT_HERSHEY_SIMPLEX, 0.66, color, 2)

    def _render_status_bar(self, frame: np.ndarray) -> None:
        bar_h = 30
        y0 = self.height - bar_h
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, y0), (self.width, self.height), (10, 10, 10), -1)
        frame[:] = cv2.addWeighted(overlay, 0.4, frame, 0.6, 0)

        text = f"FPS {self.fps:4.1f} | Camera: {self.source_name} | CollarPet: disconnected"
        cv2.putText(frame, text, (10, self.height - 9), cv2.FONT_HERSHEY_SIMPLEX, 0.52, (220, 220, 220), 1)

    def _update_menu_hover(self) -> None:
        cx, cy = self.cursor_xy
        x0, y0 = 20, 20
        if x0 <= cx <= x0 + 400:
            if not self.in_submenu:
                i = (cy - (y0 + 50)) // 36
                if 0 <= i < len(self.root_items):
                    self.active_root_index = int(i)
            else:
                root = self.root_items[self.active_root_index]
                sub_items = ["< Back"] + MENU_TREE[root]
                i = (cy - (y0 + 82)) // 34
                if 0 <= i < len(sub_items):
                    self.active_sub_index = int(i)

    def _confirm_selection(self) -> bool:
        if not self.in_submenu:
            label = self.root_items[self.active_root_index]
            if label == "EXIT":
                return False
            self.in_submenu = True
            self.active_sub_index = 0
            return True

        root = self.root_items[self.active_root_index]
        sub_items = ["< Back"] + MENU_TREE[root]
        label = sub_items[self.active_sub_index]
        if label == "< Back":
            self.in_submenu = False
            return True
        if root == "CAMERAS":
            self.source_name = label
        return True

    def _compose_frame(self) -> np.ndarray:
        left_frame = self.left.read()
        right_frame = self.right.read()
        if left_frame is None:
            left_frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        if right_frame is None:
            right_frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)

        if self.source_name == "Left":
            return cv2.resize(left_frame, (self.width, self.height))
        if self.source_name == "Right":
            return cv2.resize(right_frame, (self.width, self.height))

        left_half = cv2.resize(left_frame, (self.width // 2, self.height))
        right_half = cv2.resize(right_frame, (self.width // 2, self.height))
        return np.hstack([left_half, right_half])

    def run(self) -> None:
        cv2.namedWindow("VisionPi Prototype", cv2.WINDOW_NORMAL)
        running = True
        while running:
            frame = self._compose_frame()

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = self.hands.process(rgb)
            if result.multi_hand_landmarks:
                lm = result.multi_hand_landmarks[0].landmark
                idx = lm[8]
                thumb = lm[4]
                cx = int(idx.x * self.width)
                cy = int(idx.y * self.height)
                self.cursor_xy = (np.clip(cx, 0, self.width - 1), np.clip(cy, 0, self.height - 1))

                dist = math.hypot((idx.x - thumb.x) * self.width, (idx.y - thumb.y) * self.height)
                if self.pinch.update(dist, time.time()):
                    running = self._confirm_selection()

            self._update_menu_hover()
            self._render_menu(frame)
            self._render_status_bar(frame)

            cv2.circle(frame, self.cursor_xy, 10, (80, 255, 90), 2)
            cv2.circle(frame, self.cursor_xy, 2, (80, 255, 90), -1)

            now = time.time()
            dt = max(1e-3, now - self._last_frame_s)
            self.fps = 1.0 / dt
            self._last_frame_s = now

            cv2.imshow("VisionPi Prototype", frame)
            key = cv2.waitKey(1) & 0xFF
            if key in (27, ord("q")):
                break

        self.left.close()
        self.right.close()
        cv2.destroyAllWindows()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="VisionPi prototype")
    parser.add_argument("--width", type=int, default=1280)
    parser.add_argument("--height", type=int, default=720)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    App(args.width, args.height).run()


if __name__ == "__main__":
    main()
