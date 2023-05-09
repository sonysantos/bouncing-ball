# from sys import exit
import bpy
from math import *

# objects
scene = bpy.data.scenes['Scene']
sphere = bpy.data.objects['Sphere']
camera = bpy.data.objects['Camera']

# initial positions & values
h0 = 1         # height position of sphere
c_dist = 3     # distance between camera and origin
radius = 0.12  # radius of sphere

sphere.location = (0, 0, h0)
sphere.rotation_euler = (pi/2, 0, pi/2)  # ZYX
sphere.scale = (radius, radius, radius)

camera.location = (0, -c_dist, h0/2)
camera.rotation_euler = (pi/2, 0, 0)

# definitions
falltime = 2

# helpers
pi2 = 2 * pi
falltime2 = falltime * 2
G = 2.0 * h0 / falltime ** 2

# initial and final frames
fps = scene.render.fps
scene.frame_start = 0
scene.frame_end = 8 * fps * falltime2
scene.frame_current = 0

# this will removal all 'frame_change_pre' handlers
bpy.app.handlers.frame_change_pre.clear()

def render_frame(scene):
    
    # time
    frame = scene.frame_current
    time = frame / fps
    
    # angles
    ball_angle = pi/2 - (time * pi / falltime2) % pi2
    camera_angle = -(time * pi/4 / falltime2) % pi2
    
    # height position of sphere
    h_time = time % falltime2
    if h_time > falltime:
        h_time -= falltime2
    h = h0 - G * h_time ** 2 / 2
    
    # smash
    if (h < radius):
        # vertical and horizontal scales
        vs = (h/radius) ** 2 / 2 + 0.5
        hs = 1 + (1 - vs) / 2
        
        sphere.scale = (radius * hs, radius * vs, radius * hs)
        
        # adjust h
        h = radius * vs
    else:
        sphere.scale = (radius, radius, radius)
    
    sphere.location[2] = h
    sphere.rotation_euler[2] = ball_angle
    
    camera.rotation_euler[2] = camera_angle
    camera.location[0] = c_dist * sin(camera_angle)
    camera.location[1] = -c_dist * cos(camera_angle)
    
bpy.app.handlers.frame_change_pre.append(render_frame)