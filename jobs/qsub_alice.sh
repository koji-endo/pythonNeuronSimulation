#!/bin/bash

#PBS -l nodes=1:ppn=68
#PBS -q xeonphi

cd $PBS_O_WORKDIR
mpirun /bin/hostname

