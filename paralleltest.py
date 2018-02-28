import sys
import numpy as np
import matplotlib.pyplot as plt
sys.path.append("/home/hayato/lib/python")
sys.path.append("./modules")
import neuron
import generateNetworkMod
import setStimulusMod
import ioMod

external = False
paths = {}
paths['dynamics_def_path'] = './testdata/graded_single/test1.dyn'
paths['connection_def_path'] = './testdata/graded_single/test1.nwk'
paths['stim_setting_path'] = './testdata/graded_single/test1.stm'
paths['record_setting_path'] = './testdata/graded_single/test1.rec'
## you must set these variable even though 'external' is True
v_init = -65
tstop = 300
## you must set these variable if 'external' is False
neuron_num = 3
dynamics_list = ['HH', 'HH', 'HH']
neuron_connection = [[0, 1], [1, 0], [1, 2]]
rec_index_list = [0, 1, 2]
stim_settings = [[1, 50, 50, 0.1], [0, 150, 50, 0.1]]


# read external file
if external is True:
    neuron_num, dynamics_list, neuron_connection, stim_settings, rec_index_list = ioMod.readExternalFiles(paths)


pc = neuron.h.ParallelContext()
print("number of hosts = ", pc.nhost())
print("this is #", pc.id())
pc.barrier()

# neuron definition
neuron_list = generateNetworkMod.generateNeuron(neuron_num, dynamics_list=dynamics_list, pc=pc)
pc.barrier()

print(neuron_list)

pc.runworker()
pc.done()
neuron.h.quit()
