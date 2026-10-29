# Pi 5 dual-camera FPS experiment (standalone)

The existing app (`python3 -m visionpi`) and all existing scripts are **unchanged**. Use the new `tools/pi5_stereo_fps_test.py` to measure camera delivery and OpenCV SBS display in isolation.

## Requirements

Raspberry Pi 5, Raspberry Pi OS, two recognized IMX708 Wide cameras, Python 3, Picamera2, NumPy and OpenCV. Run in the graphical desktop session, with `DISPLAY` available. The script opens cameras **0 and 1** exclusively; close other software using them.

## Try

```bash
git pull
python3 tools/pi5_stereo_fps_test.py --width 1280 --height 720 --fps 60 --fullscreen
```

The **capture** dimensions are per camera. The default displayed SBS canvas is 1920×1080, not the headset's full physical 3840×1080 output. For native headset-size experiments:

```bash
python3 tools/pi5_stereo_fps_test.py --width 1280 --height 720 --fps 60 \
    --display-width 3840 --display-height 1080 --fullscreen
```

For a lighter capture/display experiment:

```bash
python3 tools/pi5_stereo_fps_test.py --width 960 --height 540 --fps 60 \
    --display-width 1920 --display-height 1080
```

For camera-only troubleshooting:

```bash
python3 tools/pi5_stereo_fps_test.py --single --width 1280 --height 720 --fps 30
```

Use **Q/Esc** to exit and **F** to toggle fullscreen. `--seconds 30` auto-stops after 30 seconds; `--no-overlay` disables text rendering.

## Reading results

Every two seconds the terminal prints **per-camera producer FPS**, **OpenCV display-loop FPS**, and **age of the most recently captured frame**. The camera threads replace old frames without building a Python backlog. These are **host-side FPS/age approximations**, not sensor-to-photon latency, real eye synchronization or HDMI display refresh measurements. 60 FPS is a *request*: actual sensor mode and performance can differ. If a capture mode is unsupported, Picamera2 may choose a different mode or fail to start; check `rpicam-hello --list-cameras` and retest another resolution/fps.

If display FPS is low but capture FPS stays high, try 1920×1080 instead of 3840×1080 SBS and turn off the overlay. If both capture FPS values are low, check sensor mode and CPU thermal/load before changing renderer code.

### Fallback

The known baseline is untouched:

```bash
python3 -m visionpi
```

No per-user config, calibration or OS settings are modified by the FPS test.
