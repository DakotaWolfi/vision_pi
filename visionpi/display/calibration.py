from __future__ import annotations

from typing import Tuple

import cv2
import numpy as np

from visionpi.config import DisplaySettings, EyeCalibration


def _apply_crop(frame: np.ndarray, cal: EyeCalibration) -> np.ndarray:
    h, w = frame.shape[:2]
    l = max(0, min(w - 1, cal.crop.left))
    t = max(0, min(h - 1, cal.crop.top))
    r = max(0, min(w - 1, cal.crop.right))
    b = max(0, min(h - 1, cal.crop.bottom))

    x0 = l
    y0 = t
    x1 = max(x0 + 1, w - r)
    y1 = max(y0 + 1, h - b)
    return frame[y0:y1, x0:x1]


def apply_eye_calibration(frame: np.ndarray, cal: EyeCalibration, out_size: Tuple[int, int]) -> np.ndarray:
    working = _apply_crop(frame, cal)
    if cal.mirror:
        working = cv2.flip(working, 1)

    h, w = working.shape[:2]
    cx, cy = w * 0.5, h * 0.5
    m = cv2.getRotationMatrix2D((cx, cy), cal.rotation_deg, cal.scale)
    m[0, 2] += cal.offset_x
    m[1, 2] += cal.offset_y

    transformed = cv2.warpAffine(working, m, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    return cv2.resize(transformed, out_size)


def apply_display_settings(frame: np.ndarray, settings: DisplaySettings) -> np.ndarray:
    out = frame.astype(np.float32)
    out *= settings.brightness
    out = np.clip(out, 0, 255).astype(np.uint8)

    if settings.zoom > 1.0:
        h, w = out.shape[:2]
        zw = int(w / settings.zoom)
        zh = int(h / settings.zoom)
        x0 = max(0, (w - zw) // 2)
        y0 = max(0, (h - zh) // 2)
        out = out[y0 : y0 + zh, x0 : x0 + zw]
        out = cv2.resize(out, (w, h))

    if settings.night_mode:
        green = out[:, :, 1]
        out = np.zeros_like(out)
        out[:, :, 1] = green

    return out
