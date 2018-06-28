import sys
import numpy as np
sys.path.append("/home/hayato/lib/python")
import neuron


class Lneuron:
    def __init__(self,index):
        self.index = index
        self.soma = neuron.h.Section(name="soma")
        self.soma.nseg = 1
        self.soma.diam = 5
        self.soma.L = 10
        self.soma.insert("mole")
	self.soma.ek = -70
	self.soma.eca = 100
        self.axon = neuron.h.Section(name="axon")
        self.axon.nseg = 1
        self.axon.diam = 0.1
        self.axon.L = 45
        self.axon.insert("mole")
        self.ap_dend = neuron.h.Section(name="ap_dend")
        self.ap_dend.L = 45
        self.ap_dend.diam = 0.1
        self.ap_dend.nseg = 1
        self.ap_dend.insert("mole")
        self.soma.connect(self.axon, 1)
        self.ap_dend.connect(self.soma, 1)
        neuron.h.psection()
        self.synlist = []

    def synapticConnection(self, target, setting=[-10, 1, 10]):
        netcon = neuron.h.NetCon(self.axon(0.5)._ref_v, target.esyn, sec=self.axon)
        netcon.threshold = setting[0]
        netcon.weight[0] = setting[1]
        netcon.delay = setting[2]
        return netcon

    def generateSynapse(self):
        syn = neuron.h.gsyn(self.soma(0.5))
        self.synlist.append(syn)
        return syn
