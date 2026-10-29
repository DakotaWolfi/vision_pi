# Vision Paw v0.2 — organic hand-back TPU glove carrier

**Replaces the crude v0.1 rectangular sheet.** This is a dimension-driven, curved-in-use glove *shell*, not a fully enclosed fabric glove and not a scan of your hand. It has a tapered wrist, rounded knuckle crown, asymmetric thumb/index wing, TPU flex cuts, a central PETG electronics cartridge, a smaller PETG joystick cartridge, and two optional PCL reinforcement lanes.

Source: [vision_paw_flat.scad](vision_paw_flat.scad)

## OpenSCAD controls

All user-editable parameters are now at the **top** of the file, grouped for the OpenSCAD Customizer:
- **Output**: `part = "glove_tpu" | "electronics_petg" | "joystick_petg" | "rail_test" | "assembly"`, and `hand = "right" | "left"`.
- **Hand dimensions**: `knuckle_width`, `wrist_width`, `palm_length`, `thumb_wing`, `deck_width`.
- **TPU geometry**: `base_thickness`, `flex_bridge_width`, `strap_slot_width`, `strap_width`, `rail_clearance`.
- **PCL ribs**: `pcl_diameter`, `pcl_channel_length`, `pcl_channel_spacing`.
- **PETG insert**: `deck_length`, `deck_thickness`, and generic mounting-hole values.

Units are **millimetres**, with adult-hand placeholder defaults. These are NOT custom measurements of your hand. No tape is needed just to print a fitting sample; measure with a ruler and string later.

## Parts / layout

- TPU glove: flat silhouette, approximately 1.6 mm thick in flexible areas, wrist/knuckle strap openings, and isolated flex slits.
- PETG electronics deck: nominal 39 × 42 mm central removable cartridge. **Generic 26 × 32 mm M2 holes only**; these are *not* verified footprints of the real OLED, ESP32-S3, LRA board or battery.
- PETG joystick deck: nominal 24 × 24 mm removable blank with cable hole, on an asymmetric thumb/index wing. No actual Hall joystick pin/fastener geometry yet.
- PCL: two short, noncontinuous reinforcement lanes outside the central cartridge. The moldable rods supply optional residual curvature, leaving wrist/knuckle flex zones unreinforced.

## Print / assembly

Set `part="glove_tpu"` and render with **F6** and export STL. Repeat for the two PETG parts. First print `part="rail_test"` to check flexible rail clearance. Print TPU flat on the bed; use PETG for inserts. Strap material and PCL rods are separate, not printable as part of the STL. The PCL rails are intended to retain preformed, cooled rods; a real test may require changes to retention.

**Prototype status:** The OpenSCAD source has been committed but **has not yet been successfully rendered/physically fit-tested**. Confirm that F6 generates a valid manifold model before printing, and check the fit with no electronics. Do not mistake the simple PCB holes for finished component mounts.

The next iteration should use actual hand dimensions, PCB measurements and real joystick reach. Form-fitting PCL inserts should be shaped away from skin until cooled to a comfortable temperature; the electronics should be detached during any heat forming.
