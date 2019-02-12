import sys
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import argparse
import pickle
import json
from itertools import product
from time import sleep
def threshing(li,var):
    purelist = []
    for ele in li:
	if ele > var:
	    purelist.append(ele-var)
	else:
	    purelist.append(0)
    return purelist
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

Networklist = [["T4a",-55,10.0],["T4b",-59,7.0],["T4c",-55,5],["T4d",-60,5.0]]
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
    for j,f in enumerate(files):
        with open(f, mode='rb') as F:
            data = pickle.load(F)
        r_v_list = data["results"]["r_v_list"]
        t = data['results']['t']
	if j == 0:
            T4asum = np.zeros(len(t))
	    T4bsum = np.zeros(len(t))
            T4csum = np.zeros(len(t))
	    T4dsum = np.zeros(len(t))
        for r_v in r_v_list:
            v = r_v[1]
            if r_v[0]["target_cellname"].startswith("T4a"):
                T4asum = T4asum + threshing(v,Networklist[0][1])
            if r_v[0]["target_cellname"].startswith("T4b"):
                T4bsum = T4bsum + threshing(v,Networklist[1][1])
            if r_v[0]["target_cellname"].startswith("T4c"):
                T4csum = T4csum + threshing(v,Networklist[2][1])
            if r_v[0]["target_cellname"].startswith("T4d"):
                T4dsum = T4dsum + threshing(v,Networklist[3][1])
    ts = range(0,5100)
    stm=[]
    stm.extend([1 for itr in range(0,1000)])
    stm.extend([0 for itr in range(1000,1200)])
    stm.extend([1 for itr in range(1200,2200)])
    stm.extend([0 for itr in range(2200,2400)])
    stm.extend([1 for itr in range(2400,3400)])
    stm.extend([0 for itr in range(3400,3600)])
    stm.extend([1 for itr in range(3600,4600)])
    stm.extend([0 for itr in range(4600,5100)])
    plt.figure()
    plt.figure(figsize=(8,6), dpi=100)
    plt.subplots_adjust(hspace=0.6,wspace=0.5)
    plt.subplot(5,1,1)
    plt.plot(ts,stm)
    plt.title("Stimulation")
    plt.subplot(5,1,2)
    plt.plot(t[500:],T4asum[500:])
    plt.title("T4a")
    plt.subplot(5,1,3)
    plt.plot(t[500:],T4bsum[500:])
    plt.title("T4b")
    plt.subplot(5,1,4)
    plt.plot(t[500:],T4csum[500:])
    plt.title("T4c")
    plt.subplot(5,1,5)
    plt.plot(t[500:],T4dsum[500:])
    plt.title("T4d")
    plt.savefig(root_dir + "result"+ str(i)+".png")
    sleep(1)
    plt.close()
