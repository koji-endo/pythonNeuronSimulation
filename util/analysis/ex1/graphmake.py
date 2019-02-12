import sys
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import argparse
import pickle
import json
from time import sleep
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
    plt.figure()
    plt.figure(figsize=(6,5), dpi=100)
    for f in files:
        with open(f, mode='rb') as F:
            data = pickle.load(F)
        r_v_list = data["results"]["r_v_list"]
        t = data['results']['t']
        vsum = np.zeros(len(t))
        counter = 0
        for r_v in r_v_list:
            v = r_v[1]
            if r_v[0]["target_cellname"].startswith("T4a,5,5"):
                plt.plot(t[500:],v[500:])
		plt.ylim(-70,-50)
		plt.xlabel("time (ms)")
		plt.ylabel("voltage (mV)")
                plt.title("T4a")
                #plt.title(json_run["description"])
    
    plt.savefig(root_dir + "result"+ str(i)+".png")
    sleep(1)
    plt.close()
