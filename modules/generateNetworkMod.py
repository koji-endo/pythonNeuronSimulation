import sys
import numpy as np
sys.path.append("/home/hayato/lib/python")
import neuron
import json
from collections import OrderedDict
from importlib import import_module

class SimulationManager:
    def __init__(self, N=3, dynamics_list=[["R",[]],["R",[]],["R",[]]], neuron_connection=[[0,1],[1,2]], stim_settings={}, rec_index_list=[0,2],condition="serial"):
        self.N = N
        self.dynamics_list = dynamics_list
        self.nametoid = namealloc(dynamics_list)
        self.neuron_connection = neuron_connection
        self.stim_settings = stim_settings
        self.rec_index_list = rec_index_list
        self.condition = condition
        self.gidlist = []
        self.cells = []
        self.nclist = []
        self.stimlist = []
        self.pc = neuron.h.ParallelContext()
        self.palcon = {}
        self.palcon["id"] = int(self.pc.id())
        self.palcon["nhost"] = int(self.pc.nhost())
        print("I am {} of {}".format(self.palcon["id"], self.palcon["nhost"]))

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
        class_dict = loadModuleClass()
        dynamics = []
        if len(self.dynamics_list) == 0:
            dynamics = ['HH' for i in range(self.N)]
        else:
            dynamics = self.dynamics_list
        self.cells = []
        print(dynamics)
        for i in self.gidlist:
            #try:
            nrn = class_dict[dynamics[i]["celltype"]]["class_object"](i,opt=class_dict[dynamics[i]["celltype"]]["opt"],params=dynamics[i]["params"])
            print(nrn)
            self.cells.append(nrn)
            #except ImportError:
            #    print("module error")
            #except AttributeError:
            #    print("attribute error")
            self.pc.set_gid2node(i, int(self.pc.id()))
        self.pc.barrier()

    def connect_cells(self):
        for index,con in enumerate(self.neuron_connection):
            # only implemented for parallel transfer, not for spike based communication in parallel context
            if self.pc.gid_exists(con[0]):
                self.pc.source_var(self.cells[self.gidlist.index(con[0])].cell[con[2]](con[3])._ref_v,index,sec=self.cells[self.gidlist.index(con[0])].cell[con[2]])
        self.pc.barrier()
        for index,con in enumerate(self.neuron_connection):
            if self.pc.gid_exists(con[1]):
                self.cells[self.gidlist.index(con[1])].synapticConnection(connection_gid=index,type=con[6],position=[con[4],con[5]],pc=self.pc)
        self.pc.barrier()

    def connect_stim(self):
        self.stim_list = []
        for ele in self.stim_settings:
            if "target_cellname" in ele:
                id = self.name_to_id[ele["target_cellname"]]
            elif "target_cellid" in ele:
                id = ele["target_cellid"]
            else:
                print("each elements of stim file must contain key named target_cellname or target_cellid")
                exit()
            if self.pc.gid_exists(id):
                stim = getattr(neuron.h(),ele["suffix"])(self.cells[self.gidlist.index(id)].cell[ele["section"]["name"]](ele["section"]["point"]))
                for params in ele["opt"].items():
                    setattr(stim, params[0], ele[1])
                self.stim_list.append(stim)

def loadModuleClass():
    nametomodule = {}
    with open("cellname_module.json","r") as f:
        df = json.load(f)
        for member in df:
            print(member["path"])
            print(member["root"])
            mdl_obj = import_module(str(member["path"]),member["root"])
            cls_obj = getattr(mdl_obj, member["class"])
            nametomodule[member["name"]] = {"class_object": cls_obj,"opt": member["opt"]}
    return nametomodule

def namealloc(list):
    namelist = {}
    for i,ele in enumerate(list):
        if "cellname" in ele:
            namelist[ele["cellname"]] = i
    return namelist
