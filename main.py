# -*- coding: utf-8 -*-
"""
Created on Thu Dec 23 23:16:52 2021

@author: Jlang
"""
import numpy as np
from vec_defs import *
from colour_defs import *
from ray_defs import *
from material_defs import *
from hittable_defs import *

aspect = 3/2
image_width = 120
image_height = int(image_width / aspect)
samples_per_pixel = 10
max_depth = 50

lookfrom = np.array([13,2,3])
lookat = np.array([0,0,0])
dist_to_focus = 10
aperture = 0.1

world = Random_world(6)

material_centre = Lambertian(np.array([0.7, 0.3, 0.3]))
#material_left = Metal(np.array([0.8, 0.8, 0.8]), 0.1)
#material_centre = Dielectric(1.5)
material_left = Dielectric(1.5)
material_right = Metal(np.array([0.6, 0.6, 0.2]), 0.3)

world.append(Sphere(np.array([0,0,-1]), 0.5, material_centre))
world.append(Sphere(np.array([-1,0,-1]), 0.5, material_left))
world.append(Sphere(np.array([-1,0,-1]), -0.45, material_left))
world.append(Sphere(np.array([1,0,-1]), 0.5, material_right))

cam = Camera(20, 16/9, lookfrom=np.array([-2,2,1]), lookat=lookat, 
             aperture=aperture, focus_dist=dist_to_focus)

out_string = "P3\n{} {}\n255\n".format(image_width, image_height)

for j in range(image_height-1, -1, -1):
    print("\rScanlines left: {}".format(j))
    for i in range(0, image_width):
        pixel_colour = np.zeros(3)
        for s in range(0, samples_per_pixel):
            u = (i+np.random.rand()) / (image_width - 1)
            v = (j+np.random.rand()) / (image_height - 1)
            ray = cam.get_ray(u, v)
            pixel_colour += ray_colour(ray, world, max_depth)
        out_string += write_colour(pixel_colour, samples_per_pixel)
print("\rDone")

with open("image.ppm", "w") as op:
    op.write(out_string)
    op.close()