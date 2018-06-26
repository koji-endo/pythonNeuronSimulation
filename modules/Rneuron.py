import sys
import numpy as np
sys.path.append("/home/hayato/lib/python")
import neuron


class Rneuron:
    def __init__(self,index):
        self.index = index
        self.soma = neuron.h.Section(name="soma")
        self.soma.nseg = 1
        self.soma.diam = 5
        self.soma.cm =4
        self.soma.L = 10
        self.soma.insert("phcm")
        self.axon = neuron.h.Section(name="axon")
        self.axon.nseg = 1
        self.axon.diam = 5
        self.axon.cm = 4
        self.axon.L = 90
        self.axon.insert("phcm")
        self.soma.connect(self.axon, 1)
        neuron.h.psection()

    def synapticConnection(self, target, setting=[-10, 1, 10]):
        syn = target.generateSynapse()
        neuron.h.setpointer(self.soma(0.5)._ref_v,"vpre", syn)
        netcon = [self.index, target.index]
        return netcon
