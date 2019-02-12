# stmfile generator
from PIL import Image, ImageDraw
import numpy as np
import cv2
from itertools import product
from myfunc import coord, rrange
from myfunc import Squarewave2d
import json
import math
# meta settings
NOCONVERT = False
NOMOVIE = True
dirname = "ex6"
## settings
# array scale
width = 20
height = 20
class GaussianDistribution:
    def __init__(self,center,sigma,A,hexagonal=True,sup=1e9):
        # default coordinate axis is hexagonal axis(ommatidia)
        # but in the class, position is set as orthogonal axis
        if hexagonal is True:
            position=self.toorthogonal(center)
        else:
            position=center
        self.center = position
        self.sigma = sigma
        self.A = A
        self.sup = sup
    def getCenter(self):
        position = [self.center[0]*2/math.sqrt(3),self.center[1]-self.center[0]*math.sqrt(3)]
        return position
    def getSigma(self):
        return self.sigma
    def getA(self):
        return self.A
    def getSup(self):
        return self.sup
    def setCenter(self,pos,hexagonal=True):
        if hexagonal is True:
            position=self.toorthogonal(pos)
        else:
            position=pos
        self.center = position
    def getValue(self,pos,hexagonal=True):
        pos=self.toorthogonal(pos)
        dist = math.pow((pos[0]-self.center[0]),2)+math.pow((pos[1]-self.center[1]),2)
        return self.saturation(math.exp(-dist/2/math.pow(self.sigma,2))*self.A)
    def toorthogonal(self,pos):
        return [pos[0]*math.sqrt(3)/2.0,pos[0]/2.0+pos[1]]
    def saturation(self,value):
        if value >= self.sup:
            return self.sup
        else:
            return value

def ObjectPosition(t):
    # generate position of Object
    zeroposition= [10,10]
    leftposition=[5,10]
    rightposition=[15,10]
    upposition=[10,5]
    downposition=[10,15]
    if t>=0 and t<1000:
        return [zeroposition[0]*(1000-t)/1000.0+upposition[0]*t/1000.0,zeroposition[1]*(1000-t)/1000.0+upposition[1]*t/1000.0]
    if t>=1000 and t<1200:
        return upposition
    if t>=1200 and t<2200:
        return [upposition[0]*(2200-t)/1000.0+downposition[0]*(t-1200)/1000.0,upposition[1]*(2200-t)/1000.0+downposition[1]*(t-1200)/1000.0]
    if t>=2200 and t<2400:
        return downposition
    if t>=2400 and t<3400:
        return [downposition[0]*(3400-t)/1000.0+leftposition[0]*(t-2400)/1000.0,downposition[1]*(3400-t)/1000.0+leftposition[1]*(t-2400)/1000.0]
    if t>=3400 and t<3600:
        return leftposition
    if t>=3600 and t<4600:
        return [leftposition[0]*(4600-t)/1000.0+rightposition[0]*(t-3600)/1000.0,leftposition[1]*(4600-t)/1000.0+rightposition[1]*(t-3600)/1000.0]
    if t>=4600:
        return rightposition

# comvert array to stmfile
if NOCONVERT is False:
    stims = []
    for x,y in product(range(width),range(height)):
        stim = {}
        stim["stimulator"] = "IClamp"
        stim["target_cellname"] = "R1-6" + "," + str(x) + "," + str(y)
        stim["section"] = {"name":"axon","point":0.5}
        stim["opt"] = {}
        stim["opt"]["del"] = 0
        stim["opt"]["dur"] = 1e9
        stim["opt"]["amp"] = {}
        stim["opt"]["amp"]["time"] = [i for i in range(0,5100)]
        stim["opt"]["amp"]["continuous"] = 1
        value = []
        GD = GaussianDistribution([0,0],2,3,sup=1)
        for t in stim["opt"]["amp"]["time"]:
            GD.setCenter(ObjectPosition(t))
            value.append(GD.getValue([x,y]))
        stim["opt"]["amp"]["value"] = value
        stims.append(stim)
with open("./"+ dirname + "/stm_3.json","w") as f:
    json.dump(stims,f)
