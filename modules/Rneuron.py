import sys
import numpy as np
sys.path.append("/home/hayato/lib/python")
import neuron


class Rneuron:
    def __init__(self):
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
        self.esyn = neuron.h.Exp2Syn(self.axon(0.5))
        self.esyn.tau1 = 0.5
        self.esyn.tau2 = 1.0
        self.esyn.e = 0

    def synapticConnection(self, target, setting=[-10, 1, 10]):
        netcon = neuron.h.NetCon(self.soma(0.5)._ref_v, target.esyn, sec=self.axon)
        netcon.threshold = setting[0]
        netcon.weight[0] = setting[1]
        netcon.delay = setting[2]
        return netcon
