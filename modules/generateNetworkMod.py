import sys
import numpy as np
sys.path.append("/home/hayato/lib/python")
import neuron
from HHneuron import HHneuron
from Gradedneuron import Gradedneuron
from Rneuron import Rneuron
from Lneuron import Lneuron
def generateNeuron(num, dynamics_list=[]):
    dynamics = []
    if len(dynamics_list) == 0:
        dynamics = ['HHneuron' for i in range(num)]
    else:
        dynamics = dynamics_list
    neuronlist = []
    for i in range(num):
        if dynamics[i] == 'HH':
            nrn = HHneuron(i)
            neuronlist.append(nrn)
        elif dynamics[i] == 'G':
            nrn = Gradedneuron(i)
            neuronlist.append(nrn)
        elif dynamics[i] == 'R':
            nrn = Rneuron(i)
            neuronlist.append(nrn)
        elif dynamics[i] == 'L':
            nrn = Lneuron(i)
            neuronlist.append(nrn)
    return neuronlist


def generateNetworks(neuronlist, connectivity):
    netcon_list = []
    for con in connectivity:
        if len(con) == 3:
            netcon = neuronlist[con[0]].synapticConnection(neuronlist[con[1]],type=con[2])
        elif len(con) == 2:
            netcon = neuronlist[con[0]].synapticConnection(neuronlist[con[1]])
        netcon_list.append(netcon)
    return netcon_list
