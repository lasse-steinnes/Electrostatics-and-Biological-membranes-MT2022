#!/bin/bash
#SBATCH --job-name=HyMD-biphase
#SBATCH --account=nn4654k
#SBATCH --time=1-0:0:0
#SBATCH --ntasks=16
#SBATCH --mem-per-cpu=1G 

module --quiet purge
set -o errexit # exit on errors
module load h5py/2.10.0-foss-2020a-Python-3.8.2
module load pfft-python/0.1.21-foss-2020a-Python-3.8.2 
export PYTHONPATH="/cluster/home/${USER}/.local/lib/python3.8/site-packages:${PYTHONPATH}"
set -x

OUT_DIR=${SLURM_SUBMIT_DIR}
CASE=${OUT_DIR}/eps5-sigma-tweak-ions-5-lower-mesh

mkdir -p ${CASE}

date
srun -n 16 python3 -m hymd config-5mM-eps-C-tweak.toml partition5mM.h5  --logfile=log_eps5-tweak.txt --verbose 2 --velocity-output --destdir ${CASE} --seed 10  
