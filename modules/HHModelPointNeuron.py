import sys
import numpy as np
import json
with open("meta.json","r") as f:
    meta = json.load(f)
    sys.path.append(meta["nrnpy-path"])
import neuron

class HHmodel:
    def __init__(self, index, opt={}, params={}):
        self.index = index
        self.cell={}
        self.cell["soma"] = neuron.h.Section(name="soma")
        self.cell["soma"].nseg = 1
        self.cell["soma"].diam = 10
        self.cell["soma"].L = 10
        self.cell["soma"].insert("hh")
        if "gnabar_hh" in opt:
            self.cell["soma"].gnabar_hh = opt["gnabar_hh"]
        else:
            self.cell["soma"].gnabar_hh = 0.012
        self.cell["soma"].gkbar_hh = 0.0036
        self.cell["soma"].gl_hh = 0.00003

    def synapticConnection(self, target, setting=[-10, 1, 10]):
        netcon = neuron.h.NetCon(self.axon(0.5)._ref_v, target.esyn, sec=self.axon)
        netcon.threshold = setting[0]
        netcon.weight[0] = setting[1]
        netcon.delay = setting[2]
        return netcon
