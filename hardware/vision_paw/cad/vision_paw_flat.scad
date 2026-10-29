// VISION PAW — organic flat-print hand-back glove v0.2
// Units: mm. Each setting below appears in OpenSCAD Customizer.
// The flat TPU bends around the hand; optional removable PCL ribs hold a fitted curve.
// Experimental hand-shaped pattern, NOT a scan or guaranteed anatomical fit.

// ==== OUTPUT ==========================================================
/* [Output] */
// Export one material at a time. "assembly" spaces both parts for preview.
part = "assembly"; // [assembly,glove_tpu,electronics_petg,joystick_petg,rail_test]
hand = "right"; // [right,left]

// ==== YOUR HAND (measure with ruler/string later) ======================
/* [Hand dimensions] */
// Across knuckles, excluding thumb
knuckle_width = 83; // [60:1:115]
// Wrist width, side to side, not circumference
wrist_width = 57; // [40:1:85]
// Wrist crease to knuckle line
palm_length = 93; // [65:1:130]
// How far thumb-side support protrudes
thumb_wing = 23; // [8:1:38]
// Width of central hand-back platform
deck_width = 39; // [28:1:60]

// ==== FLEXIBLE SHELL ==================================================
/* [TPU geometry] */
base_thickness = 1.6; // [1.0:0.2:3.0]
flex_bridge_width = 13; // [7:1:22]
strap_slot_width = 4.5; // [3:0.5:7]
strap_width = 18; // [10:1:28]
rail_clearance = 0.6; // [0.2:0.1:1.2]

// ==== REMOLDABLE PCL STIFFENERS =======================================
/* [PCL ribs] */
// PCL rods are captured with flexible strap clips; do not bond the rods in.
pcl_diameter = 3.5; // [2:0.5:6]
pcl_channel_length = 39; // [25:1:53]
pcl_channel_spacing = 29; // [22:1:43]

// ==== REMOVABLE ELECTRONICS MOUNTS ===================================
/* [PETG insert] */
deck_length = 42; // [30:1:60]
deck_thickness = 2.0; // [1.5:0.2:3.5]
generic_hole_pitch_x = 26; // [14:1:40]
generic_hole_pitch_y = 32; // [15:1:48]
generic_hole_diameter = 2.4; // [2:0.1:3.5]
joystick_plate_size = 24; // [18:1:36]

// ==== INTERNAL ========================================================
$fn = 48;
eps = 0.02;
mirror_sign = hand == "right" ? -1 : 1;
function side_x(x) = mirror_sign*x;
function hand_w(y) = wrist_width + (knuckle_width-wrist_width)*min(1,max(0,y/palm_length));

// Smooth, asymmetric silhouette with wrist, knuckle crown, thumb-side wing.
// x=0 is hand center; y=0 wrist crease, y=palm_length knuckles.
module smooth_hull(a,b,r1,r2) {
 hull(){
  translate(a) circle(r=r1);
  translate(b) circle(r=r2);
 }
}
module glove_outline(){
 union(){
   // main palm with tapered wrist and rounded knuckle crown
   hull(){
    translate([0,5]) scale([wrist_width/2,12]) circle(r=1);
    translate([0,palm_length*.51]) scale([knuckle_width*.51,22]) circle(r=1);
    translate([0,palm_length-8]) scale([knuckle_width*.49,14]) circle(r=1);
   }
   // thumb-index saddle, two organic lobes joined to main area
   hull(){
    translate([side_x(knuckle_width*.34),palm_length*.65]) circle(r=13);
    translate([side_x(knuckle_width*.50+thumb_wing*.57),palm_length*.76]) circle(r=9);
    translate([side_x(knuckle_width*.34),palm_length*.88]) circle(r=10);
   }
   // shorter dorsal wrist tail
   hull(){
    translate([0,4]) scale([wrist_width*.43,10]) circle(r=1);
    translate([0,-12]) scale([wrist_width*.31,9]) circle(r=1);
   }
 }
}
module capsule(l,w){hull(){
 translate([-l/2+w/2,0]) circle(d=w);
 translate([l/2-w/2,0]) circle(d=w);
}}
module strap_cut(x,y){
 translate([x,y,-eps]) linear_extrude(height=base_thickness+2*eps)
   rotate(90) capsule(strap_width,strap_slot_width);
}
module lattice_cut(x,y,l=14,w=3){
 translate([x,y,-eps]) linear_extrude(height=base_thickness+2*eps)
   capsule(l,w);
}
module tpu_sheet(){
 difference(){
  linear_extrude(base_thickness) glove_outline();
  // Pair of curved strap anchor slots at wrist and proximal palm edges.
  for(y=[12,palm_length*.58], s=[-1,1])
    strap_cut(s*(hand_w(y)*.43),y);
  // Flexible slits on either side of the rigid electronics island
  for(y=[30,39,palm_length-17],s=[-1,1])
    lattice_cut(s*(deck_width/2+14),y,flex_bridge_width-1,2.8);
  // Three small ventilation slots across the knuckle bridge
  for(x=[-17,0,17]) lattice_cut(x,palm_length-4,11,3);
 }
}
// Straight slide-in PETG cartridge with TWO open ends, soft side walls and
// intermittent TPU-overhang tabs. No permanent mount for actual electronics yet.
module deck_socket(){
 L=deck_length;
 W=deck_width;
 y0=palm_length*.46;
 for(s=[-1,1]){
   translate([s*(W/2+rail_clearance+1.7)-1.7,y0-L/2,base_thickness])
      cube([3.4,L,2.4]);
   // three intermittent inward lips for easier TPU assembly/printing
   for(dy=[4,L/2,L-4])
     translate([s*(W/2+rail_clearance+1.7)-1.7,
                y0-L/2+dy-2,base_thickness+2.1])
        cube([3.4,4,0.8]);
 }
 // soft stop at far end
 translate([-W/2,y0+L/2,base_thickness])
   cube([W,2.2,1.9]);
}
// Removable PCL longitudinal ribs retained by small TPU clip bridges.
// Channels intentionally stop short of wrist and knuckles.
// Open-bottom grooves leave much of carrier TPU able to flex.
module pcl_retainer(x){
 y0=palm_length*.47-pcl_channel_length/2;
 wall=1.4;
 for(s=[-1,1])
   translate([x+s*(pcl_diameter/2+wall/2+.35)-wall/2,y0,base_thickness])
      cube([wall,pcl_channel_length,2.4]);
 for(y=[y0+5,y0+pcl_channel_length-5])
   translate([x-pcl_diameter/2-wall,y,base_thickness+2.2])
      cube([pcl_diameter+2*wall,2.4,0.9]);
}
module tpu(){
 union(){
  tpu_sheet();
  deck_socket();
  for(s=[-1,1]) pcl_retainer(s*pcl_channel_spacing/2+ s*(deck_width/2+7));
  // TPU pocket for joystick plate, on index/thumb wing
  x=side_x(knuckle_width*.45+thumb_wing*.38);
  y=palm_length*.78;
  for(s=[-1,1])
   translate([x+s*(joystick_plate_size/2+1.0)-1.4,
              y-joystick_plate_size/2,base_thickness])
    cube([2.8,joystick_plate_size,2.6]);
 }
}
module petg_deck(){
 difference(){
  translate([-deck_width/2,-deck_length/2,0])
   linear_extrude(deck_thickness)
     offset(r=2) offset(delta=-2) square([deck_width,deck_length]);
  // mounting holes are GENERIC: not an ESP32 or OLED footprint
  for(x=[-generic_hole_pitch_x/2,generic_hole_pitch_x/2],
      y=[-generic_hole_pitch_y/2,generic_hole_pitch_y/2])
   translate([x,y,-eps]) cylinder(h=deck_thickness+2*eps,d=generic_hole_diameter);
 }
}
module joystick_deck(){
 difference(){
  translate([-joystick_plate_size/2,-joystick_plate_size/2,0])
   linear_extrude(deck_thickness)
     offset(r=3) offset(delta=-3) square([joystick_plate_size,joystick_plate_size]);
  translate([0,0,-eps]) cylinder(h=deck_thickness+2*eps,d=4); // cable pass-through
 }
}
if(part=="glove_tpu") tpu();
else if(part=="electronics_petg") petg_deck();
else if(part=="joystick_petg") joystick_deck();
else if(part=="rail_test"){
 intersection(){
  tpu();
  translate([-deck_width/2-6,palm_length*.46-10,-eps])
    cube([deck_width+12,20,base_thickness+6]);
 }
}
else {
 tpu();
 translate([knuckle_width+43,deck_length/2+5,0]) petg_deck();
 translate([knuckle_width+43,-joystick_plate_size/2-10,0]) joystick_deck();
}
