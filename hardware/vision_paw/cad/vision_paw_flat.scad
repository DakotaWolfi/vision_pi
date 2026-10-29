// Vision Paw v0.3 - open, vein-like TPU hand mesh, printed flat.
// ALL parameters in millimetres. Designed for OpenSCAD Customizer.

/* [Output] */
part = "tpu"; // [tpu,petg_main,petg_joystick,all]
hand = "right"; // [right,left]

/* [Hand measurements] */
palm_width = 85; // [65:1:110]
palm_length = 95; // [70:1:125]
wrist_width = 58; // [40:1:80]
forearm_extension = 52; // [25:1:90]
thumb_reach = 26; // [12:1:45]

/* [Flexible TPU mesh] */
vein_width = 5; // [3:0.5:8]
branch_width = 3.5; // [2:0.5:6]
mesh_thickness = 2; // [1.2:0.2:3.5]
node_radius = 4.6; // [3:0.5:8]

/* [Removable PETG islands] */
main_mount_width = 36; // [25:1:48]
main_mount_length = 37; // [28:1:50]
joystick_mount_diameter = 21; // [16:1:28]
mount_hole_diameter = 2.7; // [2:0.1:4]
petg_thickness = 2.4; // [1.5:0.1:4]

/* [PCL form shaping] */
pcl_rod_diameter = 3.5; // [2:0.5:6]
pcl_clip_count = 3; // [0:1:5]

$fn=36;
mirror_x = hand=="right" ? 1 : -1;
function P(p) = [p[0]*mirror_x,p[1]];
module bone(a,b,wd=vein_width) {
  hull(){translate(P(a)) circle(d=wd);translate(P(b)) circle(d=wd);}
}
module n(p,diam=node_radius*2){translate(P(p)) circle(d=diam);}
module loop_path(pts,wd=vein_width){
  for(i=[0:len(pts)-2]) bone(pts[i],pts[i+1],wd);
  bone(pts[len(pts)-1],pts[0],wd);
}
module veins2d(){
 w=palm_width/2; r=wrist_width/2; f=forearm_extension;
 loop_path([[-r*.8,-f],[-r,-f*.65],[-r*.88,-f*.24],[-w*.72,5],[-w*.95,32],
 [-w*.90,palm_length*.66],[-w*.56,palm_length*.95],[0,palm_length],
 [w*.56,palm_length*.95],[w*.92,palm_length*.7],[w*.89,32],[w*.73,5],
 [r*.88,-f*.24],[r,-f*.65],[r*.8,-f]]);
 bone([-r*.8,-f],[-r*.28,-f*.65]);bone([r*.8,-f],[r*.28,-f*.65]);
 bone([-r*.28,-f*.65],[0,-f*.30]);bone([r*.28,-f*.65],[0,-f*.30]);
 bone([-r,-f*.65],[-r*.35,-f*.12]);bone([r,-f*.65],[r*.35,-f*.12]);
 bone([-r*.35,-f*.12],[-w*.72,5]);bone([r*.35,-f*.12],[w*.73,5]);
 bone([-r*.35,-f*.12],[0,16]);bone([r*.35,-f*.12],[0,16]);
 bone([-w*.72,5],[-w*.30,30]);bone([w*.73,5],[w*.30,30]);
 bone([-w*.30,30],[0,16]);bone([w*.30,30],[0,16]);
 bone([-w*.95,32],[-w*.3,30]);bone([w*.89,32],[w*.3,30]);
 bone([-w*.30,30],[-w*.76,palm_length*.58]);
 bone([w*.30,30],[w*.75,palm_length*.58]);
 bone([-w*.76,palm_length*.58],[-w*.34,palm_length*.74]);
 bone([w*.75,palm_length*.58],[w*.30,palm_length*.76]);
 bone([-w*.34,palm_length*.74],[0,palm_length*.61]);
 bone([w*.30,palm_length*.76],[0,palm_length*.61]);
 bone([0,palm_length*.61],[-w*.56,palm_length*.95]);
 bone([0,palm_length*.61],[w*.56,palm_length*.95]);
 bone([0,palm_length*.61],[0,palm_length]);
 bone([-w*.95,32],[0,palm_length*.61],branch_width);
 bone([w*.89,32],[0,palm_length*.61],branch_width);
 bone([-r*.35,-f*.12],[r*.30,30],branch_width);
 bone([r*.35,-f*.12],[-w*.3,30],branch_width);
 // Asymmetric thumb/index wing, part of mesh rather than a solid lobe.
 loop_path([[w*.89,32],[w*.95,palm_length*.61],
  [w+thumb_reach*.70,palm_length*.74],[w+thumb_reach,palm_length*.91],
  [w+thumb_reach*.47,palm_length*.97],[w*.56,palm_length*.95],
  [w*.30,palm_length*.76]],branch_width);
 bone([w*.95,palm_length*.61],[w+thumb_reach*.47,palm_length*.97],branch_width);
 for(y=[-f*.54,palm_length*.36],side=[-1,1]){
   px=side*(y<0?r*.94:w*.91);n([px,y],10);
 }
}
module fastener_holes2d(){
 w=palm_width/2;r=wrist_width/2;f=forearm_extension;
 for(y=[-f*.54,palm_length*.36],side=[-1,1]){
   px=side*(y<0?r*.94:w*.91);
   translate(P([px,y])) circle(d=3.3);
 }
}
module island_anchors2d(){
 y=palm_length*.48;
 for(x=[-main_mount_width/2+4,main_mount_width/2-4],
     dy=[-main_mount_length/2+4,main_mount_length/2-4]){
   bone([x,y+dy],[x*1.45,y+dy+(dy<0?-8:8)],branch_width);
   n([x,y+dy],9);
 }
 for(dy=[-joystick_mount_diameter*.28,joystick_mount_diameter*.28]){
   n([palm_width/2+thumb_reach*.45,palm_length*.80+dy],8);
   bone([palm_width/2+thumb_reach*.45,palm_length*.80+dy],
        [palm_width*.46,palm_length*.77+dy],branch_width);
 }
}
module anchor_holes2d(){
 y=palm_length*.48;
 for(x=[-main_mount_width/2+4,main_mount_width/2-4],
     dy=[-main_mount_length/2+4,main_mount_length/2-4])
    translate(P([x,y+dy])) circle(d=mount_hole_diameter);
 for(dy=[-joystick_mount_diameter*.28,joystick_mount_diameter*.28])
    translate(P([palm_width/2+thumb_reach*.45,palm_length*.80+dy]))
       circle(d=mount_hole_diameter);
}
module tpu_mesh(){
 linear_extrude(mesh_thickness)
 difference(){union(){veins2d();island_anchors2d();}
 fastener_holes2d();anchor_holes2d();}
}
module main_plate(){
 difference(){
 linear_extrude(petg_thickness) hull()
  for(x=[-main_mount_width/2+4,main_mount_width/2-4],
      y=[-main_mount_length/2+4,main_mount_length/2-4])
    translate([x,y]) circle(r=4);
 for(x=[-main_mount_width/2+4,main_mount_width/2-4],
     y=[-main_mount_length/2+4,main_mount_length/2-4])
    translate([x,y,-.1]) cylinder(h=petg_thickness+.2,d=mount_hole_diameter);
 }
}
module joystick_plate(){
 difference(){
 linear_extrude(petg_thickness) hull(){
  translate([0,-joystick_mount_diameter*.28]) circle(d=9);
  translate([0,joystick_mount_diameter*.28]) circle(d=9);
 }
 for(y=[-joystick_mount_diameter*.28,joystick_mount_diameter*.28])
  translate([0,y,-.1]) cylinder(d=mount_hole_diameter,h=petg_thickness+.2);
 }
}
if(part=="tpu") tpu_mesh();
else if(part=="petg_main") main_plate();
else if(part=="petg_joystick") joystick_plate();
else{
 tpu_mesh();
 translate([palm_width+thumb_reach+30,0,0]) main_plate();
 translate([palm_width+thumb_reach+30,-palm_length*.5,0]) joystick_plate();
}
