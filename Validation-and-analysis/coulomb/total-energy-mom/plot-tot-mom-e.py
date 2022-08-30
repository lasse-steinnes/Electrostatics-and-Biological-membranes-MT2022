"""
Plot of total energy and momentum by reading of HDF5 trajectory
"""

import h5py
import numpy as np
import matplotlib.pyplot as plt

### Accesss simulation files
def get(file_path):
    f = h5py.File(file_path,"r")
    energy = f["/observables/total_energy/value"] # total energy!
    mom = f["/observables/total_momentum/value"] # total momentum
    time = f["/observables/field_q_energy/time"] # in picoseconds

    pico_to_nano = 1e-3
    time = np.array(time) #*pico_to_nano
    energy = np.array(energy)
    mom = np.array(mom)
    s = np.shape(mom)[0]
    mom_x  = np.zeros(s); mom_y = np.zeros(s); mom_z = np.zeros(s)
    for i in range(s):
        mom_x[i] = mom[i,0]
        mom_y[i] = mom[i,1]
        mom_z[i] = mom[i,2]

    return [energy, mom_x, mom_y ,mom_z, time]

### plot details
fs = 30
width = 3
ms = 14
fs_leg = 25
###

## GPE
file_path = "./results-coulomb-NVE-const/sim.H5"
energy, mom_x, mom_y, mom_z, time = get(file_path)

## GPE
file_path2 = "./results-coulomb-NVE-dielec-f/sim.H5"
energy2, mom_x2, mom_y2, mom_z2, time = get(file_path)

L = "dotted"
l = "dashed"
s = "solid"

# energy
plt.figure(figsize = (10,8))
plt.plot(time, energy,linestyle = s,marker = "|", color = "purple", markersize = ms, linewidth = width, label = r"$\epsilon_r = 1$")
plt.xlabel("time [ps]",fontsize = fs)
plt.ylabel(r" E$_{tot}$ [kJ mol$^{-1}$]",fontsize = fs)
plt.legend(fontsize = fs_leg)
plt.xticks(fontsize = fs)
plt.yticks(fontsize = fs)
plt.ylim([100,140])
plt.tight_layout()
plt.savefig("./tot-energies.pdf", format = "pdf")
plt.show()


# mom
plt.figure(figsize = (10,8))
plt.plot(time, mom_x ,linestyle = l,markersize = ms, linewidth = width,  label = r"x")
plt.plot(time, mom_y ,linestyle = l,markersize = ms, linewidth = width,  label = r"y")
plt.plot(time, mom_z ,linestyle = l,markersize = ms, linewidth = width,  label = r"z")
plt.ylabel(r" p$_{tot}$ [u nm ps$^{-1}$]",fontsize = fs)
plt.xlabel("time [ps]",fontsize = fs)
plt.legend(fontsize = fs_leg)
plt.xticks(fontsize = fs)
plt.yticks(fontsize = fs)
plt.ylim(-0.01,0.01)
plt.tight_layout()
plt.savefig("./tot-momentum.pdf", format = "pdf")
plt.show()
