import sys
import numpy as np
import json
with open("../meta.json","r") as f:
    meta = json.load(f)
    sys.path.append(meta["nrnpy-path"])
import neuron
from collections import OrderedDict
from importlib import import_module

class SimulationManager:
    def __init__(self, N=3, dynamics_list=[], neuron_connection=[], stim_settings=[], rec_list=[],condition="serial"):
        self.N = N
        self.dynamics_list = dynamics_list
        self.nametoid = namealloc(dynamics_list)
        self.neuron_connection = neuron_connection
        self.stim_settings = stim_settings
        self.rec_list = rec_list
        self.condition = condition
        self.generated_cellid_list = []
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
        self.generated_cellid_list = []
        for i in range(int(self.pc.id()), self.N, int(self.pc.nhost())):
            self.generated_cellid_list.append(i)

    def generateNeuron(self):
        class_dict = loadModuleClass()
        dynamics = []
        if len(self.dynamics_list) == 0:
            dynamics = ['HH' for i in range(self.N)]
        else:
            dynamics = self.dynamics_list
        self.cells = []
        print(dynamics)
        for i in self.generated_cellid_list:
            nrn = class_dict[dynamics[i]["celltype"]]["class_object"](i,opt=class_dict[dynamics[i]["celltype"]]["opt"],params=dynamics[i]["params"])
            print(nrn)
            self.cells.append(nrn)
        self.pc.barrier()

    def connect_cells(self):
        for index,con in enumerate(self.neuron_connection):
            if "source_cellname" in con:
                source_id = self.name_to_id[con["source_cellname"]]
            elif "source_cellid" in con:
                source_id = con["source_cellid"]
            else:
                print("each elements of nwk file must contain key named source_cellname or source_cellid")
                exit()
            if "spike_depend" not in con or con["spike_depend"] is False:
                if source_id in self.generated_cellid_list:
                    source_obj = self.cells[self.generated_cellid_list.index(source_id)].cell[con["source_section"]["name"]]
                    self.pc.source_var(source_obj(con["source_section"]["point"])._ref_v,index,sec=source_obj)
            else:
                if source_id in self.generated_cellid_list:
                    gid = index*2
                    self.pc.set_gid2node(gid,self.palcon["id"])
                    source_obj = self.cells[self.generated_cellid_list.index(source_id)].cell[con["source_section"]["name"]]
                    nc = neuron.h.NetCon(source_obj(con["source_section"]["point"])._ref_v, None, sec=source_obj)
                    if "source_opt" in con:
                        for opt in con["source_opt"]:
                            setattr(nc,opt[0],opt[1])
                    self.pc.cell(gid, nc)
        self.pc.barrier()
        for index,con in enumerate(self.neuron_connection):
            if "target_cellname" in con:
                target_id = self.name_to_id[con["target_cellname"]]
            elif "target_cellid" in con:
                target_id = con["target_cellid"]
            else:
                print("each elements of nwk file must contain key named target_cellname or target_cellid")
                exit()
            if "spike_depend" not in con or con["spike_depend"] is False:
                if target_id in self.generated_cellid_list:
                    target_obj =self.cells[self.generated_cellid_list.index(target_id)].cell[con["target_synapse"]["section"]["name"]]
                    syn_obj = getattr(neuron.h,con["target_synapse"]["suffix"])(target_obj(con["target_synapse"]["section"]["point"]))
                    for opt in con["synapse_opt"]:
                        setattr(syn_obj,opt[0],opt[1])
                    self.pc.target_var(syn_obj,getattr(syn_obj,"_ref_" + con["target_synapse"]["value"]),index)
            else:
                if target_id in self.generated_cellid_list:
                    gid = index*2 +1
                    self.pc.set_gid2node(gid,self.palcon["id"])
                    target_obj =self.cells[self.generated_cellid_list.index(target_id)].cell[con["target_synapse"]["section"]["name"]]
                    syn_obj = getattr(neuron.h,con["target_synapse"]["suffix"])(target_obj(con["target_synapse"]["section"]["point"]))
                    for opt in con["synapse_opt"]:
                        setattr(syn_obj,opt[0],opt[1])
                    nc = self.pc.gid_connect(gid-1,syn_obj)
                    for opt in con["netcon_opt"]:
                        if opt[0] == "weight":
                            nc.weight[0] = opt[1]
                        else:
                            setattr(nc,opt[0],opt[1])
                    self.nclist.append(nc)
        self.pc.barrier()

    def connect_stim(self):
        self.stim_list = []
        for ele in self.stim_settings:
            if ("spike_stim" not in ele) or ele["spike_stim"] is False:
                if "target_cellname" in ele:
                    id = self.name_to_id[ele["target_cellname"]]
                elif "target_cellid" in ele:
                    id = ele["target_cellid"]
                else:
                    print("each elements of stim file must contain key named target_cellname or target_cellid")
                    exit()
                if id in self.generated_cellid_list:
                    cls_obj = getattr(neuron.h,ele["stimulator"])
                    stim = cls_obj(self.cells[self.generated_cellid_list.index(id)].cell[ele["section"]["name"]](ele["section"]["point"]))
                    for params in ele["opt"].items():
                        setattr(stim, params[0], params[1])
                    self.stim_list.append(stim)
            else:
                if "target_cellname" in ele["synapse"]:
                    id = self.name_to_id[ele["synapse"]["target_cellname"]]
                elif "target_cellid" in ele["synapse"]:
                    id = ele["synapse"]["target_cellid"]
                else:
                    print("synapse must contain key named target_cellname or target_cellid")
                    exit()
                if id in self.generated_cellid_list:
                    cls_obj = getattr(neuron.h,ele["stimulator"])
                    stim = cls_obj()
                    for params in ele["stimulator_opt"].items():
                        setattr(stim, params[0], params[1])
<<<<<<< HEAD
                    syn_obj = getattr(neuron.h,ele["synapse"])
                    syn = syn_obj(self.cells[self.generated_cellid__list.index(id)].cell[ele["synapse"]["section"]["name"]](ele["synapse"]["section"]["point"]))
=======
                    syn_obj = getattr(neuron.h,ele["synapse"]["suffix"])
                    syn = syn_obj(self.cells[self.gidlist.index(id)].cell[ele["synapse"]["section"]["name"]](ele["synapse"]["section"]["point"]))
>>>>>>> 3c7dd4a1c3209725e813a99440f7d3a1b5ac7ed0
                    for params in ele["synapse_opt"].items():
                        setattr(syn, params[0], params[1])
                    ncstim = neuron.h.NetCon(stim,syn)
                    for params in ele["netcon_opt"].items():
                        if params[0] == "weight":
                            ncstim.weight[0] = params[1]
                        else:
                            setattr(ncstim, params[0], params[1])
                    self.stim_list.append(ncstim)

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
