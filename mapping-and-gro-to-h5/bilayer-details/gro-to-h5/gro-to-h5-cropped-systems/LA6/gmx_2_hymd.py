##### import libaries
import numpy as np
import os
import sys
sys.path.append('/Users/Lasse/Documents/GitHub/Ms-CS-Physics/HyMD/utils/')
from topologyParser import *
import pandas as pd

print('---------------------- start ')


################# generate atomtype csv, before is based on the fort file,
##### here is based on the forcefield_verbose.itp
atomtype_id     = np.array([  1,    2,     3,     4,   5,   6])
atomtype_name   = np.array([ 'P', 'L',   'G',   'C',   'N',   'W'])
atomtype_mass   = np.array([72.0,  72.0,  72.0,  72.0, 72.0,    72.0])
atomtype_charge = np.array([ -1.0,  0.0,   0.0, 0.0,  +2.0,    0.0  ])
df = pd.DataFrame({ 'atomtypeID': atomtype_id,
                           'atomName':atomtype_name,
                           'atomMass':atomtype_mass,
                           'atomCharge':atomtype_charge}
                        )
atomtype_csv = os.path.join('./', 'atomtype.csv')
df.to_csv(atomtype_csv, index=False)
##  bond terms

work_folder = './'

out_h5_filename = 'lipid-A-hexa-feb-2022-reduced-box.h5'
out_h5_file     = os.path.join(work_folder, out_h5_filename)
in_gro_file     = os.path.join(work_folder, 'frame90ns_new.gro')


in_top_name = 'lipid-A-v1.top'
in_top_file = os.path.join(work_folder, in_top_name)

### here the top_file could also be the top_csv top_mol_dict
electric_label  =  True
alias_mol_dict  =  {
    'LA6' : 'LA6',
    'W' : 'SOL',
    'N' : 'N',
}
## the key is the molecule name from the gmx top
## the value is the hpf itp files in the save folder as atomtype_csv (some funciton will asume this...)
##

gmx_to_h5_from_more_hand(out_h5_file, in_gro_file, in_top_file, atomtype_csv, alias_mol_dict, electric_label) ## atomtype_csv is needed change from atomtypeID to atomtypeName(atomName)
