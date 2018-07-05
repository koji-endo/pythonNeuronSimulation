import numpy as np
import matplotlib.pyplot as plt
import math
import time
import copy
# parameters
gkbar = 2
gcabar = 1.1
gl = 0.5
el = -0.05
v1 = -0.001
v2 = 0.015
v3 = -0.05
v4 = 0.001
b  = 0.02
phi = 0.0025
eca = 0.1
ek = -0.07
tau = 0.8
C= 1
# plot nullcline curve
def vnullcline(v):
    n = (b - gl*(v-el)-0.5 * gcabar * (1+math.tanh((v-v1)/v2))*(v-eca))/(gkbar * (v - ek))
    return n
def nnullcline(v):
    n = 0.5 * (1+math.tanh((v-v3)/v4))
    return n

vlist = range(-60,80,1)
vlist = [v / 1000.0 for v in vlist]
vnull = [vnullcline(v) for v in vlist]
nnull = [nnullcline(v) for v in vlist]
plt.subplot(3,1,1)
plt.plot(vlist, vnull)
plt.plot(vlist, nnull)
plt.title("nullcline")
# solve diff-eq with Runge-kutta
def Mss(v):
    return 0.5 * (1+math.tanh((v-v1)/v2))
def Nss(v):
    return 0.5 * (1+math.tanh((v-v3)/v4))
def Tn(v):
    return 1/(phi * math.cosh((v-v3)/(2*v4)))
def vdiff(i,v,n):
    print(Mss(v))
    f =(b - i - gl*(v-el) - gcabar * Mss(v) * (v-eca) - gkbar * n *(v-ek)) / C
    print(f)
    return f
def ndiff(v,n):
    f = (Nss(v) - n) / Tn(v)
    return f
def rksolver(v,n,dt,i):
    av = vdiff(i,v,n)
    an = ndiff(v,n)
    bv = vdiff(i,v + av * dt /2,n + an * dt/2)
    bn = ndiff(v + av * dt /2,n + an * dt/2)
    cv = vdiff(i,v + bv * dt /2,n + bn * dt/2)
    cn = ndiff(v + bv * dt /2,n + bn * dt/2)
    dv = vdiff(i,v + cv * dt,n + cn * dt)
    dn = ndiff(v + cv * dt,n + cn * dt)
    #print(av,bv,cv,dv,an,bn,cn,dn)
    v1 = v + dt / 6 * (av + 2*bv + 2*cv + dv)
    n1 = n + dt / 6 * (an + 2*bn + 2*cn + dn)
    return v1,n1

dt = 0.001
t = [i/1000.0 for i in range(0,1000,1)]
ilist = np.zeros((1001))
current1 = [-0.05 for i in range(0,100)]
current2 = [-0.1 for i in range(0,100)]
current3 = [-0.15 for i in range(0,100)]

ilist[100:200] = copy.deepcopy(current1)
ilist[300:400] = copy.deepcopy(current2)
ilist[500:600] = copy.deepcopy(current3)

vlist = [-0.05]
nlist = [0.5]

for i,tstep in enumerate(t):
    v = vlist[-1]
    n = nlist[-1]
    print(v,n)
    v1,n1 = rksolver(v,n,dt,ilist[i])
    vlist.append(v1)
    nlist.append(n1)
t.append(1)

plt.subplot(3,1,2)
plt.plot(t, vlist)
plt.plot(t, ilist)
plt.title("i and v value")

plt.subplot(3,1,3)
plt.plot(t, nlist)

plt.title("n value")

plt.tight_layout()
plt.show()
