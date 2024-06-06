# -*- coding: utf-8 -*-
"""
Created on Thu Dec 23 23:43:23 2021

@author: Jlang
"""

import numpy as np
from vec_defs import *

class Hit_record():
    def __init__(self, p=None, normal=None, t=None, front_face=None, material=None):
        self.p = p
        self.normal = normal
        self.t = t
        self.front_face = front_face
        self.material = material
        
    def set_face_normal(self, ray, outward_normal):
        self.front_face = np.dot(ray.direction, outward_normal) < 0
        self.normal = outward_normal if self.front_face else -outward_normal
        
    def copy_other(self, other):
        self.__dict__.update(other.__dict__)

class Ray(): 
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction
    
    def __call__(self, t):
        return self.origin + t*self.direction

class Camera():
    def __init__(self, vfov=90, aspect=16/9, lookfrom=np.zeros(3), lookat=np.array([0,0,-1]), 
                 vup=np.array([0,1,0]), aperture=0.1, focus_dist=1.0):
        self.vfov = vfov*np.pi/180
        self.h = np.tan(self.vfov/2)
        self.aspect = aspect
        self.viewport_height = 2.0 * self.h
        self.viewport_width = self.viewport_height * self.aspect
        
        self.w = unit_vec(lookfrom - lookat)
        self.u = unit_vec(np.cross(vup, self.w))
        self.v = np.cross(self.w, self.u)
        
        self.origin = lookfrom
        self.horizontal = self.viewport_width * self.u
        self.vertical = self.viewport_height * self.v
        self.lower_left = self.origin - self.horizontal/2 - self.vertical/2 - focus_dist*self.w
        
        self.lens_radius = aperture/2
    
    def get_ray(self, u, v):
        rd = self.lens_radius * random_in_disk()
        offset = self.u * rd[0] + self.v * rd[1]
        return Ray(self.origin + offset,
                   self.lower_left + u*self.horizontal + v*self.vertical - self.origin - offset)

def ray_colour(r, world, depth=10):
    rec = Hit_record()
    
    if depth <= 0:
        return np.zeros(3)
    
    if world.hit(r, 0.001, np.infty, rec):
        has_hit, scatter_ray, attenuation = rec.material.scatter(r, rec)
        if has_hit:
            return attenuation*ray_colour(scatter_ray, world, depth-1)
        return np.zeros(3)
    
    u_direction = unit_vec(r.direction)
    t = 0.5*(u_direction[1] + 1)
    return (1-t)*np.array([1,1,1]) + t*np.array([0.5, 0.7, 1.0])
