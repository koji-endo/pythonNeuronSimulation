import sys
import numpy as np
sys.path.append("/home/hayato/lib/python")
import neuron
from HHneuron import HHneuron


def setStimulus(neuron_list, stim_settings):
    stim_list = []
    for ele in stim_settings:
        stim = neuron.h.IClamp(neuron_list[ele[0]].soma(0.5))
        stim.delay = ele[1]
        stim.dur = ele[2]
        stim.amp = ele[3]
        stim_list.append(stim)
    return stim_list
