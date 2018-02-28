import sys
import numpy as np
sys.path.append("/home/hayato/lib/python")
import neuron
from HHneuron import HHneuron
from Gradedneuron import Gradedneuron


def generateNeuron(num, dynamics_list=[], pc=None):
    dynamics = []
    if len(dynamics_list) == 0:
        dynamics = ['HH' for i in range(num)]
    else:
        dynamics = dynamics_list
    neuronlist = []
    idlist = []
    print(pc)
    if pc is None:
        idlist = range(num)
    else:
        idlist = range(int(pc.id()), num, int(pc.nhost()))

    for i in idlist:
        if dynamics[i] == 'HH':
            nrn = HHneuron()
            nrn.host = int(pc.id())
            nrn.gid = i
            neuronlist.append(nrn)
        elif dynamics[i] == 'G':
            nrn = Gradedneuron()
            neuronlist.append(nrn)
    return neuronlist



def generateNetworks(neuronlist, connectivity):
    netcon_list = []
    for con in connectivity:
        netcon = neuronlist[con[0]].synapticConnection(neuronlist[con[1]])
        netcon_list.append(netcon)
    return netcon_list
