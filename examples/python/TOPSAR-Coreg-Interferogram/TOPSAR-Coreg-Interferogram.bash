#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=01:00:00
#SBATCH --cpus-per-task=4
#SBATCH --partition=short

module load snap
module load python/3.10

source ../../../venv/bin/activate

DATA_DIR="/project/caroline/Data/radar_data/sentinel1/s1_asc_t088/"
MOTHER_PATH=${DATA_DIR}/IW_SLC__1SDV_VVVH/20250404/S1A_IW_SLC__1SDV_20250404T172547_20250404T172614_058610_07414D_AC68.zip
DAUGHTER_PATH=${DATA_DIR}/IW_SLC__1SDV_VVVH/20250416/S1A_IW_SLC__1SDV_20250416T172546_20250416T172614_058785_074873_228C.zip

AOI_WKT="POLYGON ((5.111186 52.990841, 5.111186 53.31203, 4.704692 53.31203, 4.704692 52.990841, 5.111186 52.990841))"
NCORES=${SLURM_CPUS_PER_TASK}

time python TOPSAR-Coreg-Interferogram.py \
  -q ${NCORES} \
  --mother-path ${MOTHER_PATH} \
  --daughter-paths ${DAUGHTER_PATH} \
  --aoi-wkt "${AOI_WKT}" #--view > graph.xml

