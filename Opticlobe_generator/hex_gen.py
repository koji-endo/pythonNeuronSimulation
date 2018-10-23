import json
import numpy as np
from itertools import product
neighbors = [[0,1],[0,-1],[1,0],[-1,0],[1,-1],[-1,1]]

layer_name = ["R1-6","L1","L3","L5","Mi1","Tm3","Mi4","Mi9","TmY15","CT1","C1"]
dynamics = ["R","L","L","L","Mi1","Mi1","Mi1","Mi1","Mi1","Mi1","Mi1"]
# layer size
w = 35
h = 20
cells = []
for i,name in enumerate(layer_name):
    for x,y in product(range(w),range(h)):
        cell = {}
        cell["cellname"] = name + "," + str(x) + "," + str(y)
        cell["celltype"] = dynamics[i]
        cell["params"] = {}
        cells.append(cell)

with open("./dyn.json","w") as f:
    json.dump(cells,f)
