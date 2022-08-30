HYMD_DIRECTORY="/cluster/home/${USER}/HyMD-pressure"

# Bayesian opt. parameters
OPT_FILE="opt_data.txt"  # use existing data, or start from scratch if file does
                         # not exist
BOUNDS_FILE="bounds-la.txt" # specify variables and their allowed ranges
METRIC="SMAPE"           # "MSE" or "RMSE" or "MAE" or "MAPE" or "R2" or "SMAPE"
RESOLUTION="types"       # "types" or "names"
BINS=81                  # histogram bins
RANGE="8.0"              # histogram binning range (-RANGE/2, RANGE/2) from the
                         # bilayer midpoint
OUT_DIR="hymd-opt-out"   # output directory inside ${SLURM_SUBMIT_DIR}
RANDOM_SIMS=10            # random simulations before the bayesian opt starts
SIMS=1000000              # iterations of the bayesian opt
SKIP_REF=20           # skipping every 20 reference frames (large reference)
# opt. exploration/exploitation trade-off parameter
KAPPA=(DO_NOT_USE_FIRST_ELEMENT 0.001 0.01 0.1 0.5 1.0 1.5 2.0 5.0 10.0 100.0)

PARALLEL=10              # number of parallel simulations for each parameter set
MULTIPLE=8               # number of different parameter sets to simulate
RANDOM_SEED=1

# Parallelization specification
export OMP_NUM_THREADS=2
export NODES=1           # nodes per simulation (NOT total nodes for the job)
export MPI_NUM_RANKS=30  # cpus per simulation (NOT total cpus for the job)

# HyMD input
HYMD_INPUT="lipid-A-hexa-feb-2022.h5"
CONFIG_INPUT="lipid-A.toml"

# Reference structure
REF_TOPOLOGY="frame90ns.gro"
REF_TRAJECTORY="aa-traj.xtc"

# HyMD profile specifications
SKIP_FIRST=75
AXIS=2                   # x (0) or y (1) or z (2)

# Reference profile specifications
SKIP_FIRST_REF=100
AXIS_REF=2               # x (0) or y (1) or z (2)
