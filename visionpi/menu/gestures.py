from __future__ import annotations

import math
import time
from dataclasses import dataclass
from typing import Optional, Tuple

import cv2
import mediapipe as mp
import numpy as np


@dataclass
class GestureEvent:
    cursor_xy: Tuple[int, int]
    pinch_confirmed: bool
    pinch_active: bool
    debounce_remaining_s: float
    pinch_distance_px: float


class GestureTracker:
    def __init__(self, frame_size: Tuple[int, int], threshold_px: float = 26.0, debounce_s: float = 0.33) -> None:
        self.width, self.height = frame_size
        self.threshold_px = threshold_px
        self.debounce_s = debounce_s
        self.was_pinched = False
        self.last_confirm_s = 0.0

        self.hands = mp.solutions.hands.Hands(
            model_complexity=0,
            max_num_hands=1,
            min_detection_confidence=0.55,
            min_tracking_confidence=0.5,
        )

    def update(self, frame_bgr: np.ndarray) -> Optional[GestureEvent]:
        rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        result = self.hands.process(rgb)
        if not result.multi_hand_landmarks:
            return None

        landmarks = result.multi_hand_landmarks[0].landmark
        index_tip = landmarks[8]
        thumb_tip = landmarks[4]

        cx = int(index_tip.x * self.width)
        cy = int(index_tip.y * self.height)
        cx = int(np.clip(cx, 0, self.width - 1))
        cy = int(np.clip(cy, 0, self.height - 1))

        distance_px = math.hypot((index_tip.x - thumb_tip.x) * self.width, (index_tip.y - thumb_tip.y) * self.height)
        pinched = distance_px < self.threshold_px
        now_s = time.time()

        pinch_confirmed = False
        if pinched and not self.was_pinched and now_s - self.last_confirm_s >= self.debounce_s:
            pinch_confirmed = True
            self.last_confirm_s = now_s

        self.was_pinched = pinched
        elapsed = now_s - self.last_confirm_s
        debounce_remaining_s = max(0.0, self.debounce_s - elapsed)
        return GestureEvent(
            cursor_xy=(cx, cy),
            pinch_confirmed=pinch_confirmed,
            pinch_active=pinched,
            debounce_remaining_s=debounce_remaining_s,
            pinch_distance_px=distance_px,
        )
