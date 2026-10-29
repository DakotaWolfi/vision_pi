// VisionPi — Raspberry Pi 5 electronics carrier
// Units: mm. Prototype: verify actual component sizes before printing.
// OpenSCAD: F6 -> Export STL.
// Layout: Pi USB/Ethernet edge points +X; DP adapter sits by the DC-DC board,
// away from that edge. Leave connector ends clear for slim 90-degree HDMI plugs.
// No geometry obstructs the Pi underside, fan, or cable connectors.
// Edit marked parameters to fit the actual DC-DC and HDMI/DP adapter.
//
// Raspberry Pi 5 board 85 x 56; mounting holes 58 x 49 mm on 3.5 mm edge offsets.
// M2.5 screws through Pi; use appropriate standoffs and keep underside clear.

$fn = 48;

// Layout variants: both retain mounting holes and perforations.
layout_variant = "stacked"; // [stacked,compact,wide]
adapter_rotate_90 = layout_variant == "compact"; // stacked uses horizontal adapter between boards


// ---- Lightweight plate options ----
// solid: original full plate; hex: honeycomb apertures; round: circular holes.
// The pattern automatically leaves clearance around all mounting features.
plate_pattern = "hex"; // [hex,round,solid]
pattern_hole_diameter = 12;      // mm: across corners for hex
pattern_pitch_x = 17;            // mm between hole centers across rows
pattern_pitch_y = 15;            // mm between rows
pattern_edge_margin = 6;        // mm, solid perimeter around plate

// ---- Editable sizes ----
plate_thickness = 3.0;
margin = 9;
plate_width = layout_variant == "stacked" ? 112 : (layout_variant == "compact" ? 160 : 198);
plate_depth = layout_variant == "stacked" ? 178 : 124;
corner_radius = 6;

pi_board = [85,56];
pi_origin = layout_variant == "stacked" ? [12,109] : [12,12];            // lower-left of Pi board outline
pi_hole_pitch = [58,49];
pi_hole_offset = [3.5,3.5];
pi_post_height = 7;
pi_post_diameter = 8.0; // adjustable overall boss outside diameter
pi_screw_clearance = 2.8;       // M2.5 clearance (adjust for your printer)

// DC-DC module: use measured board/hole geometry!
// Placed behind Pi, with access around the edges.
dc_board = [59,44];             // product overall width/depth
dc_origin = layout_variant == "stacked" ? [15,10] : [20,75];            // beside Pi, not under its cooling
dc_hole_pitch = [48,33];        // assumed CM4 pitch; verify on real module
dc_hole_offset = [5.5,5.5];     // centered in 59x44 envelope
dc_post_height = 6;
dc_post_diameter = 8.0; // adjustable overall boss outside diameter
dc_screw_clearance = 2.8;       // M2.5 mounting-hole clearance
dc_screw_mounts = true;         // provisional: confirm hole positions before print
dc_zip_ties = layout_variant != "stacked"; // stacked layout leaves converter-side wiring free

// HDMI -> USB-C DP Alt-Mode converter: body is zip-tied, not screwed.
// Sits at +X near Pi's USB/Ethernet edge.
adapter_body = [60,32];         // ULT-unite body from product diagram
adapter_origin = layout_variant == "stacked" ? [29,69] : (layout_variant == "compact" ? [112,49] : [109,78]);
adapter_clearance = 1.5;
// Adapter held EDGE-ON between tall rails. This is a separate measured
// gap from the 60x32 mm face dimensions; check housing thickness before print.
adapter_wall_height = 20;      // mm above plate
adapter_wall_thickness = 2.6;  // mm
adapter_wall_inner_gap = 16;   // mm clear opening between inner wall faces
adapter_wall_offset = 0;       // mm: signed shift across short axis
adapter_wall_along_offset = 0; // mm: signed shift along long axis
adapter_wall_length = 42;      // mm, leave both connectors accessible
adapter_zip_slot_width = 4.6;
adapter_zip_slot_length = 9;
adapter_zip_positions = [13,43]; // away from connector ends
adapter_rail_end_gap = 9;       // keep both connector faces accessible
adapter_footprint = adapter_rotate_90 ? [adapter_body[1], adapter_body[0]] : adapter_body;

// Independent mounting-hole mode: plain through-hole or heat-set threaded insert.
// Heat-set pilot is BLIND in the standoff; only use inserts matched to your hardware.
pi_heat_inserts = false; // [true,false]
dc_heat_inserts = false; // [true,false]
pi_insert_pilot_diameter = 3.5; // verify against M2.5 insert datasheet
dc_insert_pilot_diameter = 3.5; // verify against M2.5 insert datasheet
pi_insert_depth = 4.0;
dc_insert_depth = 4.0;
insert_lead_in = 0.2; // extra mouth radius for insertion
// Enforce closed bottom in insert mode by not boring the base plate.

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
module post(x,y,z,height,outer_d,inner_d,heat_insert=false,pilot_d=3.5,pilot_depth=4) {
    assert(outer_d >= pilot_d+2.4, "Boss too thin around insert pilot");
    assert(!heat_insert || pilot_depth < height, "Insert pocket must leave a solid floor");
    translate([x,y,z]) difference() {
        cylinder(h=height,d=outer_d);
        if (heat_insert) {
            // top-accessible blind insert pilot, with a small lead-in
            translate([0,0,height-pilot_depth])
                cylinder(h=pilot_depth+0.2,d=pilot_d);
            translate([0,0,height-0.4])
                cylinder(h=0.5,d1=pilot_d,d2=pilot_d+2*insert_lead_in);
        } else
            translate([0,0,-0.1])
                cylinder(h=height+0.2,d=inner_d);
    }
}

// Holes are omitted near mounts, tie-down slots and adapter's locating rails.
// Extra material around the adapter keeps the zip ties from tearing the plate.
function dist2(x,y,a,b) = (x-a)*(x-a)+(y-b)*(y-b);
function near_pi_post(x,y) =
    len([for (xx=[0,pi_hole_pitch[0]], yy=[0,pi_hole_pitch[1]])
        if (dist2(x,y,pi_origin[0]+pi_hole_offset[0]+xx,
                        pi_origin[1]+pi_hole_offset[1]+yy)<pow(pi_post_diameter/2+3+pattern_hole_diameter/2,2)) 1]) > 0;
function near_dc_post(x,y) =
    dc_screw_mounts &&
    len([for (xx=[0,dc_hole_pitch[0]], yy=[0,dc_hole_pitch[1]])
        if (dist2(x,y,dc_origin[0]+dc_hole_offset[0]+xx,
                        dc_origin[1]+dc_hole_offset[1]+yy)<pow(dc_post_diameter/2+3+pattern_hole_diameter/2,2)) 1]) > 0;
// Keep the strap slots and two retaining rails, but allow lightening holes
// UNDER the converter body where no mounting hardware occupies the plate.
function in_box(x,y,x0,y0,x1,y1,pad=0) =
    x > x0-pad && x < x1+pad && y > y0-pad && y < y1+pad;
function near_adapter(x,y) =
    let(pad=pattern_hole_diameter/2+2,
        ax=adapter_origin[0], ay=adapter_origin[1],
        aw=adapter_footprint[0], ah=adapter_footprint[1])
    (!adapter_rotate_90 ?
      (in_box(x,y,ax+adapter_rail_end_gap,ay-adapter_clearance-adapter_rail_thickness,
                  ax+aw-adapter_rail_end_gap,ay-adapter_clearance,pad) ||
       in_box(x,y,ax+adapter_rail_end_gap,ay+ah+adapter_clearance,
                  ax+aw-adapter_rail_end_gap,ay+ah+adapter_clearance+adapter_rail_thickness,pad) ||
       len([for(sx=adapter_zip_positions)
          if (in_box(x,y,ax+sx,ay-adapter_zip_slot_length-2,
                     ax+sx+adapter_zip_slot_width,ay-2,pad) ||
              in_box(x,y,ax+sx,ay+ah+2,
                     ax+sx+adapter_zip_slot_width,ay+ah+2+adapter_zip_slot_length,pad)) 1])>0)
      :
      (in_box(x,y,ax-adapter_clearance-adapter_rail_thickness,ay+adapter_rail_end_gap,
                  ax-adapter_clearance,ay+ah-adapter_rail_end_gap,pad) ||
       in_box(x,y,ax+aw+adapter_clearance,ay+adapter_rail_end_gap,
                  ax+aw+adapter_clearance+adapter_rail_thickness,ay+ah-adapter_rail_end_gap,pad) ||
       len([for(sy=adapter_zip_positions)
          if(in_box(x,y,ax-adapter_zip_slot_length-2,ay+sy,
                    ax-2,ay+sy+adapter_zip_slot_width,pad) ||
             in_box(x,y,ax+aw+2,ay+sy,
                    ax+aw+2+adapter_zip_slot_length,ay+sy+adapter_zip_slot_width,pad)) 1])>0));
function near_adapter_wall(x,y) =
    let(pad=pattern_hole_diameter/2+3,
        wallx=adapter_origin[0]+adapter_footprint[0]/2+adapter_wall_offset,
        wally=adapter_origin[1]+adapter_footprint[1]/2+adapter_wall_offset,
        longx=adapter_origin[0]+(adapter_footprint[0]-adapter_wall_length)/2+adapter_wall_along_offset,
        longy=adapter_origin[1]+(adapter_footprint[1]-adapter_wall_length)/2+adapter_wall_along_offset)
    (!adapter_rotate_90 ?
     in_box(x,y,longx,wally-adapter_wall_inner_gap/2-adapter_wall_thickness,
         longx+adapter_wall_length,wally+adapter_wall_inner_gap/2+adapter_wall_thickness,pad)
      :
     in_box(x,y,wallx-adapter_wall_inner_gap/2-adapter_wall_thickness,longy,
        wallx+adapter_wall_inner_gap/2+adapter_wall_thickness,longy+adapter_wall_length,pad));

function near_dc_ties(x,y) =
    dc_zip_ties &&
    x>dc_origin[0]-5 && x<dc_origin[0]+dc_board[0]+5 &&
    (abs(y-(dc_origin[1]-1))<7+pattern_hole_diameter/2 ||
     abs(y-(dc_origin[1]+dc_board[1]))<7+pattern_hole_diameter/2);
function near_frame_slots(x,y) =
    len([for(px=[12,plate_width-12],py=[7,plate_depth-7])
        if(dist2(x,y,px,py)<pow(10+pattern_hole_diameter/2,2)) 1]) > 0;

module lightening_holes() {
 if(plate_pattern!="solid")
  for(row=[0:ceil((plate_depth-2*pattern_edge_margin)/pattern_pitch_y)]){
   y=pattern_edge_margin+row*pattern_pitch_y;
   for(column=[0:ceil((plate_width-2*pattern_edge_margin)/pattern_pitch_x)]){
     x=pattern_edge_margin+column*pattern_pitch_x+
       ((row%2)==1?pattern_pitch_x/2:0);
     if(x>pattern_edge_margin+pattern_hole_diameter/2 &&
        x<plate_width-pattern_edge_margin-pattern_hole_diameter/2 &&
        y>pattern_edge_margin+pattern_hole_diameter/2 &&
        y<plate_depth-pattern_edge_margin-pattern_hole_diameter/2 &&
        !near_pi_post(x,y) && !near_dc_post(x,y) &&
        !near_adapter(x,y) && !near_adapter_wall(x,y) && !near_dc_ties(x,y) &&
        !near_frame_slots(x,y))
       translate([x,y,-0.1])
         cylinder(h=plate_thickness+0.2,d=pattern_hole_diameter,
                  $fn=plate_pattern=="hex"?6:48);
   }
  }
}

// ---- Plate, including zip-tie and mounting slots ----
difference() {
    rounded_plate(plate_width,plate_depth,corner_radius,plate_thickness);
    lightening_holes();

    // Screw shaft clearance through base, so screws aren't blind.
    if (!pi_heat_inserts)
    for (xx=[0,pi_hole_pitch[0]], yy=[0,pi_hole_pitch[1]])
        translate([pi_origin[0]+pi_hole_offset[0]+xx,
                   pi_origin[1]+pi_hole_offset[1]+yy,-0.1])
            cylinder(h=plate_thickness+0.2,d=pi_screw_clearance);

    if (dc_screw_mounts && !dc_heat_inserts)
        for (xx=[0,dc_hole_pitch[0]], yy=[0,dc_hole_pitch[1]])
            translate([dc_origin[0]+dc_hole_offset[0]+xx,
                       dc_origin[1]+dc_hole_offset[1]+yy,-0.1])
                cylinder(h=plate_thickness+0.2,d=dc_screw_clearance);

    // Two zip-tie pairs, rotated together with the converter footprint.
    if (!adapter_rotate_90) {
        for (sx=adapter_zip_positions) {
            translate([adapter_origin[0]+sx,
                       adapter_origin[1]-adapter_zip_slot_length-2,-0.1])
                cube([adapter_zip_slot_width,adapter_zip_slot_length,plate_thickness+0.2]);
            translate([adapter_origin[0]+sx,
                       adapter_origin[1]+adapter_footprint[1]+2,-0.1])
                cube([adapter_zip_slot_width,adapter_zip_slot_length,plate_thickness+0.2]);
        }
    } else {
        for (sy=adapter_zip_positions) {
            translate([adapter_origin[0]-adapter_zip_slot_length-2,
                       adapter_origin[1]+sy,-0.1])
                cube([adapter_zip_slot_length,adapter_zip_slot_width,plate_thickness+0.2]);
            translate([adapter_origin[0]+adapter_footprint[0]+2,
                       adapter_origin[1]+sy,-0.1])
                cube([adapter_zip_slot_length,adapter_zip_slot_width,plate_thickness+0.2]);
        }
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
         plate_thickness,pi_post_height,pi_post_diameter,pi_screw_clearance,
         pi_heat_inserts,pi_insert_pilot_diameter,pi_insert_depth);

// DC-DC standoffs optional; enable only after measuring its holes.
if (dc_screw_mounts)
    for (xx=[0,dc_hole_pitch[0]], yy=[0,dc_hole_pitch[1]])
        post(dc_origin[0]+dc_hole_offset[0]+xx,
             dc_origin[1]+dc_hole_offset[1]+yy,
             plate_thickness,dc_post_height,dc_post_diameter,dc_screw_clearance,
             dc_heat_inserts,dc_insert_pilot_diameter,dc_insert_depth);

// Tall parallel walls holding converter edge-on.
// Horizontal footprint: walls run X, spacing in Y.
// Rotated footprint: walls run Y, spacing in X.
assert(adapter_wall_inner_gap >= 16, "Adapter clear gap must be at least 16 mm");
assert(adapter_wall_height >= 20, "Adapter wall height must be at least 20 mm");
assert(adapter_wall_length > 0 &&
       adapter_wall_length <= (adapter_rotate_90 ? adapter_footprint[1] : adapter_footprint[0]),
       "Wall length must fit within converter long dimension");
if (!adapter_rotate_90) {
    center_y = adapter_origin[1] + adapter_footprint[1]/2 + adapter_wall_offset;
    start_x  = adapter_origin[0] + (adapter_footprint[0]-adapter_wall_length)/2
               + adapter_wall_along_offset;
    for (dy=[-adapter_wall_inner_gap/2-adapter_wall_thickness,
              adapter_wall_inner_gap/2])
        translate([start_x,center_y+dy,plate_thickness])
            cube([adapter_wall_length,adapter_wall_thickness,adapter_wall_height]);
} else {
    center_x = adapter_origin[0] + adapter_footprint[0]/2 + adapter_wall_offset;
    start_y  = adapter_origin[1] + (adapter_footprint[1]-adapter_wall_length)/2
               + adapter_wall_along_offset;
    for (dx=[-adapter_wall_inner_gap/2-adapter_wall_thickness,
              adapter_wall_inner_gap/2])
        translate([center_x+dx,start_y,plate_thickness])
            cube([adapter_wall_thickness,adapter_wall_length,adapter_wall_height]);
}

// Both adapter ends OPEN: route slim HDMI right-angle plug toward Pi and
// USB-C cable toward goggles without a printed end wall.

// NOTE: Power electronics require insulation and airflow. Do not press exposed
// solder pads against printed plastic or allow cable strain on USB-C ports.
