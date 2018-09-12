import os.path
import numpy as np
import pickle
from datetime import datetime
import shutil

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
        pickle.dump(dict, f)

def validator():
    return 0

def readExternalFiles(paths):
    f = open(paths['dynamics_def_path'], 'r')
    str_dynamics = f.read()
    f.close()
    dynamics_list = str_dynamics.split('\n')
    dynamics_list.pop()
    print(dynamics_list)
    num = len(dynamics_list)

    f = open(paths['connection_def_path'], 'r')
    str_connection = f.read()
    f.close()
    str_list = str_connection.split('\n')
    str_list.pop()
    print(str_list)
    connection_list = []
    for str in str_list:
        split_str = str.split(',')
        if len(split_str) == 2:
            connection_list.append([int(split_str[0]),int(split_str[1])])
        elif len(split_str) == 3:
            connection_list.append([int(split_str[0]),int(split_str[1]),split_str[2]])
        else:
            printf("Error: " + paths["connection_def_path"] + "contains invalid data. Each row must be INT INT STR or INT INT\n")
            exit()
    print(connection_list)

    f = open(paths['stim_setting_path'], 'r')
    str_stim = f.read()
    f.close()
    str_list = str_stim.split('\n')
    str_list.pop()
    stim_settings_precast = [str.split(',') for str in str_list]
    stim_settings = [[int(str[0]), float(str[1]), float(str[2]), float(str[3])] for str in stim_settings_precast]

    f = open(paths['record_setting_path'], 'r')
    str_record = f.read()
    f.close()
    str_list = str_record.split('\n')
    str_list.pop()
    rec_index_list = map(int, str_list)
    rec_index_list.sort()
    return num, dynamics_list, connection_list, stim_settings, rec_index_list
