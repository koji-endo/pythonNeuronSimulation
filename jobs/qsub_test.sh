#!/bin/bash
#
EXECPATH="/home/tsunoda/pythonNeuronSimulation"
PYTHONPROGRAM="${EXECPATH}/parallelNeuronSimulation.py"
SIMFILE="${EXECPATH}/testdata/retina_l1l2l4_simulation"

mpiexec -np 8 python $PYTHONPROGRAM -f $SIMFILE

