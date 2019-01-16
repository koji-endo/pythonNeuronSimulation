#!/bin/bash
#

#PBS -l nodes=1:ppn=40
#PBS -q xeonphi

export PATH
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
if command -v pyenv 1>/dev/null 2>&1; then
  eval "$(pyenv init -)"
fi
eval "$(pyenv virtualenv-init -)"

pyenv activate alice

export PYTHONPATH=$PYTHONPATH:/home/tsunoda/mpi4py-3.0.0/build/lib.linux-x86_64-2.7:/home/tsunoda/alice/lib/python
export PATH=$PATH:/usr/local/openmpi-1.10.4-gnu64.4.8.5/bin
EXECPATH="/home/tsunoda/pythonNeuronSimulation"
PYTHONPROGRAM="${EXECPATH}/parallelNeuronSimulation.py"
SIMFILE="${EXECPATH}/testdata/opticlobe/whole10by10/run0.json"

cd $EXECPATH
nrnivmodl mods/

SIMFILE="${EXECPATH}/testdata/opticlobe/whole10by10/runs.json"
mpirun python $PYTHONPROGRAM -s $SIMFILE
SIMFILE="${EXECPATH}/testdata/opticlobe/whole10by10/runss.json"
mpirun python $PYTHONPROGRAM -s $SIMFILE
