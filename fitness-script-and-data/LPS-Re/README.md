
# Investigation of optimization
How the hymd_optimize is called at betzy , to compare the two.

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
             --force    

## More info
See the Readme for LA6 fitness.

## Fitness to thesis: 
* LA6

python3 hymd_optimize.py fitness --traj gpe-Flory-huggins.H5 --top lipid-A-hexa-feb-2022.h5 --skip-first 5 --axis 2  --ref-traj aa-traj.xtc --ref-top frame90ns.gro --skip-first-ref 0  --axis-ref 2 --resolution types  --bins 100 --no-marker --out fitness-gpe-FH.txt --range 8 --symmetrize --force

python3 hymd_optimize.py fitness --traj gpe-lower2-FH.H5 --top lipid-A-hexa-feb-2022.h5 --skip-first 5 --axis 2  --ref-traj aa-traj.xtc --ref-top frame90ns.gro --skip-first-ref 0  --axis-ref 2 --resolution types  --bins 100 --no-marker --out fitness-gpe-lower-FH.txt --range 8 --symmetrize --force

python3 hymd_optimize.py fitness --traj eps15-flory-huggins.H5 --top lipid-A-hexa-feb-2022.h5 --skip-first 5 --axis 2  --ref-traj aa-traj.xtc --ref-top frame90ns.gro --skip-first-ref 0  --axis-ref 2 --resolution types  --bins 100 --no-marker --out fitness-eps15-FH.txt --range 8 --symmetrize --force

python3 hymd_optimize.py fitness --traj eps80-flory-huggins.H5 --top lipid-A-hexa-feb-2022.h5 --skip-first 5 --axis 2  --ref-traj aa-traj.xtc --ref-top frame90ns.gro --skip-first-ref 0  --axis-ref 2 --resolution types  --bins 100 --no-marker --out fitness-eps80-FH.txt --range 8 --symmetrize --force

* Lre5

python3 hymd_optimize.py fitness --traj lre5-eps15.H5 --top lps-Re-mar-2022-full.h5 --skip-first 5 --axis 2  --ref-traj aa-traj.xtc --ref-top frame90ns.gro --skip-first-ref 0  --axis-ref 2 --resolution types  --bins 100 --no-marker --out fitness-lre-eps15-FH.txt --range 8 --symmetrize --force

python3 hymd_optimize.py fitness --traj lre-eps80.H5 --top lps-Re-mar-2022-full.h5 --skip-first 5 --axis 2  --ref-traj aa-traj.xtc --ref-top frame90ns.gro --skip-first-ref 0  --axis-ref 2 --resolution types  --bins 100 --no-marker --out fitness-lre-eps80-FH.txt --range 8 --symmetrize --force

python3 hymd_optimize.py fitness --traj lre5-gpe.H5 --top lps-Re-mar-2022-full.h5 --skip-first 5 --axis 2  --ref-traj aa-traj.xtc --ref-top frame90ns.gro --skip-first-ref 0  --axis-ref 2 --resolution types  --bins 100 --no-marker --out fitness-lre-gpe-FH.txt --range 8 --symmetrize --force

python3 hymd_optimize.py fitness --traj lre-gpe-lower.H5 --top lps-Re-mar-2022-full.h5 --skip-first 5 --axis 2  --ref-traj aa-traj.xtc --ref-top frame90ns.gro --skip-first-ref 0  --axis-ref 2 --resolution types  --bins 100 --no-marker --out fitness-lre-gpe-lower-FH.txt --range 8 --symmetrize --force

python3 hymd_optimize.py fitness --traj lre5-GPE-BO.H5 --top lps-Re-mar-2022-full.h5 --skip-first 5 --axis 2  --ref-traj aa-traj.xtc --ref-top frame90ns.gro --skip-first-ref 0  --axis-ref 2 --resolution types  --bins 100 --no-marker --out fitness-lre-gpe-BO.txt --range 8 --symmetrize --force

python3 hymd_optimize.py fitness --traj lre5-PE-BO.H5 --top lps-Re-mar-2022-full.h5 --skip-first 5 --axis 2  --ref-traj aa-traj.xtc --ref-top frame90ns.gro --skip-first-ref 0  --axis-ref 2 --resolution types  --bins 100 --no-marker --out fitness-lre-pe-BO.txt --range 8 --symmetrize --force

Plots to thesis:

* LA6

python3 hymd_optimize.py plot --traj gpe-Flory-huggins.H5 --top lipid-A-hexa-feb-2022.h5 --skip-first 5 --resolution types --bins 100 --no-marker --range 9.39 --ignore "all" "solvent" "name:.*" "lipid:.*" "ions"  --symmetrize

python3 hymd_optimize.py plot --traj gpe-lower2-FH.H5 --top lipid-A-hexa-feb-2022.h5 --skip-first 5 --resolution types --bins 100 --no-marker --range 9.39 --ignore "all" "solvent" "name:.*" "lipid:.*" "ions"  --symmetrize

python3 hymd_optimize.py plot --traj eps15-flory-huggins.H5 --top lipid-A-hexa-feb-2022.h5 --skip-first 5 --resolution types --bins 100 --no-marker --range 9.39 --ignore "all" "solvent" "name:.*" "lipid:.*" "ions"  --symmetrize

python3 hymd_optimize.py plot --traj eps80-flory-huggins.H5 --top lipid-A-hexa-feb-2022.h5 --skip-first 5 --resolution types --bins 100 --no-marker --range 9.39 --ignore "all" "solvent" "name:.*" "lipid:.*" "ions"  --symmetrize

python3 hymd_optimize.py plot --traj aa-traj.xtc --top frame90ns.gro --skip-first 0 --resolution types --bins 100 --no-marker --range 8 --ignore "all" "solvent" "name:.*" "lipid:.*" "ions"  --symmetrize

* Lre

python3 hymd_optimize.py plot --traj aa-traj.xtc --top frame90ns.gro --skip-first 0 --resolution types --bins 100 --no-marker --range 8 --ignore "all" "solvent" "name:.*" "lipid:.*" "ions"  --symmetrize --skip 20

python3 hymd_optimize.py plot --traj lre-eps80.H5 --top lps-Re-mar-2022-full.h5 --skip-first 5 --resolution types --bins 100 --no-marker --range 9.39 --ignore "all" "solvent" "name:.*" "lipid:.*" "ions"  --symmetrize

python3 hymd_optimize.py plot --traj lre5-eps15.H5 --top lps-Re-mar-2022-full.h5 --skip-first 5 --resolution types --bins 100 --no-marker --range 9.39 --ignore "all" "solvent" "name:.*" "lipid:.*" "ions"  --symmetrize

python3 hymd_optimize.py plot --traj lre5-gpe.H5 --top lps-Re-mar-2022-full.h5 --skip-first 5 --resolution types --bins 100 --no-marker --range 9.39 --ignore "all" "solvent" "name:.*" "lipid:.*" "ions"  --symmetrize

python3 hymd_optimize.py plot --traj lre5-GPE-BO.H5 --top lps-Re-mar-2022-full.h5 --skip-first 5 --resolution types --bins 100 --no-marker --range 9.39 --ignore "all" "solvent" "name:.*" "lipid:.*" "ions"  --symmetrize

python3 hymd_optimize.py plot --traj lre5-PE-BO.H5 --top lps-Re-mar-2022-full.h5 --skip-first 5 --resolution types --bins 100 --no-marker --range 9.39 --ignore "all" "solvent" "name:.*" "lipid:.*" "ions"  --symmetrize
