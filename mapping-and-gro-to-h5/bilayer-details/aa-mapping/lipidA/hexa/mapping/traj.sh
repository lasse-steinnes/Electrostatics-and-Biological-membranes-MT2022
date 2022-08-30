#!/bin/bash

grompp -p topol.top -f md.mdp -c mem-md-initial.gro -o AA-COG.tpr

no_of_beads=16980
no_of_beads_minus_1=16979

seq 0 $no_of_beads_minus_1 | g_traj -f whole.xtc -s AA-COG.tpr -oxt mapped-traj.pdb -n new2.ndx  -ng ${no_of_beads} -com


rm \#*
