#include "colors.inc"

// FPS = 30
// clock = 0 to 360 (camera angle)

#declare INITIAL_Y = 10;
#declare FALLTIME = 2;
#declare FALLTIME2 = FALLTIME * 2;

#declare G = 2 * INITIAL_Y / pow(FALLTIME, 2);

#declare Time = clock * FALLTIME2 / 45;
#declare Camera_Angle = mod(Time * 45 / FALLTIME2, 360);
#declare Ball_Angle = -mod(Time * 180 / FALLTIME2, 360);

#declare Time = mod(Time, FALLTIME2);
#if (Time > FALLTIME)
  #declare Time = Time - FALLTIME2;
#end
#declare Y = INITIAL_Y - G * pow(Time, 2) / 2;
#if (Y < 1)
  #declare Scale_Y = Y * Y / 2 + 0.5;
  #declare Scale_XZ = 1 + (1 - Scale_Y)/2;
  #declare Y = Scale_Y;
#else
  #declare Scale_Y = 1;
  #declare Scale_XZ = 1;
#end

background { color rgb <0.5, 0.7, 0.9> }

sphere {
  <0, 0, 0>, 1
  pigment { 
    image_map {
      png "ball.png"
      map_type 1
    }
  }
  finish {
    ambient .2
    diffuse .8
    phong 0.2
    phong_size 10
  }
  // must rotate in origin BEFORE translating!
  rotate <90, 0, Ball_Angle>
  scale <Scale_XZ, Scale_Y, Scale_XZ>
  translate <0, Y, 0>
}

plane {
  y, 0
  pigment {
    checker color White, color Black
  }
  finish {
    reflection 0.2
  }
  scale <2, 1, 2>
}

camera {
  right x*16/9
  location <0, 5, -15>
  look_at  <0, 5,  0>
  rotate <0, Camera_Angle, 0>
}

light_source { <-50, 50, -50> color White}