# stmfile generator
from PIL import Image, ImageDraw
import numpy as np
import cv2
from itertools import product
from myfunc import coord, rrange
from myfunc import Squarewave2d
import json
# meta settings
NOCONVERT = False
NOMOVIE = True
dirname = "ex3/stmdata"
## settings
# array scale
width = 10
height = 10

timefreqlist = [1.0]
spatialfreqlist = [3.0/16]
boldness_list = [0.1]
direction_list = [0,30,60,90,120,150,180,210,240,270,300,330]
for tfreq,sfreq,bness,dtion in product(timefreqlist,spatialfreqlist,boldness_list,direction_list):
    # horizontal = X * 1.73/2, vertical = X * 1/2 + Y
    # timefrequency(hz/s), spatialfrequency (hz/ommatidium) = 1/wqavelength
    # stim
    # direction(degree from x axis), offset(ms), duration(ommatidium), power(uA)
    timefreq = tfreq
    spatialfreq = sfreq
    stim_bold = bness
    stim_direction = dtion
    stim_offset = 100
    stim_duration = 5000
    stim_power = 1.0
    idx = spatialfreqlist.index(spatialfreq) + 1
    #filename = "tf" + str(timefreq)+ "sf"+ str(spatialfreq)+"bold"+str(stim_bold)+ "direct"+str(stim_direction)
    filename = "direct"+ str(stim_direction)
    # movie setting
    # hex_size is radius of an ommatidium
    hex_size = 15
    fps = 60

    SW = Squarewave2d(timefreq,spatialfreq,stim_bold,stim_direction,stim_power)

    hexarray = np.zeros((width,height))

    #for x,y in product(range(width),range(height)):
    #    hexarray[x,y] = SW.waveheightave(x,y,0)
    #    print("hexarray={}".format(hexarray[x,y]))
    #    xx,yy = coord(x*hex_size,y*hex_size)
    #    draw.ellipse((int(xx),int(yy),int(xx+hex_size),int(yy+hex_size)), fill=(int(255 * hexarray[x,y]),int(255 * hexarray[x,y]),int(255 * hexarray[x,y])), outline=(0,0,0))
    #im.save("result.png")
    #exit()

    total_frame = (stim_offset + stim_duration) / 1000.0 * fps

    # generate movie
    if NOMOVIE is False:
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter('./' + dirname + '/' + filename + '.avi',fourcc,fps,(480,480),False)
        for t in range(int(total_frame)):
            im_gray = np.zeros((480,480), dtype = 'uint8')
            for x,y in product(range(width),range(height)):
                hexarray[x,y] = SW.waveheightave(x,y,t * 1000.0 / fps)
    #            print(hexarray[x,y])
                xx,yy = coord(x*hex_size,y*hex_size)
                #draw.ellipse((int(xx),int(yy),int(xx+hex_size),int(yy+hex_size)), fill=(int(255 * hexarray[x,y]),int(255 * hexarray[x,y]),int(255 * hexarray[x,y])), outline=(0,0,0))
                for dx,dy in product(range(int(xx),int(xx+hex_size)), range(int(yy),int(yy+hex_size))):
                    if (dx - xx - hex_size/2)**2 + (dy - yy - hex_size/2)**2 <= (hex_size/2)**2:
                        im_gray[dy,dx] = int(255 * hexarray[x,y])
    #        print(im_gray)
    #        exit()
            out.write(im_gray)
        out.release()

    # comvert array to stmfile
    if NOCONVERT is False:
        stims = []
        for x,y in product(range(width),range(height)):
            start,end,period = SW.peaktiming(x,y)
            stim = {}
            stim["stimulator"] = "SinCurrent"
            stim["target_cellname"] = "R1-6" + "," + str(x) + "," + str(y)
            stim["section"] = {"name":"axon","point":0.5}
            stim["opt"] = {}
            stim["opt"]["st"] = 100
            stim["opt"]["en"] = 5100
            stim["opt"]["amp"] = 0.5
            stim["opt"]["offset"] = 0.5
            stim["opt"]["delay"] = (start + end)/2.0 * 1000
            stim["opt"]["freqency"] = tfreq/1000.0
            stims.append(stim)

    with open("./"+ dirname + '/' + filename +"_stm.json","w") as f:
        json.dump(stims,f)
