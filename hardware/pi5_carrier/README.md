# VisionPi — Pi 5 carrier plate (prototype)

Parametric OpenSCAD mounting plate for a Raspberry Pi 5, the 12 V to 5 V DC-DC converter, and the HDMI-to-USB-C (DP Alt Mode) adapter used with the VISION MINI goggles.

## Arrangement

- Pi 5 at the front-left; USB/Ethernet connector edge points right (+X).
- HDMI-to-USB-C adapter in a low cradle **beside the DC-DC module, behind/above the Pi**, away from the Pi USB/Ethernet connector edge. Housing is **60 × 32 mm** according to the product diagram; thickness remains unknown. Two pairs of slots accept zip ties. **Both connector ends are open** for short/slim 90° HDMI adapters and a possible right-angle USB-C lead.
- DC-DC converter behind the Pi. Product listing shows **59 × 44 mm overall**, with a **55 × 40 mm PCB-like interior** and about **22 mm overall height including fan**. Four screw posts are enabled, using a **provisional 48 × 33 mm M2.5 CM4-style hole pitch**; check actual hole centers before printing. Alternative zip-tie slots are included.
- Four raised Pi 5 mounting posts using the standard 58 x 49 mm pitch, with M2.5 clearance bores.
- Four elongated plate-to-frame mounting slots.

## Before printing

Open `pi5_carrier.scad` in OpenSCAD and adjust:

- `dc_board`, `dc_origin`, `dc_hole_pitch`, `dc_hole_offset`: verify the power module's actual screw-hole pitch. CM4 has a 55 × 40 mm PCB with hole centers inset 3.5 mm (48 × 33 mm pitch), but the photographed power-board **outer envelope is 59 × 44 mm**. The same hole pattern on the DC-DC module is an assumption, not yet measured. Set `dc_screw_mounts = false` if it differs; zip-tie slots remain available.
- `adapter_body = [60,32]` is based on the ULT-unite photo. Check adapter thickness, rounded corners, cable-end clearances, and zip-tie fit.
- `plate_width`, `plate_depth`: check fit inside the headset/assembly.
- `pi_post_height`, screw clearances: check Pi underside component clearance, cooling, and your fasteners.

The converter and adapter **overall dimensions are sourced from the product photos**, not independently measured. Their thickness, true mounting-hole positions, and clearance for connectors still require a physical fit-check. In particular, the adapter's stop rail may need removing if it blocks an HDMI connector.

Render with **F6**, then export STL. Print a fit-check before committing to permanent mounting.

## Safety / wiring

Keep the Pi's underside above the plate and avoid contact between exposed converter pads and conductive items. Provide strain relief on HDMI, USB-C and power leads. Do not cover the Pi fan/heatsink or block converter cooling. The printed plate is a mechanical carrier, not an electrical enclosure or qualified high-temperature mount.

## Cable routing (revision)

- Keep the Pi's micro-HDMI exits accessible for slim 90° adapters. Check the actual direction of the angled plugs: left-hand and right-hand variants can route in opposite directions.
- The HDMI-to-USB-C adapter now sits beside the power converter, rather than directly beside the Pi's USB/Ethernet stack. Its HDMI and USB-C connector faces have no printed end stop.
- Leave a bend-radius and unplugging allowance for the Pi's power USB-C cable, the power converter's DC input, the HDMI adapter's USB-C output cable to the goggles, and any USB peripherals. Optional right-angle USB-C plugs must be checked for orientation and current rating.
- CAD positions are still an early prototype. Check actual Pi connector orientation and cable interference with a printed fit test; neither connector clearance nor cable strain relief is guaranteed by the 2D board dimensions alone.

## Lightweight patterned plate (new)

The carrier now defaults to an open **hexagonal cutout pattern** rather than a fully solid sheet. Edit at the top of `pi5_carrier.scad`:

- `plate_pattern = "hex"` for hexagonal apertures, `"round"` for circles, or `"solid"` for the original uninterrupted plate.
- `pattern_hole_diameter = 13` mm and `pattern_pitch_x = 20` / `pattern_pitch_y = 18` mm for density.
- `pattern_edge_margin = 10` mm for a continuous perimeter.

Holes are skipped near the Pi 5 and provisional DC-DC mounting posts, the HDMI-to-USB-C converter cradle and zip-tie slots, DC-DC tie slots, and frame mounts. This is a **lightening pattern**, not a validated structural optimization: check the printed plate's stiffness, material, and fit. Save a solid STL as a fallback if needed.
