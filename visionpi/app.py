from __future__ import annotations

import argparse

import cv2

from . import __version__
from .cameras import CameraManager
from .cameras.manager import CameraConfig
from .display import render_cursor, render_menu, render_status_bar
from .menu import MENU_TREE, GestureTracker, MenuController
from .system import StatusCollector


class VisionPiApp:
    def __init__(self, width: int, height: int, wifi_eye_1: str = "", wifi_eye_2: str = "") -> None:
        self.width = width
        self.height = height
        self.camera_name = "Stereo"

        self.cameras = CameraManager(CameraConfig(width=width, height=height, wifi_eye_1=wifi_eye_1, wifi_eye_2=wifi_eye_2))
        self.menu = MenuController(MENU_TREE)
        self.gestures = GestureTracker((width, height))
        self.status = StatusCollector()
        self.cursor_xy = (width // 2, height // 2)
        self.pinched = False

    def _apply_selection(self, selection) -> None:
        if selection is None:
            return
        if selection.root == "CAMERAS":
            self.camera_name = selection.item

    def run(self) -> None:
        cv2.namedWindow("VisionPi", cv2.WINDOW_NORMAL)

        running = True
        while running:
            frame = self.cameras.compose(self.camera_name)

            event = self.gestures.update(frame)
            if event is not None:
                self.cursor_xy = event.cursor_xy
                self.pinched = event.pinch_distance_px < self.gestures.threshold_px
                self.menu.update_hover(self.cursor_xy)
                if event.pinch_confirmed:
                    running, _, selection = self.menu.confirm()
                    self._apply_selection(selection)

            breadcrumb = self.menu.breadcrumb()
            items = self.menu.current_items()
            active_index = self.menu.active_root_index if not self.menu.in_submenu else self.menu.active_sub_index

            render_menu(frame, breadcrumb, items, active_index)
            self.status.update_fps()
            render_status_bar(frame, self.status.snapshot(self.camera_name), self.width, self.height)
            render_cursor(frame, self.cursor_xy, self.pinched)

            cv2.imshow("VisionPi", frame)
            key = cv2.waitKey(1) & 0xFF
            if key in (27, ord("q")):
                break

        self.cameras.close()
        cv2.destroyAllWindows()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=f"VisionPi {__version__}")
    parser.add_argument("--width", type=int, default=1280)
    parser.add_argument("--height", type=int, default=720)
    parser.add_argument("--wifi-eye-1", default="")
    parser.add_argument("--wifi-eye-2", default="")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    app = VisionPiApp(width=args.width, height=args.height, wifi_eye_1=args.wifi_eye_1, wifi_eye_2=args.wifi_eye_2)
    app.run()
