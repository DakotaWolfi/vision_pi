#!/usr/bin/env python3
"""Standalone Pi 5 stereo latency/FPS experiment; does not alter VisionPi runtime.

Run from desktop session:
    python3 tools/pi5_stereo_fps_test.py --width 1280 --height 720 --fps 60
    python3 tools/pi5_stereo_fps_test.py --width 960 --height 540 --fps 60

Both cameras run in independent producer threads; the display always reads the
newest frame, never a queue of old frames. Actual FPS depends on sensor modes.
"""
from __future__ import annotations

import argparse
import threading
import time
from dataclasses import dataclass

import cv2
import numpy as np

try:
    from picamera2 import Picamera2
except ImportError:
    raise SystemExit("Picamera2 not installed: sudo apt install python3-picamera2")


@dataclass
class Sample:
    frame: np.ndarray | None = None
    timestamp: float = 0.0
    sequence: int = 0
    error: str = ""


class LatestCamera:
    def __init__(self, index: int, size: tuple[int, int], fps: int, buffers: int):
        self.index = index
        self.camera = Picamera2(index)
        # RGB888 buffers are BGR-ordered when interpreted by OpenCV.
        config = self.camera.create_preview_configuration(
            main={"size": size, "format": "RGB888"},
            buffer_count=buffers,
            queue=False,
            controls={"FrameDurationLimits": (round(1_000_000 / fps), round(1_000_000 / fps))},
        )
        self.camera.configure(config)
        self.lock = threading.Lock()
        self.sample = Sample()
        self.stop_flag = threading.Event()
        self.thread = threading.Thread(target=self._capture, name=f"CSI-{index}", daemon=True)

    def start(self):
        self.camera.start()
        self.thread.start()

    def _capture(self):
        try:
            while not self.stop_flag.is_set():
                # capture_array returns a separate frame; producer owns it until
                # replaced. Main thread reads the same immutable frame reference.
                frame = self.camera.capture_array("main")
                now = time.monotonic()
                with self.lock:
                    self.sample = Sample(frame, now, self.sample.sequence + 1)
        except Exception as exc:
            with self.lock:
                self.sample.error = f"{type(exc).__name__}: {exc}"

    def latest(self):
        with self.lock:
            s = self.sample
            return Sample(s.frame, s.timestamp, s.sequence, s.error)

    def close(self):
        self.stop_flag.set()
        # Camera stop can release a pending capture; avoid closing from two threads.
        try:
            self.camera.stop()
        except Exception:
            pass
        self.thread.join(timeout=2)
        self.camera.close()


def args_parse():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--width", type=int, default=1280, help="Per-camera capture width")
    p.add_argument("--height", type=int, default=720, help="Per-camera capture height")
    p.add_argument("--fps", type=int, default=60, help="Requested capture FPS, not guaranteed")
    p.add_argument("--buffers", type=int, default=3, help="Camera buffer count (2-6 recommended)")
    p.add_argument("--display-width", type=int, default=1920, help="Composited window width")
    p.add_argument("--display-height", type=int, default=1080, help="Composited window height")
    p.add_argument("--fullscreen", action="store_true")
    p.add_argument("--single", action="store_true", help="Use camera 0 duplicated to both eyes")
    p.add_argument("--no-overlay", action="store_true", help="Disable performance text")
    p.add_argument("--seconds", type=float, default=0, help="Auto-quit after N seconds, 0=manual")
    args = p.parse_args()
    if min(args.width, args.height, args.fps, args.buffers, args.display_width, args.display_height) <= 0:
        p.error("Resolution, FPS and buffer count must be positive")
    return args


def main():
    args = args_parse()
    cv2.setNumThreads(2)
    cameras = []
    try:
        for index in range(1 if args.single else 2):
            camera = LatestCamera(index, (args.width, args.height), args.fps, args.buffers)
            cameras.append(camera)
        for camera in cameras:
            camera.start()

        cv2.namedWindow("VisionPi FPS TEST", cv2.WINDOW_NORMAL)
        if args.fullscreen:
            cv2.setWindowProperty("VisionPi FPS TEST", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        half = (args.display_width // 2, args.display_height)
        last_sequences = [0] * len(cameras)
        capture_counts = [0] * len(cameras)
        display_count = 0
        last_stats = time.monotonic()
        start = last_stats
        capture_fps = [0.0] * len(cameras)
        display_fps = 0.0
        no_frame = np.zeros((args.height, args.width, 3), dtype=np.uint8)
        print("Controls: Q/Esc quit; F toggle fullscreen")
        print("Capture resolution:", args.width, "x", args.height, "@ requested", args.fps, "FPS")

        while True:
            now = time.monotonic()
            samples = [camera.latest() for camera in cameras]
            for i, sample in enumerate(samples):
                if sample.error:
                    raise RuntimeError(f"Camera {i}: {sample.error}")
                if sample.sequence != last_sequences[i]:
                    capture_counts[i] += sample.sequence - last_sequences[i]
                    last_sequences[i] = sample.sequence

            # No queue: repeat most recent image if capture hasn't updated.
            left = samples[0].frame if samples[0].frame is not None else no_frame
            right = (samples[0].frame if args.single else samples[1].frame)
            if right is None:
                right = no_frame
            left_eye = cv2.resize(left, half, interpolation=cv2.INTER_LINEAR)
            right_eye = cv2.resize(right, half, interpolation=cv2.INTER_LINEAR)
            # Concatenation copies once; main VisionPi pipeline may copy more.
            output = np.concatenate((left_eye, right_eye), axis=1)
            display_count += 1

            if now - last_stats >= 2.0:
                elapsed = now - last_stats
                capture_fps = [count / elapsed for count in capture_counts]
                display_fps = display_count / elapsed
                capture_counts = [0] * len(cameras)
                display_count = 0
                last_stats = now
                ages = [round((now - s.timestamp) * 1000) if s.timestamp else None for s in samples]
                print(f"Capture FPS: {[round(x,1) for x in capture_fps]} | Display FPS: {display_fps:.1f} | newest frame age ms: {ages}", flush=True)

            if not args.no_overlay:
                left_age = (now - samples[0].timestamp) * 1000 if samples[0].timestamp else -1
                right_s = samples[0] if args.single else samples[1]
                right_age = (now - right_s.timestamp) * 1000 if right_s.timestamp else -1
                cv2.putText(output,
                            f"L {capture_fps[0]:.1f} fps age {left_age:.0f}ms | R {capture_fps[-1]:.1f} fps age {right_age:.0f}ms | display {display_fps:.1f}",
                            (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            cv2.imshow("VisionPi FPS TEST", output)
            key = cv2.waitKey(1) & 0xFF
            if key in (ord("q"), 27):
                break
            if key == ord("f"):
                current = cv2.getWindowProperty("VisionPi FPS TEST", cv2.WND_PROP_FULLSCREEN)
                cv2.setWindowProperty("VisionPi FPS TEST", cv2.WND_PROP_FULLSCREEN,
                                      cv2.WINDOW_NORMAL if current == cv2.WINDOW_FULLSCREEN else cv2.WINDOW_FULLSCREEN)
            if args.seconds and now - start >= args.seconds:
                break
    finally:
        for camera in reversed(cameras):
            camera.close()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
