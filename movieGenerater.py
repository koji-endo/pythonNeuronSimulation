import sys
import os.path
import numpy as np
import matplotlib.pyplot as plt
sys.path.append("/home/hayato/lib/python")
sys.path.append("./modules")
import argparse
import pickle
import cv2

width = 10
height = 6
framerate = 60
min = -77
max = -60

if not len(sys.argv) == 2:
    print("this program requires 1 argument (filepath)")
    exit()

with open(sys.argv[1], mode='rb') as f:
    data = pickle.load(f)
print(data)
r_v_list = data['results']['r_v_list']
t = data['results']['t']
if len(r_v_list) != width * height:
    print("Error: inconsistent length of data to width and height")
    exit()
dataps = int(1 / (t[1] - t[0]) * 1000)
print(dataps)
if dataps < framerate:
    framerate = dataps
name, ext = os.path.splitext(sys.argv[1])
filename = name + '.avi'
rec = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*'XVID'), framerate, (width,height), False)
im_gray = np.zeros((height,width), dtype = 'uint8')
print(im_gray.shape)
print(len(r_v_list[0]))
for t in range(0, len(r_v_list[0]), int(dataps/framerate)):
    for i,v_list in enumerate(r_v_list):
            w = i % width
            h = int(i / width)
            im_gray[h,w] = int(255 * (v_list[t]-min)/(max-min))
    rec.write(im_gray)
rec.release()
