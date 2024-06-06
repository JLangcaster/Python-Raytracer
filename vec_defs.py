# -*- coding: utf-8 -*-
"""
Created on Thu Dec 23 23:33:27 2021

@author: Jlang
"""

import numpy as np

def norm2(v):
    return np.dot(v, v)

def norm(v):
    return np.sqrt(norm2(v))

def unit_vec(v):
    return v/norm(v)

def random_in_sphere():
    while True:
        candidate = 2*np.random.rand(3)-1
        if norm2(candidate)<1:
            return candidate

def random_on_sphere():
    return unit_vec(random_in_sphere())

def random_in_disk():
    while True:
        candidate = 2*np.random.rand(2)-1
        if norm2(candidate)<1:
            return candidate

def reflect(v, n):
    return v - 2*np.dot(v,n)*n

def refract(v, n, rr):
    cos_theta = min(np.dot(-v, n), 1)
    r_out_perp = rr * (v + cos_theta * n)
    r_out_para = -np.sqrt(1-norm2(r_out_perp))*n
    return r_out_para + r_out_perp