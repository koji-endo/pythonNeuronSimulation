import sys
import numpy as np
#import matplotlib.pyplot as plt
from mpi4py import MPI
sys.path.append("/home/hayato/lib/python")
sys.path.append("./modules")
import neuron
import generateNetworkMod
import ioMod
import argparse
from glob import glob
import time
import datetime
neuron.h.load_file("nrngui.hoc")
p = argparse.ArgumentParser(description='Multineuron simulator for Neuron with python',
                            add_help=True)
p.add_argument("--nostore", action="store_true")
p.add_argument('-f', '--file', help="execute simulation with target directories parameter files.",
               default='')
p.add_argument('-s', '--setting', help="execute simulation with target setting files.", default='')
args = p.parse_args()

# variable
external = True
noDisplay = True #for remote
Setting = (args.setting != "")
File = (args.file != "")
paths = {}
# default v_init and tstop
sim_params = [-65,1000]

if Setting:
    with open(args.setting) as f:
        l = f.readlines()
        paths['dynamics_def_path'] = l[0].replace('\n','')
        paths['connection_def_path'] = l[1].replace('\n','')
        paths['stim_setting_path'] = l[2].replace('\n','')
        paths['record_setting_path'] = l[3].replace('\n','')
        sim_params[0] = float(l[4].replace('\n',''))
        sim_params[1] = float(l[5].replace('\n',''))
        paths['setting_file_path'] = args.setting
elif File:
    #paths['dynamics_def_path'] = './testdata/singleRtoL/test1.dyn'
    if args.file[-1] != '/':
        filename = args.file + "/"
    else:
        filename = args.file
    stm = glob(filename+"*.stm")
    nwk = glob(filename+"*.nwk")
    dyn = glob(filename+"*.dyn")
    rec = glob(filename+"*.rec")
    if len(stm) == 0 or len(nwk) == 0 or len(dyn) == 0 or len(rec) == 0:
        print("Error: lack at least one of required setting files in " + filename + ".")
        exit()
    else:
        paths['dynamics_def_path'] = dyn[0]
        paths['connection_def_path'] = nwk[0]
        paths['stim_setting_path'] = stm[0]
        paths['record_setting_path'] = rec[0]
else:
    #paths['connection_def_path'] = './testdata/singleRtoL/test1.nwk'
    #paths['stim_setting_path'] = './testdata/singleRtoL/test1.stm'
    #paths['record_setting_path'] = './testdata/singleRtoL/test1.rec'
    paths['dynamics_def_path'] = './testdata/lamina_single/lamina_single.dyn'
    paths['connection_def_path'] = './testdata/lamina_single/lamina_single.nwk'
    paths['stim_setting_path'] = './testdata/lamina_single/lamina_single.stm'
    paths['record_setting_path'] = './testdata/lamina_single/lamina_single.rec'

## you must set these variable if 'external' is False
neuron_num = 3
dynamics_list = ['HH', 'G', 'HH']
neuron_connection = [[0, 1], [1, 0], [1, 2]]
rec_index_list = [0, 1, 2]
stim_settings = [[1, 50, 50, 0.1], [0, 150, 50, 0.1]]
print("nostore = " + str(args.nostore) + " external = " + str(external) + "\n")

# read external file
if external is True:
    neuron_num, dynamics_list, neuron_connection, stim_settings, rec_index_list = ioMod.readExternalFiles(paths)

v_init = sim_params[0]
tstop = sim_params[1]

# parallel context
simManager = generateNetworkMod.SimulationManager(N=neuron_num, dynamics_list=dynamics_list, neuron_connection=neuron_connection, stim_settings=stim_settings, rec_index_list=rec_index_list,condition="parallel")
host_info = [simManager.pc.nhost(),simManager.pc.id()]


# recoding setting
print("set records")

# make unified time
strtime = ""
if host_info[1] == 0:
    strtime = datetime.datetime.now().isoformat().replace(":","_")
sref = neuron.h.ref(strtime)
simManager.pc.broadcast(sref, 0)
simManager.pc.barrier()
strtime = sref[0]

rec_v_list = []
rec_t = neuron.h.Vector()
rec_t.record(neuron.h._ref_t)
for rec in rec_index_list:
    if simManager.pc.gid_exists(rec[0]):
        rec_v = neuron.h.Vector()
        rec_v.record(simManager.cells[simManager.gidlist.index(rec[0])].cell[rec[1]](rec[2])._ref_v)
        rec_v_list.append([rec[0],rec_v])
print("setting finish")
simManager.pc.barrier()

# simulation
print("before setup")
simManager.pc.set_maxstep(10)
simManager.pc.setup_transfer()
print("before finitialize")
neuron.h.stdinit()
print("before RUN")
simManager.pc.barrier()
# gather the results
print("before psolve")
simManager.pc.psolve(tstop)
print("Finish psolve")

# gather the results
# https://www.neuron.yale.edu/neuron/static/py_doc/modelspec/programmatic/network/parcon.html
r_v_list = [[r_v[0],r_v[1].as_numpy()] for r_v in rec_v_list]
# convert results
t = rec_t.as_numpy()

#    if noDisplay is False:
#        # show graph
#        for v in final_r_v_list:
#            plt.plot(t, v)
#        plt.show()

# pickle all parameters, settings, and results
if args.nostore is False:
    if external is True:
        ioMod.pickleData(external=external, paths=paths, conditions=[v_init, tstop], results={'t': t, 'r_v_list': r_v_list}, host_info = host_info, datetime=strtime, pc= simManager.pc)
    if external is False:
        ioMod.pickleData(external=external, input=[neuron_num, dynamics_list, neuron_connection, stim_settings, rec_index_list], conditions=[v_init, tstop], results={'t': t, 'r_v_list': r_v_list}, host_info=host_info, datetime=strtime, pc= simManager.pc)


simManager.pc.barrier()
print("before runworker")
simManager.pc.runworker()
simManager.pc.done()
print("done")
