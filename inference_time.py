#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 24 16:06:20 2021

@author: alicetsai
"""
import numpy as np

time = []

try:
    file = open("result.txt","r")
    for line in file.readlines():
        line = line.strip()
        lines = line.split(" ")
        if len(lines)>4 and lines[4] == "milli-seconds.":
            time.append(float(lines[3]))
    print("Inference average time : %f" %np.average(time))
    
            
    
except IOError:
    print("File not found or path is incorrect")
finally:
    print("Inference Done!")