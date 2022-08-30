#!/bin/bash
#SBATCH --job-name=opt_dielec_directional
#SBATCH --account=nn4654k
#SBATCH --time=2-0:0:0
#SBATCH --nodes=40
#SBATCH --ntasks-per-node=64
#SBATCH --cpus-per-task=2

set -o errexit
module load h5py/2.10.0-foss-2020a-Python-3.8.2
module load pfft-python/0.1.21-foss-2020a-Python-3.8.2
set -x

export PYTHONPATH="/cluster/home/${USER}/.local/lib/python3.8/site-packages:${PYTHONPATH}"

# Make Betzy run multiple simultaneous job steps on each node, cf.
# https://documentation.sigma2.no/jobs/guides/running_job_steps_parallel.html
export SLURM_JOB_NUM_NODES=1-$SLURM_JOB_NUM_NODES
unset SLURM_MEM_PER_NODE
export SLURM_MEM_PER_CPU=1952

# OPTIMIZATION CONFIG ==========================================================
source opt_config.sh
# ==============================================================================

# Copy files
export SCRATCH="/cluster/work/users/${USER}/${SLURM_JOB_ID}"
mkdir ${SCRATCH}
mkdir -p ${SLURM_SUBMIT_DIR}/${OUT_DIR}
cd ${SCRATCH}
mkdir ${SCRATCH}/hymd/
mkdir ${SCRATCH}/utils/
cp -r ${HYMD_DIRECTORY}/hymd/*                hymd/
cp -r ${HYMD_DIRECTORY}/utils/*               utils/
cp -r ${SLURM_SUBMIT_DIR}/${CONFIG_INPUT}     ${SCRATCH}/lipid-A.toml
cp -r ${SLURM_SUBMIT_DIR}/${HYMD_INPUT}       ${SCRATCH}/lipid-A-hexa-feb-2022.h5
cp -r ${SLURM_SUBMIT_DIR}/${REF_TRAJECTORY}   ${SCRATCH}/aa-traj.xtc
cp -r ${SLURM_SUBMIT_DIR}/${REF_TOPOLOGY}     ${SCRATCH}/frame90ns.gro
cp -r ${SLURM_SUBMIT_DIR}/${BOUNDS_FILE}      ${SCRATCH}/${BOUNDS_FILE}

# Copy opt. file to $SCRATCH, if opt. file exists
[ -f ${SLURM_SUBMIT_DIR}/${OUT_DIR}/${OPT_FILE} ] && cp ${SLURM_SUBMIT_DIR}/${OUT_DIR}/${OPT_FILE} ${SCRATCH}/opt_data.txt

UNUSED_NUMBER_FILE="unused_number.txt"
NEXT_POINT_FILE="next_point.txt"
PARAMETERS_FILE="parameters.txt"
python3 utils/read_parameter_file.py                                           \
        --bounds-file ${BOUNDS_FILE}                                           \
        --out         ${PARAMETERS_FILE}


# RANDOM SIMULATIONS ===========================================================
for SIM in $(seq 1 ${RANDOM_SIMS}); do
  for M in $(seq 1 ${MULTIPLE}); do
    I=${SIM}
    M_DIR="RSIM_${I}_${M}"

    SEED=$(expr ${RANDOM_SEED} + ${I} \* ${PARALLEL} + 10000 \* ${M})
    python3 utils/get_next_point_random.py                                     \
            --bounds-file ${BOUNDS_FILE}                                       \
            --out         next_point_${M}.txt                                  \
            --random-seed ${SEED}

    PARAMS="$(paste ${PARAMETERS_FILE} next_point_${M}.txt | awk '{
      for (i=1; i<=NF/2; i++) {
        printf "-%s %s\t",$i,$(NF/2+i)
      };
      printf "\n"
    }')"

    python3 utils/change_chi.py ${PARAMS}                                      \
            --config-file lipid-A.toml                                          \
            --out         config_changed_${M}.toml

    for P in $(seq 1 ${PARALLEL}); do
      P_DIR=${M_DIR}/${P}
      mkdir -p ${P_DIR}
      srun --ntasks=${MPI_NUM_RANKS} --cpus-per-task=2 --exclusive --nodes 1   \
           python3 -m hymd  config_changed_${M}.toml  lipid-A-hexa-feb-2022.h5          \
                   --logfile     log_${I}_${M}_${P}.txt               \
                   --verbose     2                                             \
                   --destdir     ${P_DIR}                                      \
                   --seed        $(expr ${SEED} + ${P})  \
		   > /dev/null &                     
    done
  done
  wait

  for M in $(seq 1 ${MULTIPLE}); do
    I=${SIM}
    M_DIR="RSIM_${I}_${M}"

    for P in $(seq 1 ${PARALLEL}); do
      P_DIR=${M_DIR}/${P}
      srun --ntasks=1 --cpus-per-task=1 --exclusive --nodes 1                  \
           python3 utils/hymd_optimize.py  fitness                             \
              --metric          ${METRIC}                                      \
              --resolution      ${RESOLUTION}                                  \
              --traj            ${P_DIR}/sim.H5                                \
              --top             ${SCRATCH}/lipid-A-hexa-feb-2022.h5                              \
              --skip-first      ${SKIP_FIRST}                                  \
              --axis            ${AXIS}                                        \
              --ref-traj        ${SCRATCH}/aa-traj.xtc                             \
              --ref-top         ${SCRATCH}/frame90ns.gro                             \
              --skip-first-ref  ${SKIP_FIRST_REF}                              \
              --axis-ref        ${AXIS_REF}                                    \
              --bins            ${BINS}                                        \
              --out             fitness_${I}_${M}_${P}.txt                     \
              --range           ${RANGE}                                       \
              --symmetrize                                                     \
	      --skip-ref	${SKIP_REF}				       \
              --force                                                          \
              > /dev/null                                                      &
    done
  done
  wait

  for M in $(seq 1 ${MULTIPLE}); do
    python3 utils/write_to_opt_file_parallel.py                                \
            --fitness-file    fitness_${I}_${M}_*.txt                          \
            --parameters-file ${PARAMETERS_FILE}                               \
            --point-file      next_point_${M}.txt                              \
            --opt-file        ${SCRATCH}/opt_data.txt
  done

  cp ${SCRATCH}/opt_data.txt ${SLURM_SUBMIT_DIR}/${OUT_DIR}/${OPT_FILE}
done


# BAYESIAN OPT SIMULATIONS =====================================================
for SIM in $(seq 1 ${SIMS}); do
  for M in $(seq 1 ${MULTIPLE}); do
    I=${SIM}
    M_DIR="SIM_${I}_${M}"
    KAP=${KAPPA[$M]}

    SEED=$(expr ${RANDOM_SEED} + ${I} \* ${PARALLEL} + 10000 \* ${M})
    srun --ntasks=1 --cpus-per-task=1 --exclusive --nodes 1                    \
         python3 utils/get_next_point.py                                       \
            --bounds-file ${BOUNDS_FILE}                                       \
            --out         next_point_${M}.txt                                  \
            --fitness     ${METRIC}                                            \
            --kappa       ${KAP}                                               \
            --random-seed ${SEED}                                              \
            > /dev/null                                                        &
  done
  wait

  for M in $(seq 1 ${MULTIPLE}); do
    M_DIR="SIM_${I}_${M}"
    PARAMS="$(paste ${PARAMETERS_FILE} next_point_${M}.txt | awk '{
      for (i=1; i<=NF/2; i++) {
        printf "-%s %s\t",$i,$(NF/2+i)
      };
      printf "\n"
    }')"

    python3 utils/change_chi.py ${PARAMS}                                      \
            --config-file lipid-A.toml                                          \
            --out         config_changed_${M}.toml

    for P in $(seq 1 ${PARALLEL}); do
      P_DIR=${M_DIR}/${P}
      mkdir -p ${P_DIR}
      srun --ntasks=${MPI_NUM_RANKS} --cpus-per-task=2 --exclusive --nodes 1   \
           python3 -m hymd  config_changed_${M}.toml  lipid-A-hexa-feb-2022.h5              \
                   --logfile     log_${I}_${M}_${P}.txt               \
                   --verbose     2                                             \
                   --destdir     ${P_DIR}                                      \
                   --seed        $(expr ${SEED} + ${P})                        \
                   > /dev/null                                                 &
    done
  done
  wait

  for M in $(seq 1 ${MULTIPLE}); do
    I=${SIM}
    M_DIR="SIM_${I}_${M}"

    for P in $(seq 1 ${PARALLEL}); do
      P_DIR=${M_DIR}/${P}
      srun --ntasks=1 --cpus-per-task=1 --exclusive --exact --nodes 1            \
           python3 utils/hymd_optimize.py  fitness                               \
              --metric          ${METRIC}                                        \
              --resolution      ${RESOLUTION}                                    \
              --traj            ${P_DIR}/sim.H5                                  \
              --top             ${SCRATCH}/lipid-A-hexa-feb-2022.h5              \
              --skip-first      ${SKIP_FIRST}                                    \
              --axis            ${AXIS}                                          \
              --ref-traj        ${SCRATCH}/aa-traj.xtc                           \
              --ref-top         ${SCRATCH}/frame90ns.gro                         \
              --skip-first-ref  ${SKIP_FIRST_REF}                                \
              --axis-ref        ${AXIS_REF}                                      \
              --bins            ${BINS}                                          \
              --out             fitness_${I}_${M}_${P}.txt                       \
              --range           ${RANGE}                                         \
              --symmetrize                                                       \
	      --skip-ref	${SKIP_REF}                                      \
              --force                                                            \
              > /dev/null                                                        &
    done
  done
  wait

  for M in $(seq 1 ${MULTIPLE}); do
    python3 utils/write_to_opt_file_parallel.py                                \
            --fitness-file    fitness_${I}_${M}_*.txt                          \
            --parameters-file ${PARAMETERS_FILE}                               \
            --point-file      next_point_${M}.txt                              \
            --opt-file        ${SCRATCH}/opt_data.txt
  done

  cp ${SCRATCH}/opt_data.txt ${SLURM_SUBMIT_DIR}/${OUT_DIR}/${OPT_FILE}
done
