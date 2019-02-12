import sys
import os.path
import numpy as np
import matplotlib.pyplot as plt
sys.path.append("/home/hayato/lib/python")
sys.path.append("./modules")
import argparse
import pickle
import cv2

def walk_files_with(extension, directory='.'):
    """Generate paths of all files that has specific extension in a directory.

    Arguments:
    extension -- [str] File extension without dot to find out
    directory -- [str] Path to target directory

    Return:
    filepath -- [str] Path to file found
    """
    filelist = []
    for root, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            if filename.lower().endswith('.' + extension):
                filelist.append(os.path.join(root, filename))
    return filelist

def satuation(x):
    if x > 255:
        return 255
    elif x < 0:
        return 0
    else:
        return x


width = 10
height = 30
framerate = 60
min = -66
max = -59

if not len(sys.argv) == 2:
    print("this program requires 1 argument (filepath)")
    exit()

root_dir = sys.argv[1]
files = []
files = walk_files_with('pickle',root_dir)

name, ext = os.path.splitext(files[0])
filename = name + '.avi'

rec = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*'XVID'), framerate, (width,height), False)
im_gray = np.zeros((height,width), dtype = 'uint8')
vlist = []
for f in files:
    with open(f, mode='rb') as F:
        data = pickle.load(F)
        print(data)
        r_v_list = data['results']['r_v_list']
        t = data['results']['t']
        dataps = int(1 / (t[1] - t[0]) * 1000)
        if dataps < framerate:
            framerate = dataps
        vlist.extend(r_v_list)

for t in range(0, len(vlist[0][1]), int(dataps/framerate)):
    for v_list in vlist:
        w = v_list[0] % width
        h = int(v_list[0] / width)
        print(h,w,t)
        im_gray[h,w] = satuation(int(255 * (v_list[1][t]-min)/(max-min)))
    rec.write(im_gray)
rec.release()
