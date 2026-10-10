from __future__ import annotations

from typing import List, Mapping, Tuple

import cv2
import numpy as np


def render_menu(
    frame: np.ndarray,
    breadcrumb: str,
    items: List[str],
    active_index: int,
    pinch_active: bool,
    debounce_remaining_s: float,
    origin: Tuple[int, int] = (20, 20),
) -> None:
    x0, y0 = origin
    box_w, box_h = 400, 360

    overlay = frame.copy()
    cv2.rectangle(overlay, (x0, y0), (x0 + box_w, y0 + box_h), (20, 20, 20), -1)
    frame[:] = cv2.addWeighted(overlay, 0.45, frame, 0.55, 0)

    cv2.putText(frame, breadcrumb, (x0 + 14, y0 + 30), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 220, 120), 2)

    base_y = y0 + 66 if breadcrumb == "VISION" else y0 + 98
    step = 36 if breadcrumb == "VISION" else 34
    font = 0.72 if breadcrumb == "VISION" else 0.66

    if breadcrumb != "VISION":
        cv2.putText(frame, breadcrumb, (x0 + 20, y0 + 62), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (180, 255, 200), 2)

    for i, item in enumerate(items):
        y = base_y + i * step
        color = (255, 240, 170) if i == active_index else (220, 220, 220)
        if i == active_index:
            hl_y0 = y - 22
            hl_y1 = y + 10
            hl_color = (40, 70, 95) if pinch_active else (30, 55, 40)
            cv2.rectangle(frame, (x0 + 12, hl_y0), (x0 + box_w - 12, hl_y1), hl_color, -1)
        cv2.putText(frame, item, (x0 + (24 if breadcrumb != "VISION" else 20), y), cv2.FONT_HERSHEY_SIMPLEX, font, color, 2)

    # Pinch/debounce feedback near the menu header to make activation timing clear.
    status_text = "Pinch ready"
    status_color = (150, 255, 170)
    if debounce_remaining_s > 0:
        status_text = f"Debounce {debounce_remaining_s:.2f}s"
        status_color = (90, 180, 255)
    if pinch_active:
        status_text = "Pinch"
        status_color = (255, 220, 120)
    cv2.putText(frame, status_text, (x0 + box_w - 150, y0 + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, status_color, 1)


def render_status_bar(frame: np.ndarray, status: Mapping[str, str], width: int, height: int) -> None:
    bar_h = 30
    y0 = height - bar_h

    overlay = frame.copy()
    cv2.rectangle(overlay, (0, y0), (width, height), (10, 10, 10), -1)
    frame[:] = cv2.addWeighted(overlay, 0.4, frame, 0.6, 0)

    text = (
        f"CPU {status.get('cpu_temp', '--')} | Fan {status.get('fan_rpm', '--')} | "
        f"FPS {status.get('fps', '--')} | Cam {status.get('camera', '--')} | "
        f"WiFi {status.get('wifi', '--')} | Power {status.get('power', '--')} | "
        f"Collar {status.get('collar', 'disconnected')} ({status.get('collar_battery', '--')})"
    )
    cv2.putText(frame, text, (10, height - 9), cv2.FONT_HERSHEY_SIMPLEX, 0.52, (220, 220, 220), 1)


def render_cursor(frame: np.ndarray, cursor_xy: Tuple[int, int], pinched: bool = False) -> None:
    color = (80, 255, 90) if not pinched else (90, 210, 255)
    cv2.circle(frame, cursor_xy, 10, color, 2)
    cv2.circle(frame, cursor_xy, 2, color, -1)
