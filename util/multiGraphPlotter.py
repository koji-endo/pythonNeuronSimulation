import sys
import os
import numpy as np
import matplotlib.pyplot as plt
sys.path.append("./modules")
import argparse
import pickle

def walk_files_with(extension, directory='.'):
    """Generate paths of all files that has specific extension in a directory.

    Arguments:
    extension -- [str] File extension without dot to find out
    directory -- [str] Path to target directory

    Return:
    filepath -- [str] Path to file found
    """
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
files = []
files = walk_files_with('pickle',root_dir)
print(files)
for f in files:
    with open(f, mode='rb') as F:
        data = pickle.load(F)
        r_v_list = data["results"]["r_v_list"]
        t = data['results']['t']
        for r_v in r_v_list:
                v = r_v[1]
                plt.plot(t, v)
plt.show()
