import sys
import numpy as np
sys.path.append("/home/hayato/lib/python")
import neuron
from HHneuron import HHneuron
from Gradedneuron import Gradedneuron
from Rneuron import Rneuron

def generateNeuron(num, dynamics_list=[]):
    dynamics = []
    if len(dynamics_list) == 0:
        dynamics = ['HHneuron' for i in range(num)]
    else:
        dynamics = dynamics_list
    neuronlist = []
    for i in range(num):
        if dynamics[i] == 'HH':
            nrn = HHneuron()
            neuronlist.append(nrn)
        elif dynamics[i] == 'G':
            nrn = Gradedneuron()
            neuronlist.append(nrn)
        elif dynamics[i] == 'R':
            nrn = Rneuron()
            neuronlist.append(nrn)            
    return neuronlist


def generateNetworks(neuronlist, connectivity):
    netcon_list = []
    for con in connectivity:
        netcon = neuronlist[con[0]].synapticConnection(neuronlist[con[1]])
        netcon_list.append(netcon)
    return netcon_list
