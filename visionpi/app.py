from __future__ import annotations

import argparse
import os

import cv2

from . import __version__
from .config import AppConfig
from .cameras import CameraManager
from .cameras.manager import CameraConfig
from .collar import CollarClient
from .display.calibration import apply_display_settings
from .display import render_cursor, render_menu, render_status_bar
from .menu import MENU_TREE, GestureTracker, MenuController
from .system import StatusCollector


class VisionPiApp:
    def __init__(self, width: int, height: int, wifi_eye_1: str = "", wifi_eye_2: str = "") -> None:
        self.width = width
        self.height = height
        self.camera_name = "Stereo"
        self.config = AppConfig.load()
        self.calibration_mode = False
        self.calibration_eye = "left"
        self.collar = CollarClient(endpoint=os.environ.get("COLLARPET_ENDPOINT", ""))
        self.last_action_message = ""

        self.cameras = CameraManager(
            CameraConfig(width=width, height=height, wifi_eye_1=wifi_eye_1, wifi_eye_2=wifi_eye_2),
            app_config=self.config,
        )
        self.menu = MenuController(MENU_TREE)
        self.gestures = GestureTracker((width, height))
        self.status = StatusCollector()
        self.cursor_xy = (width // 2, height // 2)
        self.pinched = False
        self.debounce_remaining_s = 0.0

    def _apply_selection(self, selection) -> None:
        if selection is None:
            return
        if selection.root == "CAMERAS":
            self.camera_name = selection.item
        if selection.root == "DISPLAY":
            if selection.item == "Zoom":
                self.config.display.zoom += 0.1
                if self.config.display.zoom > 1.5:
                    self.config.display.zoom = 1.0
                self.config.save()
            elif selection.item == "Brightness":
                self.config.display.brightness += 0.1
                if self.config.display.brightness > 1.5:
                    self.config.display.brightness = 0.8
                self.config.save()
            elif selection.item == "Night Mode":
                self.config.display.night_mode = not self.config.display.night_mode
                self.config.save()
            elif selection.item == "Calibration":
                self.calibration_mode = not self.calibration_mode
        if selection.root == "COLLAR PET":
            self.last_action_message = self._handle_collar_selection(selection.item)

    def _handle_collar_selection(self, item: str) -> str:
        if item == "Status":
            status = self.collar.get_status()
            return f"CollarPet: {status.state}"
        if item == "Face / Expression":
            return f"Face: {self.collar.set_expression('neutral')}"
        if item == "LEDs":
            return f"LEDs: {self.collar.set_led_mode('default')}"
        if item == "Haptic":
            return f"Haptic: {self.collar.vibrate()}"
        if item == "NFC":
            return f"NFC: {self.collar.trigger_nfc()}"
        if item == "Music / Recognition":
            return f"Music: {self.collar.music_recognition()}"
        if item == "PetMind":
            return f"PetMind: {self.collar.petmind()}"
        return ""

    def _handle_calibration_key(self, key: int) -> None:
        if not self.calibration_mode:
            return
        eye = self.config.calibration[self.calibration_eye]

        if key == ord("e"):
            self.calibration_eye = "right" if self.calibration_eye == "left" else "left"
        elif key == ord("a"):
            eye.offset_x -= 2
        elif key == ord("d"):
            eye.offset_x += 2
        elif key == ord("w"):
            eye.offset_y -= 2
        elif key == ord("s"):
            eye.offset_y += 2
        elif key == ord("["):
            eye.scale = max(0.7, eye.scale - 0.02)
        elif key == ord("]"):
            eye.scale = min(1.5, eye.scale + 0.02)
        elif key == ord(","):
            eye.rotation_deg -= 0.5
        elif key == ord("."):
            eye.rotation_deg += 0.5
        elif key == ord("m"):
            eye.mirror = not eye.mirror
        elif key == ord("r"):
            eye.crop.right += 1
        elif key == ord("f"):
            eye.crop.right = max(0, eye.crop.right - 1)
        elif key == ord("t"):
            eye.crop.top += 1
        elif key == ord("g"):
            eye.crop.top = max(0, eye.crop.top - 1)
        elif key == ord("y"):
            eye.crop.left += 1
        elif key == ord("h"):
            eye.crop.left = max(0, eye.crop.left - 1)
        elif key == ord("u"):
            eye.crop.bottom += 1
        elif key == ord("j"):
            eye.crop.bottom = max(0, eye.crop.bottom - 1)
        else:
            return
        self.config.save()

    def run(self) -> None:
        cv2.namedWindow("VisionPi", cv2.WINDOW_NORMAL)

        running = True
        while running:
            frame = self.cameras.compose(self.camera_name)
            frame = apply_display_settings(frame, self.config.display)

            event = self.gestures.update(frame)
            if event is not None:
                self.cursor_xy = event.cursor_xy
                self.pinched = event.pinch_active
                self.debounce_remaining_s = event.debounce_remaining_s
                self.menu.update_hover(self.cursor_xy)
                if event.pinch_confirmed:
                    running, _, selection = self.menu.confirm()
                    self._apply_selection(selection)

            breadcrumb = self.menu.breadcrumb()
            items = self.menu.current_items()
            active_index = self.menu.active_root_index if not self.menu.in_submenu else self.menu.active_sub_index

            render_menu(
                frame,
                breadcrumb,
                items,
                active_index,
                pinch_active=self.pinched,
                debounce_remaining_s=self.debounce_remaining_s,
            )

            if self.calibration_mode:
                msg = f"CAL {self.calibration_eye.upper()} | WASD offset | [] scale | ,. rot | M mirror | E eye"
                cv2.putText(frame, msg, (20, 415), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 210, 120), 1)

            if self.last_action_message:
                cv2.putText(frame, self.last_action_message, (20, 440), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (180, 220, 255), 1)

            self.status.update_fps()
            collar_status = self.collar.get_status()
            collar_battery = "--" if collar_status.battery_percent is None else f"{collar_status.battery_percent}%"
            status_snapshot = self.status.snapshot(
                self.camera_name,
                collar_state=collar_status.state,
                collar_battery=collar_battery,
            )
            render_status_bar(frame, status_snapshot, self.width, self.height)
            render_cursor(frame, self.cursor_xy, self.pinched)

            cv2.imshow("VisionPi", frame)
            key = cv2.waitKey(1) & 0xFF
            if key in (27, ord("q")):
                break
            self._handle_calibration_key(key)

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
