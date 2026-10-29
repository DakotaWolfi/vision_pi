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

## Compact layout (90° adapter)

Set `layout_variant = "compact"` (the new default) to use a **160 × 124 mm** plate instead of 198 × 124 mm. The Pi 5 remains at the lower-left; DC-DC stays above it; the 60 × 32 mm HDMI-to-USB-C adapter is rotated to a **32 × 60 mm** footprint at approximately X=112, Y=49. The cradle rails and zip-tie slots rotate with it. The adapter keepout for the lightweight hex/round pattern uses the rotated footprint.

Set `layout_variant = "wide"` to restore the original 198 × 124 mm landscape layout, horizontally mounted adapter and original clearances. This retains both versions in the *same* editable OpenSCAD file.

**Fit checks before printing:** confirm the adapter's true connector direction and room for the 90° micro-HDMI leads; the power module mounting pitch is still provisional. The compact geometry has not been physically test-fitted.

## Stacked layout from physical component photo (new default)

The new `layout_variant = "stacked"` uses a **112 × 178 mm** plate, arranging the components along its long axis: **DC-DC at [15,10]**, **HDMI-to-USB-C body at [29,69]** and **Pi 5 at [12,109]** (all coordinates are the lower-left corners, in mm). The Pi 5 USB-A/Ethernet connector edge points toward **+X/right**, outside the electronics footprint. The HDMI adapter is horizontal here, matching the photo arrangement; the earlier `compact` (rotated adapter) and `wide` versions are still selectable. The DC-DC board has approximately 15 mm to the HDMI adapter's body and the Pi board starts 8 mm after the HDMI body's far edge. Check actual cable connector protrusion and thickness before printing.

The plate keeps patterned hex/round holes while reserving solid mount regions. The power board's M2.5 hole pitch remains a *provisional inferred* 48 × 33 mm; verify physically.

## Standoff settings and heat-set threaded inserts

- `pi_post_diameter` and `dc_post_diameter`: adjust boss outside diameters separately (defaults 8 mm).
- `pi_post_height` and `dc_post_height`: independent standoff heights (defaults 7 and 6 mm).
- `pi_heat_inserts` and `dc_heat_inserts`: independent toggles (default **false** for both).
- `pi_insert_pilot_diameter` and `dc_insert_pilot_diameter` (default 3.5 mm), and `pi_insert_depth` / `dc_insert_depth` (default 4 mm), define the **blind top-side insert pockets**.
- Standard screw mode instead uses a through-hole shaft. Printed boss geometry enforces a minimum 1.2 mm radial wall around the insert pocket and requires pilot depth less than boss height.

**Verify with your actual inserts:** M2.5 brass heat-set insert brands need different pilot diameters, depths and installation tolerances. Measure one and print a standalone test boss before committing to the whole carrier. For heat-set mode the blind pocket is intentionally closed by the base plate.

**Verification state:** GitHub source was updated, but full OpenSCAD render/export in the current environment could not be completed. This is a layout prototype, not a tested print.

## HDMI adapter tall retaining walls

The adapter now has a **separate edge-on wall configuration**, with the following editable values in `pi5_carrier.scad`:

```scad
adapter_wall_height = 20;
adapter_wall_inner_gap = 16;
adapter_wall_thickness = 2.6;
adapter_wall_offset = 0;
adapter_wall_along_offset = 0;
adapter_wall_length = 42;
```

The wall spacing is the **16 mm clear opening between the two inner faces**, not the adapter's 60 × 32 mm face width. The adapter is assumed to be mounted on its narrow edge between the rails. The shell thickness has not been independently measured, so verify the actual orientation and clearance on hardware. The walls follow the `layout_variant` rotation, and the hexagonal cutout keepout follows their adjustable position. Both connector ends remain open for wiring and zip-tie fastening.

## Right-angle HDMI plug clearance

`pi_hdmi_clearance = 11;` reserves an adjustable 11 mm **plan-view gap between the Pi PCB lower edge and the HDMI converter body** in the `stacked` layout. If the original placement is too close, the HDMI adapter cradle, its wall positions, and zip-tie slots all shift together automatically. With the current values the adapter moves 3 mm toward the DC-DC board (from Y=69 to Y=66). This clearance is measured to the board outline rather than the exact HDMI socket/plug protrusion; verify the real orientation and connector envelope in OpenSCAD and on a fit-check before printing. The other layout variants are unchanged.
