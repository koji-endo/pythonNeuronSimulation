import sys
import numpy as np
import matplotlib.pyplot as plt
sys.path.append("/home/hayato/lib/python")
sys.path.append("./modules")
import argparse
import pickle

if not len(sys.argv) == 2:
    print("this program requires 1 argument (filepath)")
    exit()

with open(sys.argv[1], mode='rb') as f:
    data = pickle.load(f)
print(data)
r_v_list = data['results']['r_v_list']
t = data['results']['t']
for v in r_v_list:
    plt.plot(t, v)
plt.show()
