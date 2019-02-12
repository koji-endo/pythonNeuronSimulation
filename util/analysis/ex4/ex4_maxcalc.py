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
import csv
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
savelist= []
savelist.append(["","a"])

for i,dir in enumerate(directories):
    savedat = ["",0]
    files = []
    files = walk_files_with('pickle',root_dir + dir)
    runsrc = walk_files_with('json',root_dir + dir)
    with open(runsrc[0],"r") as F:
        json_run = json.load(F)
        savedat[0]=json_run["description"]
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
		savedat[1]=max(v[5000:])
    savelist.append(savedat)
with open("ch2data2.csv","w") as file:
    writer = csv.writer(file,lineterminator = '\n')
    writer.writerows(savelist)
