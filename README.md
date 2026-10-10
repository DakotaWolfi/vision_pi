# VisionPi

VisionPi is a modular stereo-vision HUD runtime for Raspberry Pi 5 with:

- Dual IMX708 Wide camera support (left/right stereo)
- PSVR1-oriented dual-eye display composition
- MediaPipe hand tracking (normal human hand model)
- Index-finger cursor + pinch-to-click UI interaction
- WiFi Remote Eye source support
- System telemetry HUD bar (CPU temp, fan RPM when available, FPS, WiFi, power)
- CollarPet integration via a dedicated client boundary (no CollarPet merge)

## Installation

1. Install system packages on Raspberry Pi OS (example baseline):

```bash
sudo apt update
sudo apt install -y python3-pip python3-opencv python3-picamera2
```

2. Install Python dependencies:

```bash
pip3 install -r requirements.txt
```

## Run

Run the modular app directly:

```bash
python3 -m visionpi
```

Optional WiFi eye endpoints:

```bash
python3 -m visionpi --wifi-eye-1 http://192.168.1.101:8080/video --wifi-eye-2 http://192.168.1.102:8080/video
```

Optional CollarPet endpoint marker (protocol currently stubbed):

```bash
export COLLARPET_ENDPOINT=http://collarpet.local:9000
python3 -m visionpi
```

## Architecture

```text
visionpi/
├─ app.py                    Runtime loop and module orchestration
├─ config.py                 Persistent display/calibration configuration
├─ cameras/
│  ├─ sources.py             Pi CSI, WiFi, and fallback mock sources
│  └─ manager.py             Source selection + stereo composition
├─ menu/
│  ├─ model.py               Hierarchical VISION menu tree
│  ├─ gestures.py            MediaPipe fingertip + pinch debounce
│  └─ controller.py          Hover, select, back navigation, breadcrumb state
├─ display/
│  ├─ renderer.py            HUD/menu/status/cursor drawing
│  └─ calibration.py         Per-eye transforms + display post-processing
├─ system/
│  ├─ thermal.py             CPU temp from sysfs/vcgencmd fallback
│  ├─ fan.py                 fan1_input discovery from hwmon
│  ├─ wifi.py                WiFi connection summary
│  ├─ power.py               Power/battery summary
│  └─ status.py              Telemetry aggregation + FPS
└─ collar/
	└─ collar_client.py       CollarPet client/interface layer (stub-safe)
```

Known-good prototype baseline scripts are kept in `tools/` while module behavior is verified incrementally.

## Controls

- Cursor: index fingertip position from MediaPipe
- Select: pinch (thumb + index) with debounce confirmation
- Hover: menu item under cursor is highlighted
- Back: select `< Back` inside submenu
- Exit: select `EXIT` in root menu
- Quit app: `q` or `Esc`

Display menu actions:

- `Zoom`: cycles zoom preset
- `Brightness`: cycles brightness preset
- `Night Mode`: toggles green-channel night rendering
- `Calibration`: toggles calibration mode

Calibration mode keys:

- `E`: switch eye (left/right)
- `W/A/S/D`: Y/X offset
- `[` and `]`: scale down/up
- `,` and `.`: rotation
- `M`: mirror toggle
- `Y/H`, `T/G`, `R/F`, `U/J`: left/top/right/bottom crop +/-

Calibration is stored at:

```text
~/.config/visionpi/config.json
```

## Current limitations

- CollarPet protocol methods are intentionally stubbed until protocol details are finalized.
- WiFi Eye source assumes OpenCV-compatible stream URLs.
- Fan RPM only appears when a readable `fan1_input` exists in hwmon.
- Final PSVR optical tuning still depends on physical mounting and per-user calibration.

## Repository layout

```text
.
├─ docs/
├─ tests/
├─ tools/                    Prototype and diagnostics scripts
├─ visionpi/                 Modular runtime package
├─ main.py                   Compatibility launcher
├─ requirements.txt
└─ MIGRATION.md
```

## License

MIT
