# -*- coding: utf-8 -*-
"""
Created on Fri Dec 24 02:18:52 2021

@author: Jlang
"""

import numpy as np
from vec_defs import *
from ray_defs import *

class Material():
    def __init__(self):
        pass

class Lambertian(Material):
    def __init__(self, albedo):
        self.albedo = albedo
    
    def scatter(self, r_in, rec):
        scatter_direction = rec.normal + random_on_sphere()
        
        if all(scatter_direction < 1e-8):
            scatter_direction = rec.normal
        
        scatter_ray = Ray(rec.p, scatter_direction)
        attenuation = self.albedo
        
        return True, scatter_ray, attenuation

class Metal(Material):
    def __init__(self, albedo, fuzziness=0):
        self.albedo = albedo
        self.fuzz = fuzziness
    
    def scatter(self, r_in, rec):
        reflected = reflect(unit_vec(r_in.direction), rec.normal)
        scatter_ray = Ray(rec.p, reflected + self.fuzz * random_on_sphere())
        attenuation = self.albedo
        
        return (np.dot(scatter_ray.direction, rec.normal)>0), scatter_ray, attenuation

class Dielectric(Material):
    def __init__(self, index_of_refraction):
        self.ir = index_of_refraction
        
    def scatter(self, r_in, rec):
        attenuation = np.ones(3)
        refractive_ratio = 1/self.ir if rec.front_face else self.ir
        
        unit_direction = unit_vec(r_in.direction)
        cos_theta = min(np.dot(-unit_direction, rec.normal), 1)
        sin_theta = np.sqrt(1 - cos_theta*cos_theta)
        
        cannot_refract = refractive_ratio*sin_theta > 1.0
        
        if cannot_refract or (self.reflectance(cos_theta, refractive_ratio) > np.random.rand()):
            direction = reflect(unit_direction, rec.normal)
        else:
            direction = refract(unit_direction, rec.normal, refractive_ratio)
        
        scatter_ray = Ray(rec.p, direction)
        
        return True, scatter_ray, attenuation
    
    def reflectance(self, cosine, ref_index):
        r0 = (1-ref_index)/(1+ref_index)
        r0 = r0*r0
        result = r0 + (1-r0) * ((1-cosine)**5)
        return result