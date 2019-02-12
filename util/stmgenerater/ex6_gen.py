# stmfile generator
from PIL import Image, ImageDraw
import numpy as np
import cv2
from itertools import product
import json
# meta settings
NORUN = False
dirname = "ex6"
## settings
# array scale
basefilepath = "/home/tsunoda/pythonNeuronSimulation/testdata/ex6"
dynamics = "dyn.json"
connection_def =  "nwk.json"
record_setting =  "rec.json"

    # horizontal = X * 1.73/2, vertical = X * 1/2 + Y
    # timefrequency(hz/s), spatialfrequency (hz/ommatidium) = 1/wqavelength
    # stim
    # direction(degree from x axis), offset(ms), duration(ommatidium), power(uA)
for i in range(1,4):
    filename = "gausian moving object test"+ str(i)
    rundata = {}
    rundata["dynamics_def_path"] = basefilepath + "/dyn.json"
    rundata["stim_setting_path"] = basefilepath + "/stm_"+ str(i)+".json"
    rundata["connection_def_path"] = basefilepath + "/nwk.json"
    rundata["record_setting_path"] = basefilepath + "/" + record_setting
    rundata["description"] = "ex6 " + filename + " rundata"
    rundata["v_init"] = -60
    rundata["tstop"] = 5100
    rundata["downsample"] = 20
    with open("./"+ dirname + '/run_'+ str(i)+'.json',"w") as f:
        json.dump(rundata,f)
