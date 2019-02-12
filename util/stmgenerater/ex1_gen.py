# stmfile generator
from PIL import Image, ImageDraw
import numpy as np
import cv2
from itertools import product
import json
# meta settings
NORUN = False
dirname = "ex1"
## settings
# array scale
basefilepath = "/home/tsunoda/pythonNeuronSimulation/testdata/ex1"
dynamics = "dyn.json"
connection_def =  "nwk6.json"
record_setting =  "rec.json"


timefreqlist = [1.0]
spatialfreqlist = [1/6.0]
boldness_list = [3.0]
direction_list = [0,180]
dyns = [1,2,3,4,5,6,7,8,9,10,11,12]
for tfreq,sfreq,bness,dtion,dyn in product(timefreqlist,spatialfreqlist,boldness_list,direction_list,dyns):
    # horizontal = X * 1.73/2, vertical = X * 1/2 + Y
    # timefrequency(hz/s), spatialfrequency (hz/ommatidium) = 1/wqavelength
    # stim
    # direction(degree from x axis), offset(ms), duration(ommatidium), power(uA)
    timefreq = tfreq
    spatialfreq = sfreq
    stim_bold = bness
    stim_direction = dtion
    stim_offset = 100
    stim_duration = 5000
    stim_power = 1.0
    filename = "tf" + str(timefreq)+ "sf"+ str(spatialfreq)+"bold"+str(stim_bold)+ "direct"+str(stim_direction)
    rundata = {}
    rundata["dynamics_def_path"] = basefilepath + "/" + "dyn" + str(dyn) + ".json"
    rundata["stim_setting_path"] = basefilepath + "/" + filename + "_stm.json"
    rundata["connection_def_path"] = basefilepath + "/" + connection_def
    rundata["record_setting_path"] = basefilepath + "/" + record_setting
    rundata["description"] = "ex1 " + filename + " rundata" + str(dyn)
    rundata["v_init"] = -60
    rundata["tstop"] = 3100
    with open("./"+ dirname + '/' + filename +"_run" + str(dyn) +".json","w") as f:
        json.dump(rundata,f)
