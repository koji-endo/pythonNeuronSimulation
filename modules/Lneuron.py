import sys
import numpy as np
sys.path.append("/home/hayato/lib/python")
import neuron


class Lneuron:
    def __init__(self,index):
        self.index = index
        self.soma = neuron.h.Section(name="soma")
        self.soma.nseg = 1
        self.soma.diam = 0.5
        self.soma.L = 10
        self.soma.insert("mole")
        self.soma.ek = -70
        self.soma.eca = 100
        self.soma.cm = 10
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

    def synapticConnection(self, source_gid=0,type="E",pc=None):
        syn = self.generateSynapse(type=type)
        pc.target_var(syn,syn._ref_vpre, source_gid)

    def generateSynapse(self,type="E"):
        syn = neuron.h.gsyn(self.soma(0.5))

        if type == "E":
            syn.vth = -70
            syn.gsat = 0.08
            syn.k = 0.02
            syn.n = 1
            syn.numsyn = 10
            syn.vre = -80
        elif type == "I":
            syn.vth = -50
            syn.gsat = 0.03
            syn.k = 2
            syn.n = 1
            syn.numsyn = 10
            syn.vre = 0

        self.synlist.append(syn)
        return syn
