# VisionPi

Wearable stereo-vision / HUD platform for Raspberry Pi 5.

Current project goals:

- Dual Raspberry Pi Camera Module 3 Wide / IMX708 support
- PSVR1 stereo display output
- MediaPipe hand tracking and gesture-controlled HUD
- Wi-Fi Remote Eye camera support
- System thermal / fan / FPS / power telemetry
- CollarPet integration through a clean client interface

## Repository layout

```text
.
├─ docs/                  Hardware, setup and architecture notes
├─ visionpi/              Main Python package
│  ├─ cameras/            CSI, stereo and Wi-Fi eye support
│  ├─ collar/             CollarPet client/interface
│  ├─ display/            PSVR and HUD rendering
│  ├─ menu/               Menu, widgets and gesture handling
│  └─ system/             Temperature, fan and system status
├─ tools/                 Known-good experiments and diagnostics
├─ tests/                 Future tests
├─ main.py                Main launcher placeholder
├─ requirements.txt
└─ MIGRATION.md           Where to move existing prototype scripts
```

## Status

This repository starts as a clean scaffold. Move the current known-good prototype scripts into `tools/` first, commit them unchanged, and only then refactor them into `visionpi/` modules.

## Platform

Target: Raspberry Pi 5, 64-bit Raspberry Pi OS.

## License

MIT, unless you decide to use another license before publishing.
