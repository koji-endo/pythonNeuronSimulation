#!/bin/bash
#

#PBS -l nodes=2:ppn=28
#PBS -q cluster
EXECPATH="/home/tsunoda/pythonNeuronSimulation"
PYTHONPROGRAM="${EXECPATH}/parallelNeuronSimulation.py"
SIMFILE="${EXECPATH}/testdata/opticlobe/actual/run.json"

cd $EXECPATH
mpirun python $PYTHONPROGRAM -s $SIMFILE

