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
    print(json_dynamics)
    num = len(json_dynamics)

    f = open(paths['connection_def_path'], 'r')
    str_connection = f.read()
    f.close()
    str_list = comment_void_delete(str_connection.split('\n'))
    print(str_list)
    connection_list = []
    for str in str_list:
        if str == '':
            continue
        split_str = str.rstrip().split(',')
        connection_list.append(con_decorator(split_str))
    print(connection_list)

    with open(paths['stim_setting_path'], 'r') as f:
        stim_settings = json.load(f)

    f = open(paths['record_setting_path'], 'r')
    str_record = f.read()
    f.close()
    str_list = comment_void_delete(str_record.split('\n'))
    rec_index_list = []
    for str in str_list:
        if str == "":
            continue
        split_str = str.split(",")
        rec_index_list.append(rec_decorator(split_str))
    return num, json_dynamics, connection_list, stim_settings, rec_index_list

def con_decorator(split_str):
    if len(split_str) == 2:
        return [int(split_str[0]),int(split_str[1]),"soma",0.5,"soma",0.5,"E"]
    elif len(split_str) == 3:
        return [int(split_str[0]),int(split_str[1]),"soma",0.5,"soma",0.5,split_str[2]]
    elif len(split_str) == 7:
        return [int(split_str[0]),int(split_str[1]),split_str[2],float(split_str[3]),split_str[4],float(split_str[5]),split_str[6]]
    else:
        print("Error: " + "connection_def_path " + "contains invalid data. Each row must be INT INT STR or INT INT\n")
        exit()

def rec_decorator(split_str):
    if len(split_str) == 1:
        rec_target = {}
        rec_target["cell_id"] = int(split_str[0])
        rec_target["name"] = "soma"
        rec_target["place"] = 0.5
        return rec_target
    elif len(split_str) == 3:
        rec_target = {}
        rec_target["cell_id"] = int(split_str[0])
        rec_target["name"] = split_str[1]
        rec_target["place"] = float(split_str[2])
        return rec_target
    else:
        print("Error: " + "rec_def_path " + "contains invalid data. Each row must be INT or INT STR FLOAT\n")
        exit()

def comment_void_delete(str_list):
    # remove void
    s_list = [string for string in str_list if string != ""]
    # remove comment
    s_list = [string for string in s_list if string[0] != "#"]
    return s_list
def opt_separator(str_list):
    s_list = []
    splitstr_list = [str.split(";") for str in str_list]
    for str_list in splitstr_list:
        if len(str_list) == 1:
            s_list.append([str_list[0],[]])
        if len(str_list) == 2:
            s_list.append([str_list[0],str_list[1].split(",")])
    return s_list
