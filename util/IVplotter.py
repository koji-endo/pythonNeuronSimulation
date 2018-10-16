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
#mean_rv = np.zeros((11))
#ilist = [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
for i,f in enumerate(files):
    with open(f, mode='rb') as F:
        data = pickle.load(F)
        r_v_list = data["results"]["r_v_list"]
        t = data['results']['t']
        dt = t[1]-t[0]
        time_start = int(55/dt)
        time_end = int(100/dt)
        for r_v in r_v_list:
            print(r_v[0])
            if r_v[0]["cell_id"] >= 0 and r_v[0]["cell_id"] < 6:
                if r_v[0]["name"] == "soma":
                    if r_v[0]["place"] > 0.2 and r_v[0]["place"] < 11:
                        print(r_v[0])
                        v = r_v[1]
                        print(v)
                        plt.subplot(len(r_v_list), len(files), r_v[0]["cell_id"]+1)
                        plt.plot(t,v)
#            if r_v[0]["cell_id"] >= 18 and r_v[0]["cell_id"] < 20:
#                print(r_v[0])
#                v = r_v[1]
#                plt.subplot(2, 1, 2)
#                plt.plot(t,v)
            #slice_v = [v[i] for i in range(time_start,time_end)]
            #mean_rv[r_v[0]+1] = sum(slice_v)/ len(slice_v)
        #mean_rv[0] = v[time_end + 1000]
#plt.plot(ilist,mean_rv)
plt.xlabel("Time (ms)")
plt.ylabel("membrane Voltage (mV)")
plt.title("EMD circuit Result")
plt.show()
