#!/bin/bash

for ncores in 1 2 4 6 8 ; do
  sbatch --cpus-per-task=${ncores} TOPSAR-Coreg-Interferogram.bash
done
