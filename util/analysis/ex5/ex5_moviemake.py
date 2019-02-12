# stmfile generator
from PIL import Image, ImageDraw
import numpy as np
import cv2
from itertools import product
import json
import math
import copy
import sys
import os
import pickle
# meta settings
NOCONVERT = False
NOMOVIE = True
dirname = "ex5/result"
Networklist = [["R1-6",-50,10.0],["T4a",-60,30.0],["T4b",-60,8.0],["T4c",-55,5],["T4d",-60,5.0]]
## settings
# array scale
width = 10
height = 10
hex_size = 15
hexarray = np.zeros((width,height))
stim_offset=100
stim_duration=3000
fps=60
total_frame = (stim_offset + stim_duration) / 1000.0 * fps
dataformovie = {}
def coord(x,y):
    w=100+x*math.sqrt(3)/2.0
    h =100+ x/2.0+y
    return w,h

def walk_files_with(extension, directory='.'):
    filelist = []
    for root, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            if filename.lower().endswith('.' + extension):
                filelist.append(os.path.join(root, filename))
    return filelist

if not len(sys.argv) == 2:
    print("this program requires 1 argument (filepath)")
    exit()

root_dir = sys.argv[1]
directories = []
for x in os.listdir(root_dir):
    if os.path.isdir(root_dir + x):
        directories.append(x)
for i,dir in enumerate(directories):
    files = []
    files = walk_files_with('pickle',root_dir + dir)
    runsrc = walk_files_with('json',root_dir + dir)
    with open(runsrc[0],"r") as F:
        json_run = json.load(F)
    print(json_run)
    for f in files:
        with open(f, mode='rb') as F:
            data = pickle.load(F)
        r_v_list = data["results"]["r_v_list"]
        t = data['results']['t']
        vsum = np.zeros(len(t))
        counter = 0
        dataformovie["t"]=t
        for r_v in r_v_list:
            v = r_v[1]
            if r_v[0]["target_cellname"].startswith("R1-6") or r_v[0]["target_cellname"].startswith("T4"):
                dataformovie[r_v[0]["target_cellname"]]=copy.deepcopy(v)
    os.mkdir("./"+dirname+"/"+dir)
    for Net in Networklist:
        filename = Net[0]
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter('./' + dirname +"/"+dir+  '/' + filename + '.avi',fourcc,fps,(480,480),False)
        for t in range(int(total_frame)):
            im_gray = np.zeros((480,480), dtype = 'uint8')
	    time = t/60.0*1000
            for x,y in product(range(width),range(height)):
                hexarray[x,y] = dataformovie[filename+","+str(x)+','+str(y)][np.abs(dataformovie['t']-time).argmin()]
                hexarray[x,y] = (hexarray[x,y]-Net[1])/Net[2]
		if hexarray[x,y] < 0:
		    hexarray[x,y]=0
		if hexarray[x,y] > 1:
		    hexarray[x,y]=1
                xx,yy = coord(x*hex_size,y*hex_size)
            #draw.ellipse((int(xx),int(yy),int(xx+hex_size),int(yy+hex_size)), fill=(int(255 * hexarray[x,y]),int(255 * hexarray[x,y]),int(255 * hexarray[x,y])), outline=(0,0,0))
                for dx,dy in product(range(int(xx),int(xx+hex_size)), range(int(yy),int(yy+hex_size))):
                    if (dx - xx - hex_size/2)**2 + (dy - yy - hex_size/2)**2 <= (hex_size/2)**2:
                        im_gray[dy,dx] = int(200 * hexarray[x,y] + 55)
            out.write(im_gray)
        out.release()

