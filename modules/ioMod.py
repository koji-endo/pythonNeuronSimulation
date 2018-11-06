import os.path
import numpy as np
import pickle
from datetime import datetime
import shutil
import json
from collections import OrderedDict

def pickleData(**dict):
    if os.path.isdir('./result/') is False:
        os.mkdir('./result/')
    if int(dict["host_info"][1]) == 0:
        if os.path.isdir('./result/' + dict["datetime"]) is False:
            os.mkdir('./result/' + dict["datetime"])
            shutil.copy(dict['paths']['setting_file_path'],'./result/' + dict['datetime'] + '/')
    dict["pc"].barrier()
    filename = './result/' + dict["datetime"] + "/" + str(int(dict["host_info"][1])) + "_" + str(int(dict["host_info"][0])) +  '.pickle'
    with open(filename, 'wb') as f:
        dict.pop("pc")
        pickle.dump(dict, f, protocol=pickle.HIGHEST_PROTOCOL)

def readExternalFiles(paths):
    with open(paths['dynamics_def_path'], 'r') as f:
        json_dynamics = json.load(f)
    #print(json_dynamics)
    num = len(json_dynamics)

    with open(paths['connection_def_path'], 'r') as f:
        json_connection = json.load(f)
    #print(json_connection)
    with open(paths['stim_setting_path'], 'r') as f:
        stim_settings = json.load(f)
    #print(stim_settings)
    with open(paths['record_setting_path'], 'r') as f:
        rec_list = json.load(f)
    #print(rec_list)
    return num, json_dynamics, json_connection, stim_settings, rec_list
