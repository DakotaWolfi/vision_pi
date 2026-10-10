from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Dict


@dataclass
class Crop:
    left: int = 0
    top: int = 0
    right: int = 0
    bottom: int = 0


@dataclass
class EyeCalibration:
    offset_x: int = 0
    offset_y: int = 0
    scale: float = 1.0
    rotation_deg: float = 0.0
    mirror: bool = False
    crop: Crop = field(default_factory=Crop)


@dataclass
class DisplaySettings:
    zoom: float = 1.0
    brightness: float = 1.0
    night_mode: bool = False


@dataclass
class AppConfig:
    display: DisplaySettings = field(default_factory=DisplaySettings)
    calibration: Dict[str, EyeCalibration] = field(
        default_factory=lambda: {"left": EyeCalibration(), "right": EyeCalibration()}
    )

    @staticmethod
    def path() -> Path:
        return Path.home() / ".config" / "visionpi" / "config.json"

    @classmethod
    def load(cls) -> "AppConfig":
        cfg = cls()
        path = cls.path()
        if not path.exists():
            return cfg
        try:
            raw = json.loads(path.read_text())
        except Exception:
            return cfg

        display = raw.get("display", {})
        cfg.display.zoom = float(display.get("zoom", cfg.display.zoom))
        cfg.display.brightness = float(display.get("brightness", cfg.display.brightness))
        cfg.display.night_mode = bool(display.get("night_mode", cfg.display.night_mode))

        calibration = raw.get("calibration", {})
        for eye_name in ("left", "right"):
            eye_raw = calibration.get(eye_name, {})
            eye = cfg.calibration[eye_name]
            eye.offset_x = int(eye_raw.get("offset_x", eye.offset_x))
            eye.offset_y = int(eye_raw.get("offset_y", eye.offset_y))
            eye.scale = float(eye_raw.get("scale", eye.scale))
            eye.rotation_deg = float(eye_raw.get("rotation_deg", eye.rotation_deg))
            eye.mirror = bool(eye_raw.get("mirror", eye.mirror))
            crop_raw = eye_raw.get("crop", {})
            eye.crop.left = int(crop_raw.get("left", eye.crop.left))
            eye.crop.top = int(crop_raw.get("top", eye.crop.top))
            eye.crop.right = int(crop_raw.get("right", eye.crop.right))
            eye.crop.bottom = int(crop_raw.get("bottom", eye.crop.bottom))

        return cfg

    def save(self) -> None:
        path = self.path()
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "display": asdict(self.display),
            "calibration": {name: asdict(cal) for name, cal in self.calibration.items()},
        }
        path.write_text(json.dumps(payload, indent=2))
