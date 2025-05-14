#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=01:00:00
#SBATCH --cpus-per-task=4
#SBATCH --partition=normal

module load snap
module load python/3.10

DATA_DIR="/project/caroline/Data/radar_data/sentinel1/s1_asc_t088/"
MOTHER_PATH=${DATA_DIR}/IW_SLC__1SDV_VVVH/20250416/S1A_IW_SLC__1SDV_20250416T172546_20250416T172614_058785_074873_228C.zip
DAUGHTER_PATH=${DATA_DIR}/IW_SLC__1SDV_VVVH/20250428/S1A_IW_SLC__1SDV_20250428T172547_20250428T172614_058960_074FA0_4F0C.zip
AOI_WKT="POLYGON ((5.111186 52.990841, 5.111186 53.31203, 4.704692 53.31203, 4.704692 52.990841, 5.111186 52.990841))"

time python3.10 TOPSAR-Coreg-Interferogram.py \
  -q ${SLURM_CPUS_PER_TASK} \
  --mother-path "${MOTHER_PATH}" \
  --daughter-path "${DAUGHTER_PATH}" \
  --aoi-wkt "${AOI_WKT}" # --view
