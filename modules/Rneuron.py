import sys
import numpy as np
import json
with open("meta.json","r") as f:
    meta = json.load(f)
    sys.path.append(meta["nrnpy-path"])
import neuron


class Rneuron:
    def __init__(self,index,opt={},params={}):
        self.index = index
        self.cell = {}
        #self.cell["soma"] = neuron.h.Section(name="soma")
        #self.cell["soma"].nseg = 1
        #self.cell["soma"].diam = 0.1
        #self.cell["soma"].cm =4
        #self.cell["soma"].L = 10
        #self.soma.insert("hh")
        #self.cell["soma"].insert("phcm")
        #self.cell["soma"].ek = -85
        self.cell["axon"] = neuron.h.Section(name="axon")
        self.cell["axon"].nseg = 5
        self.cell["axon"].diam = 3
        self.cell["axon"].cm = 1
        self.cell["axon"].L = 100
        self.cell["axon"].insert("receptor2")
#        self.cell["axon"].ek = -85
        #self.cell["axon"].Ra = 0.001
       # self.cell["axon"].connect(self.cell["soma"], 1)
       # neuron.h.psection()

    def synapticConnection(self,connection_gid=0,type="E",pc=None):
        syn = self.generateSynapse(type=type)
        pc.target_var(syn,syn._ref_vpre, connection_gid)
