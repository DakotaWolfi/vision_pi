from __future__ import annotations

import math
import os
import time
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple

import cv2
import numpy as np


@dataclass
class GestureEvent:
    cursor_xy: Tuple[int, int]
    pinch_confirmed: bool
    pinch_active: bool
    debounce_remaining_s: float
    pinch_distance_px: float


class GestureTracker:
    MODEL_URL = (
        "https://storage.googleapis.com/mediapipe-models/"
        "hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"
    )

    def __init__(
        self,
        frame_size: Tuple[int, int],
        threshold_px: float = 26.0,
        debounce_s: float = 0.33,
    ) -> None:
        self.width, self.height = frame_size
        self.threshold_px = threshold_px
        self.debounce_s = debounce_s
        self.was_pinched = False
        self.last_confirm_s = 0.0
        self._backend = ""

        try:
            import mediapipe as mp
        except ImportError as exc:
            raise RuntimeError(
                "MediaPipe is required for gesture tracking."
            ) from exc

        self.mp = mp

        if hasattr(mp, "tasks"):
            from mediapipe.tasks import python as mp_python
            from mediapipe.tasks.python import vision

            model_path = self._ensure_hand_model()

            options = vision.HandLandmarkerOptions(
                base_options=mp_python.BaseOptions(
                    model_asset_path=str(model_path)
                ),
                running_mode=vision.RunningMode.IMAGE,
                num_hands=1,
                min_hand_detection_confidence=0.55,
                min_hand_presence_confidence=0.5,
                min_tracking_confidence=0.5,
            )

            self.hands = vision.HandLandmarker.create_from_options(options)
            self._backend = "tasks"
            return

        if hasattr(mp, "solutions"):
            self.hands = mp.solutions.hands.Hands(
                model_complexity=0,
                max_num_hands=1,
                min_detection_confidence=0.55,
                min_tracking_confidence=0.5,
            )
            self._backend = "solutions"
            return

        raise RuntimeError(
            "This MediaPipe install exposes neither Tasks nor Solutions."
        )

    def _ensure_hand_model(self) -> Path:
        override = os.environ.get("VISIONPI_HAND_MODEL", "").strip()

        if override:
            path = Path(override).expanduser()
            if not path.is_file():
                raise FileNotFoundError(
                    f"VISIONPI_HAND_MODEL does not exist: {path}"
                )
            return path

        cache_dir = Path.home() / ".cache" / "visionpi"
        model_path = cache_dir / "hand_landmarker.task"

        if model_path.is_file() and model_path.stat().st_size > 0:
            return model_path

        cache_dir.mkdir(parents=True, exist_ok=True)

        print(f"VisionPi: downloading hand model to {model_path}")
        urllib.request.urlretrieve(self.MODEL_URL, model_path)

        return model_path

    def _landmarks_from_frame(self, frame_bgr: np.ndarray):
        rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)

        if self._backend == "tasks":
            rgb = np.ascontiguousarray(rgb)

            image = self.mp.Image(
                image_format=self.mp.ImageFormat.SRGB,
                data=rgb,
            )

            result = self.hands.detect(image)

            if not result.hand_landmarks:
                return None

            return result.hand_landmarks[0]

        result = self.hands.process(rgb)

        if not result.multi_hand_landmarks:
            return None

        return result.multi_hand_landmarks[0].landmark

    def update(self, frame_bgr: np.ndarray) -> Optional[GestureEvent]:
        landmarks = self._landmarks_from_frame(frame_bgr)

        if landmarks is None:
            self.was_pinched = False
            return None

        index_tip = landmarks[8]
        thumb_tip = landmarks[4]

        cx = int(index_tip.x * self.width)
        cy = int(index_tip.y * self.height)

        cx = int(np.clip(cx, 0, self.width - 1))
        cy = int(np.clip(cy, 0, self.height - 1))

        distance_px = math.hypot(
            (index_tip.x - thumb_tip.x) * self.width,
            (index_tip.y - thumb_tip.y) * self.height,
        )

        pinched = distance_px < self.threshold_px
        now_s = time.time()

        pinch_confirmed = False

        if (
            pinched
            and not self.was_pinched
            and now_s - self.last_confirm_s >= self.debounce_s
        ):
            pinch_confirmed = True
            self.last_confirm_s = now_s

        self.was_pinched = pinched

        elapsed = now_s - self.last_confirm_s
        debounce_remaining_s = max(
            0.0,
            self.debounce_s - elapsed,
        )

        return GestureEvent(
            cursor_xy=(cx, cy),
            pinch_confirmed=pinch_confirmed,
            pinch_active=pinched,
            debounce_remaining_s=debounce_remaining_s,
            pinch_distance_px=distance_px,
        )
