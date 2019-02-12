# stmfile generator
from PIL import Image, ImageDraw
import numpy as np
import cv2
from itertools import product
import json
# meta settings
NORUN = False
dirname = "ex3"
## settings
# array scale
basefilepath = "/home/tsunoda/pythonNeuronSimulation/testdata/ex3"
dynamics = "dyn.json"
connection_def =  "nwk6.json"
record_setting =  "rec.json"

direction_list = [0,30,60,90,120,150,180,210,240,270,300,330]
for stim_direction in direction_list:
    # horizontal = X * 1.73/2, vertical = X * 1/2 + Y
    # timefrequency(hz/s), spatialfrequency (hz/ommatidium) = 1/wqavelength
    # stim
    # direction(degree from x axis), offset(ms), duration(ommatidium), power(uA)
    filename = "direct"+str(stim_direction)
    rundata = {}
    rundata["dynamics_def_path"] = basefilepath + "/dyn.json"
    rundata["stim_setting_path"] = basefilepath + "/stmdata/direct"+ str(stim_direction) + "_stm.json"
    rundata["connection_def_path"] = basefilepath + "/nwk.json"
    rundata["record_setting_path"] = basefilepath + "/" + record_setting
    rundata["description"] = "ex3 " + filename + " rundata"
    rundata["v_init"] = -60
    rundata["tstop"] = 3100
    rundata["downsample"] = 20
    with open("./"+ dirname + '/rundata/' + filename +"_run.json","w") as f:
        json.dump(rundata,f)
