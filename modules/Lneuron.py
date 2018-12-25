import sys
import numpy as np
sys.path.append("/home/hayato/lib/python")
import neuron


class Lneuron:
    def __init__(self,index,opt={},params={}):
        self.index = index
        self.cell = {}
        #self.cell["soma"] = neuron.h.Section(name="soma")
        #self.cell["soma"].nseg = 1
        #self.cell["soma"].diam = 0.5
        #self.cell["soma"].L = 10
        #self.cell["soma"].insert("mole")
        #self.cell["soma"].ek = -70
        #self.cell["soma"].eca = 100
        #self.cell["soma"].cm = 10
        #self.cell["soma"].Ra = 100
        self.cell["axon"] = neuron.h.Section(name="axon")
        self.cell["axon"].nseg = 1
        self.cell["axon"].diam = 2
        self.cell["axon"].L = 10
        self.cell["axon"].cm = 1
        self.cell["axon"].insert("LMC")
        self.cell["axon"].gl_LMC = 97
        #self.cell["axon"].gcabar_mole = 2.0
        #self.cell["ap_dend"] = neuron.h.Section(name="ap_dend")
        #self.cell["ap_dend"].L = 45
        #self.cell["ap_dend"].diam = 0.1
        #self.cell["ap_dend"].nseg = 1
        #self.cell["ap_dend"].insert("mole")
        #self.cell["ap_dend"].Ra = 100
       # self.cell["soma"].connect(self.cell["axon"], 1)
        #self.cell["ap_dend"].connect(self.cell["soma"], 1)
        #neuron.h.psection()
        self.synlist = []
