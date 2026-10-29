# Vision Paw v0.3 — open branching TPU hand mesh

The v0.1/v0.2 solid-plate approach has been replaced. This is an **open, vein-like, interconnected TPU web**, inspired by the user's reference images: irregular large cells, a tapered wrist/forearm section, finger/knuckle edge and thumb-side loop. It prints flat but is intended to drape and flex with the hand.

![No preview embedded](./vision_paw_flat.scad)

## OpenSCAD Customizer

Parameters are grouped and labeled at the top of `vision_paw_flat.scad`:

- `part`: `tpu`, `petg_main`, `petg_joystick`, `all` (export different materials separately).
- `hand`: right/left mirrored geometry.
- Hand measurements: `palm_width`, `palm_length`, `wrist_width`, `forearm_extension`, `thumb_reach` (mm).
- TPU: `vein_width`, `branch_width`, `mesh_thickness`.
- PETG: generic deck and joystick mounting dimensions.

The wrist is y = 0; palm/knuckles point toward positive Y. Default hand measurements are **placeholders**, not scanned. Hardware mounting holes are **generic interfaces**, NOT verified component footprints.

## Print and design status

Use OpenSCAD F6 then Export > STL for each part. A locally generated TPU mesh successfully exported to STL and was checked with Trimesh as **watertight, single connected component** (3600 triangular faces) before the GitHub version was authored. The published source has not undergone an independent physical fit test. Start with the TPU web only; iterate before adding electronics.

The PETG islands are separate slim screw-mounted plates; they are not fused to the TPU sheet. The main cartridge represents a place to fasten electronics, **not yet a dimensioned ESP32/OLED board holder**. The joystick plate is a minimalist mounting interface rather than a completed joystick shell.

The v0.3 model deliberately has *no full solid deck*: mounting loads go through localized reinforced nodes. Straps/finger fixation still need a hands-on fit design.

## PCL / Whitemorph

PCL shaping remains a **planned separate insert**; `pcl_rod_diameter` and `pcl_clip_count` are reserved parameters and do not yet produce channels. The open vein structure can later have individual molded PCL rods along selected branches, leaving wrist and knuckle cells flexible. This needs retention geometry designed after a flex test. Do not interpret the parameters as implemented features.

## Next steps

1. Print a small scaled or partial TPU fit test to check curve/edge comfort.
2. Measure wrist width, palm width, wrist-to-knuckle length and thumb-side clearance.
3. Tune branch placement and the flex pattern for the hand.
4. Design local PCL rod channels and actual PETG mounts for the measured electronics, without turning the web back into a solid plate.
