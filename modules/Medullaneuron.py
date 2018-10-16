import sys
import numpy as np
sys.path.append("/home/hayato/lib/python")
import neuron


class Medullaneuron:
    def __init__(self, index, opt={"type":"Tm1"},params={}):
        self.index = index
        self.celltype = opt["type"]
        self.params = params
        self.cell={}
        self.generateCell(self.celltype,self.option)
        self.synlist = []

    def generateCell(self, celltype="Tm1", params={}):
        self.cell["soma"] = neuron.h.Section(name="soma")
        self.cell["soma"].nseg = 1
        self.cell["soma"].diam = 0.5
        self.cell["soma"].L = 10
        self.cell["soma"].insert("MIN")
        self.cell["soma"].ek = -70
        self.cell["soma"].cm = 10
        if self.celltype == "Tm1":
            self.cell["axon"] = neuron.h.Section(name="axon")
            self.cell["axon"].nseg = 100
            self.cell["axon"].diam = 0.1
            self.cell["axon"].L = 300
            self.cell["axon"].insert("MIN")
            self.cell["ap_dend"] = neuron.h.Section(name="ap_dend")
            self.cell["ap_dend"].L = 50
            self.cell["ap_dend"].diam = 0.1
            self.cell["ap_dend"].nseg = 5
            self.cell["ap_dend"].insert("MIN")
        if self.celltype == "Tm2":
            self.cell["axon"] = neuron.h.Section(name="axon")
            self.cell["axon"].nseg = 30
            self.cell["axon"].diam = 0.1
            self.cell["axon"].L = 300
            self.cell["axon"].insert("mole")
            self.cell["ap_dend"] = neuron.h.Section(name="ap_dend")
            self.cell["ap_dend"].L = 50
            self.cell["ap_dend"].diam = 0.1
            self.cell["ap_dend"].nseg = 5
            self.cell["ap_dend"].insert("mole")
        if self.celltype == "Tm3":
            self.cell["axon"] = neuron.h.Section(name="axon")
            self.cell["axon"].nseg = 15
            self.cell["axon"].diam = 0.1
            self.cell["axon"].L = 300
            self.cell["axon"].insert("mole")
            self.cell["ap_dend"] = neuron.h.Section(name="ap_dend")
            self.cell["ap_dend"].L = 15
            self.cell["ap_dend"].diam = 0.1
            self.cell["ap_dend"].nseg = 5
            self.cell["ap_dend"].insert("mole")
        if self.celltype == "Mi1":
            self.cell["axon"] = neuron.h.Section(name="axon")
            self.cell["axon"].nseg = 30
            self.cell["axon"].diam = 0.1
            self.cell["axon"].L = 300
            self.cell["axon"].insert("mole")
            self.cell["ap_dend"] = neuron.h.Section(name="ap_dend")
            self.cell["ap_dend"].L = 50
            self.cell["ap_dend"].diam = 0.1
            self.cell["ap_dend"].nseg = 5
            self.cell["ap_dend"].insert("mole")
        self.cell["soma"].Ra = 100
        self.cell["ap_dend"].Ra = 100
        self.cell["axon"].Ra = 0.01
        self.cell["axon"].connect(self.cell["soma"], 1)
        self.cell["ap_dend"].connect(self.cell["axon"], 1)
        if len(option) != 0:
            self.cell["soma"].gnabar_MIN = float(params["gnabar_MIN"])

    def synapticConnection(self, connection_gid=0,type="E",pc=None,position=["soma",0.5]):
        syn = self.generateSynapse(type=type,position=position)
        pc.target_var(syn,syn._ref_vpre, connection_gid)

    def generateSynapse(self,type="E",position=["soma",0.5]):
        if position[1] > 1 or position[1] < 0:
            print("Synaptic position out of range." + str(position[1]))
            exit()
        syn = neuron.h.gsyn(self.cell[position[0]](position[1]))
        if type == "E":
            # gsat/k equals dynamic range
            syn.vth = -58
            syn.gsat = 0.08
            syn.k = 0.02
            syn.n = 1
            syn.numsyn = 10
            syn.vre = -40
        elif type == "I":
            syn.vth = -58
            syn.gsat = 0.08
            syn.k = 0.02
            syn.n = 1
            syn.numsyn = 10
            syn.vre = -70

        self.synlist.append(syn)
        return syn
