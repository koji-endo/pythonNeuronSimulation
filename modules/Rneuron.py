import sys
import numpy as np
sys.path.append("/home/hayato/lib/python")
import neuron


class Rneuron:
    def __init__(self,index):
        self.index = index
        self.soma = neuron.h.Section(name="soma")
        self.soma.nseg = 1
        self.soma.diam = 0.1
        self.soma.cm =4
        self.soma.L = 10
        #self.soma.insert("hh")
        self.soma.insert("phcm")
        self.soma.ek = -85
        self.axon = neuron.h.Section(name="axon")
        self.axon.nseg = 1
        self.axon.diam = 5
        self.axon.cm = 4 * 10e-6
        self.axon.L = 90
        self.axon.insert("phcm")
        self.axon.ek = -85
        self.soma.connect(self.axon, 1)
        neuron.h.psection()

    def synapticConnection(self,source_gid=0,type="E",pc=None):
        syn = self.generateSynapse(type=type)
        pc.target_var(syn,syn._ref_vpre, source_gid)
