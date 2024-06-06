# -*- coding: utf-8 -*-
"""
Created on Fri Dec 24 00:18:11 2021

@author: Jlang
"""
from vec_defs import *
from ray_defs import *
from material_defs import *
import numpy as np    

class Hittable():
    def __init__(self):
        pass
    
    def hit():
        pass

class Sphere(Hittable):
    def __init__(self, centre, radius, material):
        self.centre = centre
        self.radius = radius
        self.material = material
        
    def hit(self, ray, t_min, t_max, rec):
        oc = ray.origin - self.centre
        a = norm2(ray.direction)
        half_b = np.dot(oc, ray.direction)
        c = norm2(oc) - self.radius*self.radius
        discriminant = half_b*half_b - a*c
        
        if discriminant<0:
            return False
        
        sqrtd = np.sqrt(discriminant)
        
        root = (-half_b - sqrtd)/a
        if (root < t_min) or (t_max < root):
            root = (-half_b - sqrtd)/a
            if (root < t_min) or (t_max < root):
                return False
        
        rec.t = root
        rec.p = ray(root)
        outward_normal = (rec.p - self.centre)/self.radius
        rec.set_face_normal(ray, outward_normal)
        rec.material = self.material
        return True

class Hittable_list(Hittable):
    def __init__(self, items=[]):
        self.items = items
    
    def clear(self):
        self.items = []
    
    def append(self, item):
        self.items.append(item)
    
    def hit(self, ray, t_min, t_max, rec):
        temp_rec = Hit_record()
        hit_anything = False
        closest_so_far = t_max
        
        for item in self.items:
            if item.hit(ray, t_min, closest_so_far, temp_rec):
                hit_anything = True
                closest_so_far = temp_rec.t
                '''
                rec.t = temp_rec.t
                rec.normal = temp_rec.normal
                rec.p = temp_rec.p
                rec.front_face = temp_rec.front_face
                '''
                rec.copy_other(temp_rec)
        
        return hit_anything

class Random_world(Hittable_list):
    def __init__(self, num_spheres=21):
        self.items = []
        ground_material = Lambertian(np.array([0.5, 0.5, 0.5]))
        self.items.append(Sphere(np.array([0,-1000,0]),1000,ground_material))
        
        for a in range(-num_spheres//2, num_spheres//2+1):
            for b in range(-num_spheres//2, num_spheres//2+1):
                rand = np.random.rand(3)
                centre = np.array([a + 0.9*rand[0], 0.2, b + 0.9*rand[1]])
                
                if norm(centre - np.array([4,0.2,0]))>0.9:
                    if rand[2] < 0.8:
                        albedo = np.random.rand(3)*np.random.rand(3)
                        sphere_material = Lambertian(albedo)
                    elif rand[2] < 0.95:
                        albedo = np.random.rand(3)/2 + 0.5
                        fuzz = np.random.rand(1)/2
                        sphere_material = Metal(albedo, fuzz)
                    else:
                        sphere_material = Dielectric(1.5)
                    self.items.append(Sphere(centre, 0.2, sphere_material))
        