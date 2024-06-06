# -*- coding: utf-8 -*-
"""
Created on Fri Dec 24 01:19:46 2021

@author: Jlang
"""

import numpy as np

def clamp(value, lo, hi):
    if value < lo:
        return lo
    elif value > hi:
        return hi
    else:
        return value