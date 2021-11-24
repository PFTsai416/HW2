#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 17 14:46:24 2021

@author: alicetsai
"""
import h5py
import numpy as np

data_path = "./train/digitStruct.mat"
f = h5py.File(data_path,'r')


digitStructName = f['digitStruct']['name']
digitStructBbx = f['digitStruct']['bbox']

def getName(n):
    name = ''.join([chr(v[0]) for v in f[(digitStructName[n][0])]])
    return name

def bboxHelper(attr):
    if len(attr)>1 :
        attr = [f[attr[j].item()][0][0] for j in range(len(attr))]
    else:
        attr = [attr[0][0]]
    return attr

def getBbox(n):
    bbox = {}
    bb = digitStructBbx[n].item()
    bbox['height'] = bboxHelper(f[bb]['height'])
    bbox['width'] = bboxHelper(f[bb]['width'])
    bbox['label'] = bboxHelper(f[bb]['label'])
    bbox['left'] = bboxHelper(f[bb]['left'])
    bbox['top'] = bboxHelper(f[bb]['top'])
    return bbox

image_dict = {}
for i in range(len(digitStructName)):
    image_dict[getName(i)] = getBbox(i)
    
##### create train.txt to include /train/*.png ######
with open('./train.txt', 'w') as f:
    for i in range(len(digitStructName)):
        if i==len(digitStructName)-1:
            f.write("../data/train/"+str(i+1)+".png")
        else:
            f.write("../data/train/"+str(i+1)+".png\n")

##### create each file as ***.txt file ######
from PIL import Image
for i in range(len(digitStructBbx)):
    img = Image.open('./train/'+str(i+1)+'.png')
    img_w = img.size[0]
    img_h = img.size[1]
    
    total = len(image_dict[str(i+1)+'.png']['height'])
    bbx = image_dict[str(i+1)+'.png']
    with open('./train/'+str(i+1)+'.txt','w') as f:
        for j in range(len(bbx['height'])):
            x = round((bbx['left'][j]+bbx['width'][j]/2)/img_w,4)
            y = round((bbx['top'][j]+bbx['height'][j]/2)/img_h,4)
            w = round(bbx['width'][j]/img_w,4)
            h = round(bbx['height'][j]/img_h,4)
            label = int(bbx['label'][j])
            if label == 10 : 
                f.write(str(0)+" "+str(x)+" "+str(y)+" "+str(w)+" "+str(h)+"\n")
            else:
                f.write(str(label)+" "+str(x)+" "+str(y)+" "+str(w)+" "+str(h)+"\n")
    

#### create test.txt to include /test/*.png  #####
import os

test_file = os.listdir('./test')
with open('./test.txt','w') as f:
    for i in range(len(test_file)):
        if i==len(test_file)-1:
            f.write("../data/test/"+test_file[i])
        else:
            f.write("../data/test/"+test_file[i]+"\n")
        


    