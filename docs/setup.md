# Setup

This file intentionally starts minimal. Capture the commands from the current
working Pi before rebuilding the environment from scratch.

Recommended first step on the Pi:

```bash
python3 --version
pip list --format=freeze > current-python-packages.txt
```

Also record the packages installed through apt that are required for Picamera2,
OpenCV, PSVR support and MediaPipe.
