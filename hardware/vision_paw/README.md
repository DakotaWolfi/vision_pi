# Vision Paw — glove-mounted BLE remote

Vision Paw belongs to the VisionPi project. This directory records the existing hardware and firmware design for the ESP32-S3 glove controller.

**Source status:** The original Arduino firmware was previously packaged as `VisionRemote_v0_4.zip`, then `VisionRemote_v0_4_1.zip` (added `VisionVectors.h` to resolve Arduino auto-prototype problems). Those ZIP contents have **not been recovered here**, so this directory does **not** claim to contain the working firmware. Import the original archive before editing or flashing it. The previous version was not hardware-verified/compiled in the user's toolchain.

## Hardware

- **MCU:** ESP32-S3 Super Mini (4 MB flash), USB-powered while prototyping; integrated battery charging considered.
- **IMU:** BMI160 preferred; MPU6050 alternative/prototype detection in firmware.
- **Haptics:** DRV2605L with ALPS LRA.
- **Joystick:** Joy-Con-style Hall-effect thumbstick; be careful to match the exact 5-pin flex connector variant.
- **Display:** SSD1306 0.96-inch I²C monochrome OLED.
- **Status:** onboard addressable NeoPixel.
- **Mounting:** board on back of hand/paw, joystick toward index finger; later 3D-scanned shell/TPU or silicone glove mount.

**Pin numbers and complete wiring diagram are not yet recovered**. Do not treat the above as a finalized schematic; confirm sensor addresses, shared I²C bus, battery/charger wiring and the analog joystick pins before assembly.

## Existing v0.4 behavior (as previously discussed)

OLED compact status screen:
- `VISION PAW v0.4`
- BLE: connected / pairing / advertising
- Mode: gyro / joystick
- IMU and LRA presence
- Joystick ADC values
- Gyro X/Y and roll angle estimate

Control ideas and requested refinements:
- BLE HID mouse + keyboard/joystick behavior.
- IMU-driven cursor motion with a clutch, and adjustable acceleration; wrist rotation around 90° should preserve intuitive movement.
- Joystick navigation and trigger/click behavior. Modes GYRO and JOYSTICK.
- Guided serial calibration: gyro bias/axis orientation, wrist twist, joystick direction and center/endpoints.
- Joystick/button long press for pairing or mode operations; calibration at boot.
- LRA haptic feedback for important UI actions.
- Earlier experimental mapping: joystick for navigation/select; A-held IMU mouse clutch; A+B right-click; A+joystick press drag. This was a *design proposal*, not a guarantee that firmware v0.4.1 implements it.
- The design should communicate with VisionPi; BLE HID support currently targets standard host input. A dedicated VisionPi protocol is future work.

## Recovery/build notes

Previous compile diagnostics referenced Arduino ESP32 core **3.3.7**, ESP32-S3 board, **4 MB flash**, PSRAM disabled; libraries included:
- Wire, Preferences, Adafruit GFX, Adafruit SSD1306, Adafruit DRV2605, Adafruit NeoPixel
- NimBLE-Arduino and a `HijelHID_BLEMouse` library

These are **historical observed dependencies**, not a validated manifest. Verify library versions and actual includes from the original sketch once imported.

The last known packaged source was `VisionRemote_v0_4_1.zip`, including `VisionVectors.h` to work around auto-generated function prototype ordering. Do not replace that with untested reconstructed code.

## Next physical steps

1. Restore the original `VisionRemote_v0_4_1` sketch and header files to `hardware/vision_paw/firmware/`.
2. Verify real schematic and pin mappings; document the 5-pin joystick FPC pinout based on the actual module.
3. Test basic I²C OLED/IMU/LRA and BLE pairing separately.
4. Build a scan-derived glove shell with serviceable mounting for electronics and vibration isolation where appropriate.
5. Integrate with the main VisionPi app after baseline HID mouse operation is stable.
