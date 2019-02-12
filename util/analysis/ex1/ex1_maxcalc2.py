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
        print(json_run["description"])
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
                print(max(v[500:]))
		print("R maxtime = {}".format(t[v[500:].argmax()+500]))
            if r_v[0]["target_cellname"].startswith("C3,5,5"):
                print(max(v[50000:]))
		print("C3 maxtime = {}".format(t[v[50000:].argmax()+50000]))
            if r_v[0]["target_cellname"].startswith("T4a,5,5"):
                print(max(v[50000:]))
		print("T4a max = {}".format(max(v[50000:])))
