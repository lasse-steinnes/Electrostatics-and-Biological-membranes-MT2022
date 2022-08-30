
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


## Making a density profile
To make a density profile from the aa trajectory mapped as CG, Then
```bash ==
python3 hymd_optimize.py plot --traj aa-traj.xtc --top frame90ns.gro --skip-first 0 --resolution types --bins 100 --no-marker --range 8 --ignore "all" "solvent" "name:.*" "lipid:.*" "ions"  --symmetrize
```

## Testing fitness

```bash == python3 hymd_optimize.py fitness --traj sim-la-alias.H5 --top lipid-A-hexa-feb-2022.h5 --skip-first 5 --frames 10 --axis 2  --ref-traj aa-traj.xtc --ref-top frame90ns.gro --skip-first-ref 0  --axis-ref 2 --resolution types  --bins 100 --no-marker --out fitness_test.txt --range 8 --symmetrize --force
```

Output from python3 hymd_optimize.py -h:

usage: hymd_optimize.py [-h] [--out file name] [--no-show] [--save-plot] [--force] [--one-side] [--xlim XLIM XLIM] [--ylim YLIM YLIM] [--ref-traj REF_TRAJ] [--ref-top REF_TOP] [--traj TRAJ] [--top TOP] [--bins BINS] [--density] [--symmetrize] [--range RANGE] [--area-per-lipid]
                        [--axis {0,1,2}] [--axis-ref {0,1,2}] [--ignore IGNORE [IGNORE ...]] [--resolution {types,names}] [--remove-xlabel] [--remove-ylabel] [--remove-yticks] [--remove-xticks] [--remove-legend] [--tight] [--no-marker] [--skip SKIP] [--skip-first SKIP_FIRST]
                        [--frames FRAMES] [--skip-ref SKIP_REF] [--skip-first-ref SKIP_FIRST_REF] [--frames-ref FRAMES_REF] [--metric {MSE,RMSE,MAE,MAPE,SMAPE,R2}] [--vmd-colors]
                        {plot,fitness,fitness-range}

Tools for HyMD parameter optimization and fitness calculation

positional arguments:
  {plot,fitness,fitness-range}
                        action to perform

optional arguments:
  -h, --help            show this help message and exit
  --out file name       output file path
  --no-show, --noshow   do not show the plot
  --save-plot           save the histogram plot to this file path
  --force, -f           overwrite existing output file path
  --one-side, --oneside
                        only plot one side of the membrane
  --xlim XLIM XLIM, --x-lim XLIM XLIM
                        x-axis limits to use for the plot
  --ylim YLIM YLIM, --y-lim YLIM YLIM
                        y-axis limits to use for the plot
  --ref-traj REF_TRAJ   refence trajectory file path (.trr)
  --ref-top REF_TOP     refence topology file path (.gro)
  --traj TRAJ           test trajectory file path (.trr or .H5MD)
  --top TOP             test topology file path (.gro or HyMD-input .H5)
  --bins BINS           number of bins to use in the histograms and histogram plots
  --density             compute density distribution histograms, not the number density
  --symmetrize          symmetrize the histogram(s) by averaging the histogram(s) and the flipped histogram.
  --range RANGE         histogram x range to consider
  --area-per-lipid      Include the area per lipid in the fitness calculation
  --axis {0,1,2}        the direction in which to calculate the histogram(s)
  --axis-ref {0,1,2}    the direction in which to calculate the reference histogram(s)
  --ignore IGNORE [IGNORE ...]
                        species names to ignore in the calculation of the histograms (evaluated as list of regex expressions)
  --resolution {types,names}
                        if 'names', the specific Martini particle subspecies names (NC3, PO4, etc.) are compared in the fitness. If 'types', particle types (N, P, G, etc.) are compared in the fitness
  --remove-xlabel       do not show the xlabel in the plot
  --remove-ylabel       do not show the ylabel in the plot
  --remove-yticks       do not show the y ticks in the plot
  --remove-xticks       do not show the x ticks in the plot
  --remove-legend       do not show legend in the plot
  --tight, -tight       use matplotlib tight_layout for the plot
  --no-marker, -no-marker, -nomarker, --nomarker
                        dont show line markers
  --skip SKIP           consider only every N frames when calculating the histograms
  --skip-first SKIP_FIRST
                        skip the first N frames when calculating the histograms
  --frames FRAMES       Only consider N frames, starting at --skip_first (with step size --skip).
  --skip-ref SKIP_REF   consider only every N reference frames when calculating the histograms
  --skip-first-ref SKIP_FIRST_REF
                        skip the first N reference frames when calculating the histograms
  --frames-ref FRAMES_REF
                        Only consider N reference frames, starting at --skip_first (with step size --skip).
  --metric {MSE,RMSE,MAE,MAPE,SMAPE,R2}
                        which fitness metric to use in the fitness-range
  --vmd-colors, --vmdcolors, -vmdcolors
                        use the same colors for beads as default in vmd

## Notes:
- test refers to the h5
  - inputfile is topology
  - traj  is the simulation h5
  - do witouth skip frame and the problem with 8.0 might go away.
- If you give fitness instead of plot, it will instead of plotting the density profile,
  calculate the fitness

- pressure added as penalty:

 python3 hymd_optimize.py fitness --traj cal-la.H5 --top lipid-A-hexa-feb-2022-reduced-box.h5 --skip-first 0 --frames 20 --axis 2  --ref-traj aa-traj.xtc --ref-top frame90ns.gro --skip-first-ref 0  --axis-ref 2 --resolution types  --bins 100 --no-marker --out fitness_test.txt --range 8 --symmetrize --force --surface-tension

  python3 hymd_optimize.py fitness --traj sim-la-alias.H5 --top lipid-A-hexa-feb-2022.h5 --skip-first 0 --frames 400 --axis 2  --ref-traj aa-traj.xtc --ref-top frame90ns.gro --skip-first-ref 0  --axis-ref 2 --resolution types  --bins 100 --no-marker --out fitness_test.txt --range 8 --symmetrize --force --surface-tension --area-per-lipid


 ##  Plotting the density profiles examples
 python3 hymd_optimize.py plot --traj sim-la-914.H5 --top lipid-A-hexa-smaller-system-23march-area-91-4.H5 --skip-first 0 --resolution types --bins 100 --no-marker --range 8 --ignore "all" "solvent" "name:.*" "lipid:.*" "ions"  --symmetrize

 python3 hymd_optimize.py plot --traj sim-la-alias.H5 --top lipid-A-hexa-feb-2022.h5 --skip-first 0 --frames 400 --resolution types --bins 100 --no-marker --range 8 --ignore "all" "solvent" "name:.*" "lipid:.*" "ions"  --symmetrize


 ##   To thesis     

Plots to thesis:

python3 hymd_optimize.py plot --traj gpe-Flory-huggins.H5 --top lipid-A-hexa-feb-2022.h5 --skip-first 5 --resolution types --bins 100 --no-marker --range 9.39 --ignore "all" "solvent" "name:.*" "lipid:.*" "ions"  --symmetrize

python3 hymd_optimize.py plot --traj gpe-lower-FH.H5 --top lipid-A-hexa-feb-2022.h5 --skip-first 5 --resolution types --bins 100 --no-marker --range 9.39 --ignore "all" "solvent" "name:.*" "lipid:.*" "ions"  --symmetrize

python3 hymd_optimize.py plot --traj eps15-flory-huggins.H5 --top lipid-A-hexa-feb-2022.h5 --skip-first 5 --resolution types --bins 100 --no-marker --range 9.39 --ignore "all" "solvent" "name:.*" "lipid:.*" "ions"  --symmetrize

python3 hymd_optimize.py plot --traj eps80-flory-huggins.H5 --top lipid-A-hexa-feb-2022.h5 --skip-first 5 --resolution types --bins 100 --no-marker --range 9.39 --ignore "all" "solvent" "name:.*" "lipid:.*" "ions"  --symmetrize

python3 hymd_optimize.py plot --traj la6-PE-BO.H5 --top lipid-A-hexa-feb-2022.h5 --skip-first 5 --resolution types --bins 100 --no-marker --range 9.39 --ignore "all" "solvent" "name:.*" "lipid:.*" "ions"  --symmetrize

python3 hymd_optimize.py plot --traj la6-gpe-BO.H5 --top lipid-A-hexa-feb-2022.h5 --skip-first 5 --resolution types --bins 100 --no-marker --range 9.39 --ignore "all" "solvent" "name:.*" "lipid:.*" "ions"  --symmetrize

python3 hymd_optimize.py plot --traj aa-traj.xtc --top frame90ns.gro --skip-first 0 --resolution types --bins 100 --no-marker --range 8 --ignore "all" "solvent" "name:.*" "lipid:.*" "ions"  --symmetrize
-lipid --skip-ref 20

fitness to thesis:

python3 hymd_optimize.py fitness --traj gpe-Flory-huggins.H5 --top lipid-A-hexa-feb-2022.h5 --skip-first 5 --axis 2  --ref-traj aa-traj.xtc --ref-top frame90ns.gro --skip-first-ref 0  --axis-ref 2 --resolution types  --bins 100 --no-marker --out fitness-gpe-FH.txt --range 8 --symmetrize --force

python3 hymd_optimize.py fitness --traj gpe-lower-FH.H5 --top lipid-A-hexa-feb-2022.h5 --skip-first 5 --axis 2  --ref-traj aa-traj.xtc --ref-top frame90ns.gro --skip-first-ref 0  --axis-ref 2 --resolution types  --bins 100 --no-marker --out fitness-gpe-lower-FH.txt --range 8 --symmetrize --force

python3 hymd_optimize.py fitness --traj eps15-flory-huggins.H5 --top lipid-A-hexa-feb-2022.h5 --skip-first 5 --axis 2  --ref-traj aa-traj.xtc --ref-top frame90ns.gro --skip-first-ref 0  --axis-ref 2 --resolution types  --bins 100 --no-marker --out fitness-eps15-FH.txt --range 8 --symmetrize --force

python3 hymd_optimize.py fitness --traj eps80-flory-huggins.H5 --top lipid-A-hexa-feb-2022.h5 --skip-first 5 --axis 2  --ref-traj aa-traj.xtc --ref-top frame90ns.gro --skip-first-ref 0  --axis-ref 2 --resolution types  --bins 100 --no-marker --out fitness-eps80-FH.txt --range 8 --symmetrize --force

python3 hymd_optimize.py fitness --traj la6-PE-BO.H5 --top lipid-A-hexa-feb-2022.h5 --skip-first 5 --axis 2  --ref-traj aa-traj.xtc --ref-top frame90ns.gro --skip-first-ref 0  --axis-ref 2 --resolution types  --bins 100 --no-marker --out fitness-eps80-BO.txt --range 8 --symmetrize --force

python3 hymd_optimize.py fitness --traj la6-gpe-BO.H5 --top lipid-A-hexa-feb-2022.h5 --skip-first 5 --axis 2  --ref-traj aa-traj.xtc --ref-top frame90ns.gro --skip-first-ref 0  --axis-ref 2 --resolution types  --bins 100 --no-marker --out fitness-gpe-BO.txt --range 8 --symmetrize --force
