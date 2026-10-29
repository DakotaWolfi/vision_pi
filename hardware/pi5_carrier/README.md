# VisionPi — Pi 5 carrier plate (prototype)

Parametric OpenSCAD mounting plate for a Raspberry Pi 5, the 12 V to 5 V DC-DC converter, and the HDMI-to-USB-C (DP Alt Mode) adapter used with the VISION MINI goggles.

## Arrangement

- Pi 5 at the front-left; USB/Ethernet connector edge points right (+X).
- HDMI-to-USB-C adapter in a low cradle to the **right of the Pi**, close to its USB connector edge. Two pairs of slots accept zip ties. Keep the converter's HDMI and USB-C ends unobstructed.
- DC-DC converter behind the Pi. Because its exact board dimensions and hole pattern were not provided, its default retention is **two zip ties**. Optional four-post screw mounting can be enabled after measuring it.
- Four raised Pi 5 mounting posts using the standard 58 x 49 mm pitch, with M2.5 clearance bores.
- Four elongated plate-to-frame mounting slots.

## Before printing

Open `pi5_carrier.scad` in OpenSCAD and adjust:

- `dc_board`, `dc_origin`, `dc_hole_pitch`, `dc_hole_offset`: measure your actual DC-DC board. Set `dc_screw_mounts = true` only after confirming mounting-hole coordinates. Otherwise use zip ties, with electrical insulation beneath the module.
- `adapter_body`, `adapter_origin`, `adapter_zip_positions`: measure the actual HDMI/USB-C adapter's body and its cable-end clearance.
- `plate_width`, `plate_depth`: check fit inside the headset/assembly.
- `pi_post_height`, screw clearances: check Pi underside component clearance, cooling, and your fasteners.

The adapter and DC-DC module dimensions supplied in the SCAD are **placeholders, not verified measurements**. In particular, the adapter's stop rail may need removing if it blocks an HDMI connector.

Render with **F6**, then export STL. Print a fit-check before committing to permanent mounting.

## Safety / wiring

Keep the Pi's underside above the plate and avoid contact between exposed converter pads and conductive items. Provide strain relief on HDMI, USB-C and power leads. Do not cover the Pi fan/heatsink or block converter cooling. The printed plate is a mechanical carrier, not an electrical enclosure or qualified high-temperature mount.
