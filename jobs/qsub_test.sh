#!/bin/bash
#

#PBS -l nodes=2:ppn=28
#PBS -q cluster


export PATH
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
if command -v pyenv 1>/dev/null 2>&1; then
  eval "$(pyenv init -)"
fi
eval "$(pyenv virtualenv-init -)"

pyenv activate cluster

export PYTHONPATH=$PYTHONPATH:/home/tsunoda/lib/python/
EXECPATH="/home/tsunoda/pythonNeuronSimulation"
PYTHONPROGRAM="${EXECPATH}/parallelNeuronSimulation.py"
SIMFILE="${EXECPATH}/testdata/opticlobe/10by10/run.json"

cd $EXECPATH
mpirun python $PYTHONPROGRAM -s $SIMFILE

