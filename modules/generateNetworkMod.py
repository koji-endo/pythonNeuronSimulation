import sys
import numpy as np
sys.path.append("/home/hayato/lib/python")
import neuron
from HHneuron import HHneuron
from Gradedneuron import Gradedneuron
from Rneuron import Rneuron
from Lneuron import Lneuron

class SimulationManager:
    def __init__(self, N=3, dynamics_list=["R","R","R"], neuron_connection=[[0,1],[1,2]], stim_settings=[[0,50,50,0.1]], rec_index_list=[0,2],condition="serial"):
        self.N = N
        self.dynamics_list = dynamics_list
        self.neuron_connection = neuron_conncection
        self.stim_settings = stim_settings
        self.rec_index_list = rec_index_list
        self.condition = condition
        self.gidlist = []
        self.cells = []
        self.nclist = []
        self.stimlist = []
        self.pc = neuron.h.ParallelContext()
        self.palcon = {}
        self.palcon["id"] = int(pc.id())
        self.palcon["nhost"] = int(pc.nhost())
        print("I am {} of {}".format(palcon["id"],palcon["nhost"]))

        self.set_numcells()

    def set_numcells(self):
        self.set_gids()
        self.generateNeuron()
        self.connect_cells()
        self.connect_stim()

    def set_gids(self):
        self.gidlist = []
        for i in range(int(self.pc.id()), self.N, int(self.pc.nhost())):
            self.gidlist.append(i)

    def generateNeuron(self):
        dynamics = []
        if len(self.dynamics_list) == 0:
            dynamics = ['HH' for i in range(self.N)]
        else:
            dynamics = self.dynamics_list
        self.cells = []
        for i in self.gidlist:
            if dynamics[i] == 'HH':
                nrn = HHneuron(i)
                self.cells.append(nrn)
            elif dynamics[i] == 'G':
                nrn = Gradedneuron(i)
                self.cells.append(nrn)
            elif dynamics[i] == 'R':
                nrn = Rneuron(i)
                self.cells.append(nrn)
            elif dynamics[i] == 'L':
                nrn = Lneuron(i)
                self.cells.append(nrn)
            self.pc.set_gid2node(i, int(self.pc.id()))
            self.pc.source_var(nrn.soma(0.5)._ref_v,i)
        self.pc.barrier()

    def connect_cells(self):
        for index,con in enumerate(self.neuron_connection):
            # only implemented for parallel transfer, not for spike based communication in parallel context
            if self.gid_exist(con[1]):
                self.cells[self.gid.index(con[1])].synapticConnection(source_gid=con[0],type=con[2],pc=self.pc)

    def connect_stim(self):
        self.stim_list = []
        for ele in stim_settings:
            if self.gid_exist(ele[0]):
                stim = neuron.h.IClamp(self.cells[self.gid.index(ele[0])].soma(0.5))
                stim.delay = ele[1]
                stim.dur = ele[2]
                stim.amp = ele[3]
                stim_list.append(stim)
