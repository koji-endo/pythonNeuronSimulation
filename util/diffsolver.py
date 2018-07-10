import numpy as np
import matplotlib.pyplot as plt
import math
import time
import copy
# parameters
gkbar = 2 * 10e-3
gcabar = 1.1 * 10e-3
gl = 0.5 * 10e-3
el = -0.05
v1 = -0.0012
v2 = 0.018
v3 = -0.03
v4 = 0.01
b  = 0.02 * 10e-3
phi = 0.01
eca = 0.1
ek = -0.07
tau = 0.8
C= 2 * 10e-6
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
plt.subplot(2,2,1)
plt.plot(vlist, vnull)
plt.plot(vlist, nnull)
plt.title("nullcline")
# solve diff-eq with Runge-kutta
def Mss(v):
    return 0.5 * (1+math.tanh((v-v1)/v2))
def Nss(v):
    return 0.5 * (1+math.tanh((v-v3)/v4))
def Tn(v):
    return (phi * math.cosh((v-v3)/(2*v4)))
def vdiff(i,v,n):
    print(Mss(v),Nss(v),Tn(v))
    f =(b - i - gl*(v-el) - gcabar * Mss(v) * (v-eca) - gkbar * n *(v-ek)) / C
    print(f)
    return f
def ndiff(v,n):
    f = (Nss(v) - n) * Tn(v)
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

dt = 0.0005
t = [i/2000.0 for i in range(0,2000,1)]
ilist = np.zeros((2001))
current1 = [0.001 for i in range(0,200)]
current2 = [-0.001 for i in range(0,200)]
current3 = [-0.0015 for i in range(0,200)]

ilist[200:400] = copy.deepcopy(current1)
ilist[600:800] = copy.deepcopy(current2)
ilist[1000:1200] = copy.deepcopy(current3)

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

plt.subplot(2,2,4)
plt.plot(t, vlist)
plt.title("v value")

plt.subplot(2,2,2)
plt.plot(t, ilist)
plt.title("i")

plt.subplot(2,2,3)
plt.plot(t, nlist)

plt.title("n value")

plt.tight_layout()
plt.show()
