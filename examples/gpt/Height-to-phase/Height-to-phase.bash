#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=01:00:00
#SBATCH --cpus-per-task=1
#SBATCH --partition=normal

graph=Height-to-phase.xml
properties=Height-to-phase.properties
sourceDir=/project/caroline/Data/radar_data/sentinel1/s1_asc_t088/
sourcePath1=${sourceDir}/IW_SLC__1SDV_VVVH/20250416/S1A_IW_SLC__1SDV_20250416T172546_20250416T172614_058785_074873_228C.zip
sourcePath2=${sourceDir}/IW_SLC__1SDV_VVVH/20250428/S1A_IW_SLC__1SDV_20250428T172547_20250428T172614_058960_074FA0_4F0C.zip
outDir=./
date1=16Apr2025
date2=28Apr2025
formatName=BEAM-DIMAP
h2phOut=${outDir}/h2ph.dim
# Interferograms with/without topographic phase only to debug
# ifgs_srd_out=${outDir}/ifgs_srd.dim
# ifgs_srp_out=${outDir}/ifgs_srp.dim
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
  -Pdate1=${date1} \
  -Pdate2=${date2} \
  -PformatName=${formatName} \
  -Ph2phOut=${h2phOut} #-Pifgs_srd_out=${ifgs_srd_out} -Pifgs_srp_out=${ifgs_srp_out}

echo "### Ending graph execution on `date` ###"
