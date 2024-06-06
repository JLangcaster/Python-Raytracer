# -*- coding: utf-8 -*-
"""
Created on Thu Dec 23 23:37:41 2021

@author: Jlang
"""

import numpy as np

def write_colour(colour, samples_per_pixel):
    scale = 1/samples_per_pixel
    icolour = np.floor(255.999 * np.sqrt(colour * scale)).astype(int)
    return "{} {} {}\n".format(*icolour)