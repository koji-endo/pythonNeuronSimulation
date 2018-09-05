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
neuron.h.load_file("nrngui.hoc")
p = argparse.ArgumentParser(description='Multineuron simulator for Neuron with python',
                            add_help=True)
p.add_argument("--nostore", action="store_true")
p.add_argument('-f', '--file', help="execute simulation with target directorys parameter files.",
               default='')
args = p.parse_args()

# variable
external = True
noDisplay = True #for remote
paths = {}

if args.file == '':
    #paths['dynamics_def_path'] = './testdata/singleRtoL/test1.dyn'
    #paths['connection_def_path'] = './testdata/singleRtoL/test1.nwk'
    #paths['stim_setting_path'] = './testdata/singleRtoL/test1.stm'
    #paths['record_setting_path'] = './testdata/singleRtoL/test1.rec'
    paths['dynamics_def_path'] = './testdata/lamina_single/lamina_single.dyn'
    paths['connection_def_path'] = './testdata/lamina_single/lamina_single.nwk'
    paths['stim_setting_path'] = './testdata/lamina_single/lamina_single.stm'
    paths['record_setting_path'] = './testdata/lamina_single/lamina_single.rec'
else:
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

## you must set these variable even though 'external' is True
v_init = -65
tstop = 300
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

# parallel context
simManager = generateNetworkMod.SimulationManager(N=neuron_num, dynamics_list=dynamics_list, neuron_connection=neuron_connection, stim_settings=stim_settings, rec_index_list=rec_index_list,condition="parallel")

# recoding setting

rec_v_list = []
rec_t = neuron.h.Vector()
rec_t.record(neuron.h._ref_t)
for i in rec_index_list:
    if simManager.pc.gid_exists(i):
        rec_v = neuron.h.Vector()
        rec_v.record(simManager.cells[simManager.gidlist.index(i)].soma(0.5)._ref_v)
    rec_v_list.append([i,rec_v])
simManager.pc.barrier()

# simulation
print("before setup")
simManager.pc.set_maxstep(10)
simManager.pc.setup_transfer()
print("before finitialize")
neuron.h.stdinit()
print("before psolve")
simManager.pc.psolve(tstop)
print("Finish psolve")

# gather the results
# https://www.neuron.yale.edu/neuron/static/py_doc/modelspec/programmatic/network/parcon.html
r_v_list = [[r_v[0],r_v[1].as_numpy()] for r_v in rec_v_list]
all_r_v_list = []
if int(simManager.pc.id()) == 0:
    all_r_v_list = simManager.pc.py_alltoall(r_v_list)
    # convert results
    t = rec_t.as_numpy()
    r_v_list = all_r_v_list[:,1]
    final_r_v_list = r_v_list[np.argsort(all_r_v_list[:,1])]

print("Finished and Run Worker")
simManager.pc.runworker()
simManager.pc.done()
h.quit()
#    if noDisplay is False:
#        # show graph
#        for v in final_r_v_list:
#            plt.plot(t, v)
#        plt.show()

    # pickle all parameters, settings, and results
if args.nostore is False:
    if external is True:
        ioMod.pickleData(external=external, paths=paths, conditions=[v_init, tstop], results={'t': t, 'r_v_list': final_r_v_list})
    if external is False:
        ioMod.pickleData(external=external, input=[neuron_num, dynamics_list, neuron_connection, stim_settings, rec_index_list], conditions=[v_init, tstop], results={'t': t, 'final_r_v_list': final_r_v_list})
