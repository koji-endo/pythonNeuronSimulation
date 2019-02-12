# stmfile generator
import numpy as np
from itertools import product
from math import *


def coord(x,y):
    w = x * 1.732 / 2
    h = x * 0.5 + y
    return w, h

def rrange(start, end, step=1):
    if (end-start) * step <= 0:
        print("sign of end - start must be match sign of step")
        exit()
    else:
        li = []
        n = start
        if end - start > 0:
            while n < end:
                li.append(n)
                n = n+step
        elif end - start < 0:
            while n > end:
                li.append(n)
                n = n+step
        return li


class Squarewave2d():
    def __init__(self, tf, sf, bold, direction, power):
        self.tf = tf
        self.sf = sf
        self.bold = bold
        self.direction = direction
        self.power = power
        self.dv = np.array((cos(radians(self.direction)), sin(radians(self.direction))))
        if self.bold > 1/self.sf:
            print("WARNING: wave boldness is larger than wavelength")

    def peaktiming(self, x, y):
        w,h = coord(x,y)
        p = np.array((w, h))
        mapp = np.dot(self.dv,p)
        modmap = fmod(mapp,1.0/self.sf)
        if modmap < 0:
            modmap += 1.0/self.sf
        v = self.tf / self.sf
        return (modmap-self.bold/2)/v, (modmap+self.bold/2)/v, 1.0/self.tf

    def waveheight0(self, x, y):
        # position(x, y) must be coordinated. not hex record_position
        p = np.array((x, y))
        mapp = np.dot(self.dv,p)
        modmap = fmod(mapp,1/self.sf)
        if modmap < 0:
            modmap += 1/self.sf
        if modmap <= self.bold/2 or modmap >= 1/self.sf - self.bold/2:
            return self.power
        else:
            return 0
    def waveheightsin(self, x, y,t,amp,offset):
        # position(x, y) must be coordinated. not hex record_position
        p = np.array((x, y))
        st,en,pe = self.peaktiming(x,y)
        delay = (st + en)/2.0 * 1000.0
        frq = self.tf/1000.0
        return offset + amp * cos(2*pi*frq*(t - delay))

    def waveheightt(self, x, y, t):
        return self.waveheight0(x - (t * self.tf * self.dv[0])/(1000 * self.sf), y - (t * self.tf * self.dv[1])/(1000 * self.sf))

    def waveheighthex(self, x, y, t):
        w,h = coord(x,y)
        return self.waveheightt(w,h,t)

    def waveheightave(self, x, y, t, method="weighted"):
        if method == "weighted":
            weightlist = [2.0,1.0,1.0,1.0,1.0,1.0,1.0]
        waveheight = 0
        waveheight += self.waveheighthex(x,y,t) * weightlist[0]
        waveheight += self.waveheighthex(x+0.5,y-0.5,t) * weightlist[2]
        waveheight += self.waveheighthex(x+0.5,y,t) * weightlist[1]
        waveheight += self.waveheighthex(x,y-0.5,t) * weightlist[3]
        waveheight += self.waveheighthex(x-0.5,y,t) * weightlist[4]
        waveheight += self.waveheighthex(x-0.5,y+0.5,t) * weightlist[5]
        waveheight += self.waveheighthex(x,y+0.5,t) * weightlist[6]
        return waveheight /sum(weightlist)

    def settf(self, tf):
        self.tf = tf
    def setsf(self, sf):
        self.sf = sf
    def setbold(self, bold):
        self.bold = bold
    def settf(self, direction):
        self.direction = direction
        self.dv = np.array((cos(radians(self.direction)), sin(radians(self.direction))))
    def settf(self, power):
        self.power = power
