// Vision Paw v0.1 - flat-print TPU shell with remoldable PCL stiffener channels
// Units mm; OpenSCAD F6. Print shell TPU 95A, PETG cartridges separately.
// Whitemorph/PCL rods are shaped separately and inserted when comfortably cool.
// Do NOT boil electronics or put hot plastic against skin.
$fn=36;
part = "all"; // "all", "tpu", "petg", "test"
hand_width = 85;             // across metacarpals, excluding thumb
hand_length = 100;           // wrist to knuckles (shell area)
shell_thickness = 1.9;
side_margin = 8;
wrist_width = 64;
knuckle_width = 84;
strap_width = 18;
strap_slot_length = 22;
strap_slot_width = 4.5;
// PCL stiffeners are discontinuous: leave a flexible gap by knuckles and wrist
pcl_rod_diameter = 3.5;
pcl_lane_offset = 26;        // each channel from centerline
pcl_lane_length = 58;
pcl_lane_y = 48;
pcl_rail_wall = 2.1;
pcl_rail_height = 3.0;
// Removable PETG electronics plate, retained by TPU side rails and a flexible end tab
cartridge_width = 34;
cartridge_length = 42;
cartridge_thickness = 2.2;
cartridge_y = 47;
rail_height = 3.4;
rail_width = 3.2;
cartridge_clearance = 0.6;
// attachment holes for generic M2 PCB mount - NOT actual ESP/OLED footprint
cartridge_hole_pitch = [26,32];
cartridge_hole_diameter = 2.3;
// wrist and knuckle strap anchors are designed as slots in flexible wings
function half_width(y) = (wrist_width+(knuckle_width-wrist_width)*y/hand_length)/2;
module outline2d(){
  polygon(points=[
    [-half_width(0),0],
    [ half_width(0),0],
    [ half_width(13)+side_margin,13],
    [ half_width(28)+side_margin,28],
    [ half_width(65)+side_margin,65],
    [ half_width(hand_length-12)+side_margin,hand_length-12],
    [ half_width(hand_length),hand_length],
    [-half_width(hand_length),hand_length],
    [-half_width(hand_length-12)-side_margin,hand_length-12],
    [-half_width(65)-side_margin,65],
    [-half_width(28)-side_margin,28],
    [-half_width(13)-side_margin,13]
  ]);
}
module slot2d(l,w){hull(){translate([-l/2+w/2,0]) circle(d=w);translate([l/2-w/2,0]) circle(d=w);}}
module tpu_base(){
 difference(){
  linear_extrude(shell_thickness) outline2d();
  // strap slots: two at wrist and two near knuckles
  for (y=[15,85], x=[-half_width(y)+6,half_width(y)-6])
   translate([x,y,-.1]) linear_extrude(shell_thickness+.2)
    rotate(90) slot2d(strap_slot_length,strap_slot_width);
  // deliberate flex zones: lateral slits near edges, leaving center backbone
  for(y=[32,37,69,74],sx=[-1,1])
   translate([sx*(hand_width/2-3),y,-.1])
    linear_extrude(shell_thickness+.2) slot2d(11,2.8);
 }
}
module pcl_channel(x){
 // Lay PCL rods into open longitudinal grooves after molding.
 // Rail gap nominal 3.8 mm; flexible TPU can be tied/covered if needed.
 for(dx=[-(pcl_rod_diameter/2+pcl_rail_wall/2+0.25),
          (pcl_rod_diameter/2+pcl_rail_wall/2+0.25)])
  translate([x+dx,pcl_lane_y-pcl_lane_length/2,shell_thickness])
   cube([pcl_rail_wall,pcl_lane_length,pcl_rail_height]);
 // short bridges at both ends to discourage rods slipping longitudinally
 for(y=[pcl_lane_y-pcl_lane_length/2-1,
        pcl_lane_y+pcl_lane_length/2])
  translate([x-pcl_rod_diameter/2-pcl_rail_wall,y,shell_thickness])
   cube([pcl_rod_diameter+2*pcl_rail_wall,1.0,1.6]);
 // lateral TPU retainers across groove at intervals: overlaid by zip/elastic thread, optional
}
// cartridge deck sits atop flat TPU; 2 TPU side rails with shallow inward lips.
// Low stress interference tabs, final fit needs printing test.
module deck_rails(){
 for(s=[-1,1]){
  translate([s*(cartridge_width/2+cartridge_clearance+rail_width/2)-rail_width/2,
             cartridge_y-cartridge_length/2,shell_thickness])
   cube([rail_width,cartridge_length,rail_height]);
  translate([s*(cartridge_width/2+cartridge_clearance+rail_width/2)-rail_width/2,
             cartridge_y-cartridge_length/2,shell_thickness+rail_height-.9])
   cube([rail_width,cartridge_length,.9]);
 }
 // end stop, 2 mm high
 translate([-cartridge_width/2,cartridge_y+cartridge_length/2,shell_thickness])
  cube([cartridge_width,2,2]);
}
module tpu(){
 union(){
  tpu_base();
  for(x=[-pcl_lane_offset,pcl_lane_offset]) pcl_channel(x);
  deck_rails();
 }
}
module petg(){
 difference(){
   translate([-cartridge_width/2,cartridge_y-cartridge_length/2,0])
    linear_extrude(cartridge_thickness) offset(r=1.5)
      offset(delta=-1.5) square([cartridge_width,cartridge_length]);
   // optional universal screw holes, actual electronics need adapter plates
   for(x=[-cartridge_hole_pitch[0]/2,cartridge_hole_pitch[0]/2],
       y=[cartridge_y-cartridge_hole_pitch[1]/2,cartridge_y+cartridge_hole_pitch[1]/2])
     translate([x,y,-.1]) cylinder(h=cartridge_thickness+.2,d=cartridge_hole_diameter);
 }
}
if(part=="tpu") tpu();
else if(part=="petg") petg();
else if(part=="test"){
  // small TPU rail fit test: export flat, fit with 2.2-mm PETG coupon
  intersection(){
    tpu();
    translate([-24,22,0]) cube([48,51,10]);
  }
}
else if(part=="all"){
 tpu();
 translate([120,0,0]) petg();
}
