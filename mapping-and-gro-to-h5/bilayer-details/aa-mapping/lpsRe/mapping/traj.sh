#!/bin/bash

grompp -p topol.top -f mdout.mdp -c mem-md-100.gro -o AA-COG.tpr -n index.ndx

no_of_beads=20839
no_of_beads_minus_1=20838

seq 0 $no_of_beads_minus_1 | g_traj -f whole.xtc -s AA-COG.tpr -oxt mapped-traj.pdb -n new2.ndx  -ng ${no_of_beads} -com


rm \#*
