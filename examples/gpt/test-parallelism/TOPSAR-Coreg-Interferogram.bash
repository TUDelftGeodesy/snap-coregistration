#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=00:30:00
#SBATCH --cpus-per-task=1
#SBATCH --partition=normal

graph=TOPSAR-Coreg-Interferogram.xml
properties=TOPSAR-Coreg-Interferogram.properties
sourceDir=/project/caroline/Data/radar_data/sentinel1/s1_asc_t088/
sourcePath1=${sourceDir}/IW_SLC__1SDV_VVVH/20250416/S1A_IW_SLC__1SDV_20250416T172546_20250416T172614_058785_074873_228C.zip
sourcePath2=${sourceDir}/IW_SLC__1SDV_VVVH/20250428/S1A_IW_SLC__1SDV_20250428T172547_20250428T172614_058960_074FA0_4F0C.zip
targetDir=./
targetPath=${targetDir}/coreg-${SLURM_CPUS_PER_TASK}.dim  # avoid overwriting
# targetPath=${targetDir}/coreg.znap
format=BEAM-DIMAP
# format=ZNAP
userdir=${TMPDIR}  # save auxiliary data to local disk

module load snap

# print diagnostics information
gpt -q ${SLURM_CPUS_PER_TASK} --diag 

echo "### Starting graph execution on `date` ###"
echo "Running with max parallelism q=${SLURM_CPUS_PER_TASK}"

# execute graph
time gpt \
  -q ${SLURM_CPUS_PER_TASK} \
  -Dsnap.userdir=${userdir} \
  ${graph} \
  -e -p ${properties} \
  -Ssource1=${sourcePath1} \
  -Ssource2=${sourcePath2} \
  -t ${targetPath} \
  -f ${format}

echo "### Ending graph execution on `date` ###"
