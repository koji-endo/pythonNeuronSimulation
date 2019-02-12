# stmfile generator
from PIL import Image, ImageDraw
import numpy as np
import cv2
from itertools import product
import json
# meta settings
NORUN = False
dirname = "ex5"
## settings
# array scale
basefilepath = "/home/tsunoda/pythonNeuronSimulation/testdata/ex5"
dynamics = "dyn.json"
connection_def =  "nwk6.json"
record_setting =  "rec.json"

timefreqlist = [0.3,1.0,3.0]
spatialfreqlist = [0.1]
direction_list = [0,90,180,270]
for tf,sf,stim_direction in product(timefreqlist, spatialfreqlist, direction_list):
    # horizontal = X * 1.73/2, vertical = X * 1/2 + Y
    # timefrequency(hz/s), spatialfrequency (hz/ommatidium) = 1/wqavelength
    # stim
    # direction(degree from x axis), offset(ms), duration(ommatidium), power(uA)
    filename = "tf"+str(tf)+"sf"+str(sf)+"direct"+str(stim_direction)
    rundata = {}
    rundata["dynamics_def_path"] = basefilepath + "/dyn.json"
    rundata["stim_setting_path"] = basefilepath + "/stmdata/"+"tf"+str(tf)+"sf"+str(sf)+"direct"+ str(stim_direction) + "_stm.json"
    rundata["connection_def_path"] = basefilepath + "/nwk.json"
    rundata["record_setting_path"] = basefilepath + "/" + record_setting
    rundata["description"] = "ex5 " + filename + " rundata"
    rundata["v_init"] = -60
    rundata["tstop"] = 3100
    rundata["downsample"] = 20
    with open("./"+ dirname + '/rundata/' + filename +"_run.json","w") as f:
        json.dump(rundata,f)
