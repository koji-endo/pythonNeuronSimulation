# stmfile generator
from PIL import Image, ImageDraw
import numpy as np
import cv2
from itertools import product
import json
# meta settings
NORUN = False
dirname = "ex2_1"
## settings
# array scale
basefilepath = "/home/tsunoda/pythonNeuronSimulation/testdata/ex2_1"
dynamics = "dyn.json"
connection_def =  "nwk6.json"
record_setting =  "rec.json"

nwk_list = [1,2,3,4,5,6]
direction_list = [0,180]
delays = [i for i in range(1,24)]
for nw, stim_direction, delay in product(nwk_list,direction_list,delays):
    # horizontal = X * 1.73/2, vertical = X * 1/2 + Y
    # timefrequency(hz/s), spatialfrequency (hz/ommatidium) = 1/wqavelength
    # stim
    # direction(degree from x axis), offset(ms), duration(ommatidium), power(uA)
    filename = "nwk" + str(nw)+"delay" + str(delay)+ "direct"+str(stim_direction)
    rundata = {}
    rundata["dynamics_def_path"] = basefilepath + "/" + "dyn.json"
    rundata["stim_setting_path"] = basefilepath + "/stmdata/" + "delay"+ str(delay) +"direct"+ str(stim_direction) + "_stm.json"
    rundata["connection_def_path"] = basefilepath + "/nwkdata/" + "nwk"+str(nw)+ ".json"
    rundata["record_setting_path"] = basefilepath + "/" + record_setting
    rundata["description"] = "ex2 " + filename + " rundata"
    rundata["v_init"] = -60
    rundata["tstop"] = 3100
    with open("./"+ dirname + '/rundata/' + filename +"_run.json","w") as f:
        json.dump(rundata,f)
