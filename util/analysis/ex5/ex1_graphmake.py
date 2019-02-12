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
    plt.figure(figsize=(8,6), dpi=100)
    for f in files:
        with open(f, mode='rb') as F:
            data = pickle.load(F)
        r_v_list = data["results"]["r_v_list"]
        t = data['results']['t']
        vsum = np.zeros(len(t))
        counter = 0
        for r_v in r_v_list:
            v = r_v[1]
            if r_v[0]["target_cellname"].startswith("R1-6,5,5"):
                plt.subplot(3, 4, 1)
                plt.plot(t[500:],v[500:])
		plt.title("R1-6")
            if r_v[0]["target_cellname"].startswith("Mi1,5,5"):
                plt.subplot(3, 4, 5)
                plt.plot(t[500:],v[500:])
		plt.title("Mi1")
            if r_v[0]["target_cellname"].startswith("C3,5,5"):
                plt.subplot(3, 4, 6)
                plt.plot(t[500:],v[500:])
		plt.ylim(-100,-85)
		plt.title("C3")
            if r_v[0]["target_cellname"].startswith("Mi9,5,5"):
                plt.subplot(3, 4, 7)
                plt.plot(t[500:],v[500:])
		plt.ylim(-55,-40)
		plt.title("Mi9")
            if r_v[0]["target_cellname"].startswith("T4a,5,5"):
                plt.subplot(3, 4, 9)
                plt.plot(t[500:],v[500:])
		plt.ylim(-70,-48)
                plt.title("T4a")
            if r_v[0]["target_cellname"].startswith("T4b,5,5"):
                plt.subplot(3, 4, 10)
                plt.plot(t[500:],v[500:])
		plt.ylim(-70,-48)
                plt.title("T4b")
            if r_v[0]["target_cellname"].startswith("T4c,5,5"):
                plt.subplot(3, 4, 11)
                plt.plot(t[500:],v[500:])
		plt.ylim(-70,-48)
                plt.title("T4c")
            if r_v[0]["target_cellname"].startswith("T4d,5,5"):
                plt.subplot(3, 4, 12)
                plt.plot(t[500:],v[500:])
		plt.ylim(-70,-48)
                plt.title("T4d")
                #plt.title(json_run["description"])
    plt.subplots_adjust(hspace=0.6,wspace=0.5)
    plt.savefig(root_dir + "result"+ str(i)+".png")
    sleep(1)
    plt.close()
