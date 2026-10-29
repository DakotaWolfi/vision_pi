// VisionPi — Raspberry Pi 5 electronics carrier
// Units: mm. Prototype: verify actual component sizes before printing.
// OpenSCAD: F6 -> Export STL.
// Layout: Pi USB/Ethernet connectors face +X; HDMI-to-USB-C adapter sits next to that edge.
// No geometry obstructs the Pi underside, fan, or cable connectors.
// Edit marked parameters to fit the actual DC-DC and HDMI/DP adapter.
//
// Raspberry Pi 5 board 85 x 56; mounting holes 58 x 49 mm on 3.5 mm edge offsets.
// M2.5 screws through Pi; use appropriate standoffs and keep underside clear.

$fn = 48;

// ---- Editable sizes ----
plate_thickness = 3.0;
margin = 9;
plate_width = 198;
plate_depth = 124;
corner_radius = 6;

pi_board = [85,56];
pi_origin = [12,12];            // lower-left of Pi board outline
pi_hole_pitch = [58,49];
pi_hole_offset = [3.5,3.5];
pi_post_height = 7;
pi_post_diameter = 7.5;
pi_screw_clearance = 2.8;       // M2.5 clearance (adjust for your printer)

// DC-DC module: use measured board/hole geometry!
// Placed behind Pi, with access around the edges.
dc_board = [60,26];             // placeholder dimensions; MEASURE
dc_origin = [15,87];            // lower-left of converter board
dc_hole_pitch = [54,20];        // placeholder; MEASURE hole centers
dc_hole_offset = [3,3];         // placeholder; MEASURE
dc_post_height = 6;
dc_post_diameter = 7;
dc_screw_clearance = 3.2;       // e.g. M3
dc_screw_mounts = false;        // set true AFTER measuring board holes
dc_zip_ties = true;

// HDMI -> USB-C DP Alt-Mode converter: body is zip-tied, not screwed.
// Sits at +X near Pi's USB/Ethernet edge.
adapter_body = [66,25];         // placeholder body length/width; MEASURE
adapter_origin = [119,28];
adapter_clearance = 1.5;
adapter_rail_height = 4;
adapter_rail_thickness = 2.6;
adapter_zip_slot_width = 4.6;
adapter_zip_slot_length = 9;
adapter_zip_positions = [13,51]; // from adapter's x origin
adapter_rail_end_gap = 7;       // clearance for cables

// General mounting slots in plate corners (optional use for headset/frame).
frame_slot_length = 10;
frame_slot_width = 4.2;

// ---- Geometry helpers ----
module rounded_plate(w,d,r,t) {
    linear_extrude(height=t)
    hull() for (x=[r,w-r], y=[r,d-r])
        translate([x,y]) circle(r=r);
}
module round_slot(length,diameter,height) {
    hull() for (dx=[-length/2+diameter/2,length/2-diameter/2])
        translate([dx,0,0]) cylinder(h=height,d=diameter);
}
module post(x,y,z,height,outer_d,inner_d) {
    translate([x,y,z]) difference() {
        cylinder(h=height,d=outer_d);
        translate([0,0,-0.1]) cylinder(h=height+0.2,d=inner_d);
    }
}

// ---- Plate, including zip-tie and mounting slots ----
difference() {
    rounded_plate(plate_width,plate_depth,corner_radius,plate_thickness);

    // Screw shaft clearance through base, so screws aren't blind.
    for (xx=[0,pi_hole_pitch[0]], yy=[0,pi_hole_pitch[1]])
        translate([pi_origin[0]+pi_hole_offset[0]+xx,
                   pi_origin[1]+pi_hole_offset[1]+yy,-0.1])
            cylinder(h=plate_thickness+0.2,d=pi_screw_clearance);

    if (dc_screw_mounts)
        for (xx=[0,dc_hole_pitch[0]], yy=[0,dc_hole_pitch[1]])
            translate([dc_origin[0]+dc_hole_offset[0]+xx,
                       dc_origin[1]+dc_hole_offset[1]+yy,-0.1])
                cylinder(h=plate_thickness+0.2,d=dc_screw_clearance);

    // Two slots per tie, either side of adapter body.
    for (sx=adapter_zip_positions) {
        translate([adapter_origin[0]+sx,
                   adapter_origin[1]-adapter_zip_slot_length/2-2,-0.1])
            cube([adapter_zip_slot_width,adapter_zip_slot_length,plate_thickness+0.2]);
        translate([adapter_origin[0]+sx,
                   adapter_origin[1]+adapter_body[1]+2-adapter_zip_slot_length/2,-0.1])
            cube([adapter_zip_slot_width,adapter_zip_slot_length,plate_thickness+0.2]);
    }

    // DC module zip-tie slots, either side of module
    if (dc_zip_ties)
        for (sx=[12,dc_board[0]-12]) {
            translate([dc_origin[0]+sx,dc_origin[1]-5,-0.1])
                cube([4.6,9,plate_thickness+0.2]);
            translate([dc_origin[0]+sx,dc_origin[1]+dc_board[1]-4,-0.1])
                cube([4.6,9,plate_thickness+0.2]);
        }

    for (pt=[[12,plate_depth-7],[plate_width-12,plate_depth-7],
             [12,7],[plate_width-12,7]])
        translate([pt[0],pt[1],-0.1])
            linear_extrude(height=plate_thickness+0.2)
                hull() for (dx=[-frame_slot_length/2+frame_slot_width/2,
                                frame_slot_length/2-frame_slot_width/2])
                    translate([dx,0]) circle(d=frame_slot_width);
}

// Pi 5 M2.5 standoffs, screws from above.
for (xx=[0,pi_hole_pitch[0]], yy=[0,pi_hole_pitch[1]])
    post(pi_origin[0]+pi_hole_offset[0]+xx,
         pi_origin[1]+pi_hole_offset[1]+yy,
         plate_thickness,pi_post_height,pi_post_diameter,pi_screw_clearance);

// DC-DC standoffs optional; enable only after measuring its holes.
if (dc_screw_mounts)
    for (xx=[0,dc_hole_pitch[0]], yy=[0,dc_hole_pitch[1]])
        post(dc_origin[0]+dc_hole_offset[0]+xx,
             dc_origin[1]+dc_hole_offset[1]+yy,
             plate_thickness,dc_post_height,dc_post_diameter,dc_screw_clearance);

// Adapter's two shallow locating rails. Zip ties actually retain the body.
// Rails intentionally end short of connector ends.
for (dy=[-adapter_clearance-adapter_rail_thickness,
          adapter_body[1]+adapter_clearance])
    translate([adapter_origin[0]+adapter_rail_end_gap,
               adapter_origin[1]+dy,plate_thickness])
        cube([adapter_body[0]-2*adapter_rail_end_gap,
              adapter_rail_thickness,adapter_rail_height]);

// Low adapter end stop at ONE end only; other end open to simplify assembly.
// Comment out if the cable connector occupies this face.
translate([adapter_origin[0]-adapter_rail_thickness-adapter_clearance,
           adapter_origin[1]+2,plate_thickness])
    cube([adapter_rail_thickness,adapter_body[1]-4,adapter_rail_height]);

// NOTE: Power electronics require insulation and airflow. Do not press exposed
// solder pads against printed plastic or allow cable strain on USB-C ports.
