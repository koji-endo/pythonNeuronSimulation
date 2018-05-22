import os.path
import numpy as np
import pickle
from datetime import datetime


def pickleData(**dict):
    if os.path.isdir('./result/') is False:
        os.mkdir('./result/')
    filename = './result/' + datetime.now().isoformat() + '.pickle'
    with open(filename, 'wb') as f:
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
    connection_list = [map(int, str.split(',')) for str in str_list]
    print(connection_list)

    f = open(paths['stim_setting_path'], 'r')
    str_stim = f.read()
    f.close()
    str_list = str_stim.split('\n')
    str_list.pop()
    stim_settings_precast = [str.split(',') for str in str_list]
    stim_settings = [[int(str[0]), int(str[1]), int(str[2]), float(str[3])] for str in stim_settings_precast]

    f = open(paths['record_setting_path'], 'r')
    str_record = f.read()
    f.close()
    str_list = str_record.split('\n')
    str_list.pop()
    rec_index_list = map(int, str_list)

    return num, dynamics_list, connection_list, stim_settings, rec_index_list
