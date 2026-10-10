# Prototype migration plan

Do **not** refactor the working prototype immediately.

1. Copy the current known-good scripts into `tools/` unchanged.
2. Make an initial commit so there is always a working reference.
3. Move reusable pieces into the package gradually.

Suggested mapping:

| Existing prototype | Temporary destination | Eventual module |
|---|---|---|
| Current stereo / PSVR viewer | `tools/vision_menu_prototype.py` | `visionpi/display/` + `visionpi/cameras/` |
| Remote Eye viewer | `tools/remote_eye.py` | `visionpi/cameras/wifi_eye.py` |
| Camera tests | `tools/` | `visionpi/cameras/` |
| Hand tracking experiments | `tools/` | `visionpi/menu/gestures.py` |
| Thermal / fan checks | `tools/` | `visionpi/system/` |

CollarPet itself stays in its own repository. VisionPi talks to it through `visionpi/collar/collar_client.py`.
