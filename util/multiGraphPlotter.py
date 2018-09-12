import sys
import os
import numpy as np
import matplotlib.pyplot as plt
sys.path.append("./modules")
import argparse
import pickle

if not len(sys.argv) == 2:
    print("this program requires 1 argument (filepath)")
    exit()

root_dir = sys.argv[1]
files = []
for root_dir, dirs, files in os.walk(root_dir):
    continue
 
for f in files:
    with open(root_dir + f, mode='rb') as F:
        data = pickle.load(F)
        r_v_list = data["results"]["r_v_list"]
        t = data['results']['t']
        for r_v in r_v_list:
            v = r_v[1]
            plt.plot(t, v)
            plt.show()

