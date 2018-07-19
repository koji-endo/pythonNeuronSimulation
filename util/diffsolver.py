import numpy as np
import matplotlib.pyplot as plt
import math
import time
import copy
# parameters
gkbar = 2 * 10e-3 # S/cm2
gcabar = 1.1 * 10e-3 # S/cm2
gl = 0.5 * 10e-3 # S/cm2
el = -0.05 # V
v1 = -0.0012 # V
v2 = 0.018 # V
v3 = -0.03 # V
v4 = 0.01 # V
b  = 0.02 * 10e-3 # S*V/cm2 = A/cm2
phi = 0.01
eca = 0.1 # V
ek = -0.07 # V
tau = 0.8
C= 2 * 10e-6 # S/cm2 2 uA/Vcm2
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
t = [i/1600.0 for i in range(0,1600,1)]
ilist = np.zeros((1601))
current1 = [0.0001 for i in range(0,100)]
current2 = [0.001 for i in range(0,100)]
current3 = [0.002 for i in range(0,100)]
current4 = [-0.0001 for i in range(0,100)]
current5 = [-0.001 for i in range(0,100)]
current6 = [-0.002 for i in range(0,100)]

ilist[400:500] = copy.deepcopy(current1)
ilist[600:700] = copy.deepcopy(current2)
ilist[800:900] = copy.deepcopy(current3)
ilist[1000:1100] = copy.deepcopy(current4)
ilist[1200:1300] = copy.deepcopy(current5)
ilist[1400:1500] = copy.deepcopy(current6)

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
