# nwkfile generator
from PIL import Image
import numpy as np
import cv2
from itertools import product

# meta settings
filepath = "./retina_l1l2.nwk"
# settings
width = 10
height = 10
nwklist = [[0,1,"convolute"],[0,2,"convolute"]]
# making arrays
conlist = []
for nwk in nwklist:
    if nwk[2] == "convolute":
        for h,w in product(range(height),range(width)):
            for dy,dx in product(range(3),range(3)):
                superx = w + dx-1
                supery = h + dy-1
                if superx >=0 and supery >= 0 and superx < width and supery < height:
                    target = nwk[1] * 100 + h * width + w
                    source = nwk[0] * 100 + supery * width + superx
                    conlist.append([source,target])

# comvert array to stmfile
print(conlist)
f = open(filepath, 'w')
for con in conlist:
    f.write(str(con[0])+','+str(con[1])+'\n')
f.close()
