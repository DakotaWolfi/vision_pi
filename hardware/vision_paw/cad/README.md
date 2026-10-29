# Vision Paw: flat TPU carrier + removable PETG deck + PCL stiffeners (v0.1)

This is an **experimental printable parametric prototype**, not a body-fitted or field-validated glove.

The source `vision_paw_flat.scad` renders a flat, flexible **TPU hand-back carrier** with wrist/knuckle strap slots, open PCL rod lanes and side rails for a separate **PETG electronics cartridge**. The PCL stiffeners run along selected areas instead of covering the full shell, so the wrist and knuckle regions can still flex.

## OpenSCAD / export

Change `part` at the top of the file to `"tpu"` or `"petg"`; press **F6**, then **File > Export > STL**. The `"all"` value shows both parts separated on the print bed. `"test"` exports a small rail-fit section.

Parameters in millimetres: `hand_width`, `hand_length`, `wrist_width`, `knuckle_width`, `shell_thickness`, `pcl_rod_diameter`, `pcl_lane_offset`, `pcl_lane_length`, `cartridge_width`, `cartridge_length`, `cartridge_clearance`, `strap_width`.

**Dimension caveats:** The initial hand dimensions are placeholders. The 34 × 42 mm PETG deck is a generic interface and **does not yet match the actual ESP32-S3, SSD1306, DRV2605L or joystick screw pattern**. Those need measurement. The first version has no dedicated joystick pod; design that after measuring hand fit and preferred joystick reach.

## Material choices

- Print the sheet / retaining rails **flat on the build plate** in TPU (e.g. 95A); no supports expected for the basic shape.
- Print cartridge separately in PETG; mechanical fit is adjustable via `cartridge_clearance`.
- Shape ~3.5 mm-diameter **Whitemorph/PCL rods separately**, cooling them until safe to handle, then insert into the open retaining channels on the TPU. TPU channels are intentionally open, with no enclosed tube that would trap a soft insert. If rods escape during bending, use small TPU retainers or elastic thread across channels; this iteration tests geometry first.
- The PCL stiffeners should be **removable/remoldable**. Do not assume PCL will not bond to your particular TPU; test with scrap or use a thin PP/silicone release layer.
- Do **not** boil the assembled glove with PETG/electronics attached. Even without electronics, hot water could alter TPU properties and PCL could fuse into printed grooves. Mold/cool rods separately, and avoid hot PCL on skin.

## Fit process

1. Print `part="test"` and a PETG deck; test the rail interference and revise clearances if needed.
2. Print `part="tpu"` and check placement on the back of the hand with two straps. Ensure no tight pressure across tendons, veins or nerves.
3. Adjust overall width/length and strap anchors; don't yet attach electronics.
4. Insert *cool-to-touch*, premolded PCL rods and flex the carrier to assess where stiffness is useful.
5. Position the joystick on thumb/index side using cardboard or temporary mounts. Add a dedicated adjustable PETG joystick pod in the next iteration.

A flat TPU sheet cannot retain a permanently curved shape by itself; the PCL rods provide limited form retention when cooled, but this is an experimental fit feature rather than a guaranteed stable brace.

No straps or PCL rods are included in the printed model.
