import sys
import numpy as np
sys.path.append("/home/hayato/lib/python")
import neuron


class Lneuron:
    def __init__(self,index,opt={},params={}):
        self.index = index
        self.cell = {}
        self.cell["soma"] = neuron.h.Section(name="soma")
        self.cell["soma"].nseg = 1
        self.cell["soma"].diam = 0.5
        self.cell["soma"].L = 10
        self.cell["soma"].insert("mole")
        self.cell["soma"].ek = -70
        self.cell["soma"].eca = 100
        self.cell["soma"].cm = 10
        self.cell["soma"].Ra = 100
        self.cell["axon"] = neuron.h.Section(name="axon")
        self.cell["axon"].nseg = 1
        self.cell["axon"].diam = 0.1
        self.cell["axon"].L = 45
        self.cell["axon"].insert("mole")
        self.cell["axon"].Ra = 100
        self.cell["ap_dend"] = neuron.h.Section(name="ap_dend")
        self.cell["ap_dend"].L = 45
        self.cell["ap_dend"].diam = 0.1
        self.cell["ap_dend"].nseg = 1
        self.cell["ap_dend"].insert("mole")
        self.cell["ap_dend"].Ra = 100
        self.cell["soma"].connect(self.cell["axon"], 1)
        self.cell["ap_dend"].connect(self.cell["soma"], 1)
        neuron.h.psection()
        self.synlist = []

    def synapticConnection(self, connection_gid=0,type="E", position=["soma",0.5],pc=None):
        syn = self.generateSynapse(type=type,position=position)
        pc.target_var(syn,syn._ref_vpre, connection_gid)

    def generateSynapse(self,type="E",position=["soma",0.5]):
        syn = neuron.h.gsyn(self.cell[position[0]](position[1]))

        if type == "E":
            syn.vth = -80
            syn.gsat = 0.8
            syn.k = 0.02
            syn.n = 1
            syn.numsyn = 1
            syn.vre = -40
        elif type == "I":
            syn.vth = -50
            syn.gsat = 0.03
            syn.k = 2
            syn.n = 1
            syn.numsyn = 10
            syn.vre = 0

        self.synlist.append(syn)
        return syn
