"""
Plot electrostatic energies from PE and GPE
"""
import h5py
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import gammainc as regularized_lower_incomplete_gamma # gaussian coulomb
from scipy.special import gamma # gaussian coulomb

def lower_incomplete_gamma(a, x):
    return regularized_lower_incomplete_gamma(a, x) * gamma(a)

# Boys function, Fn(x)
def Fn(n, x):
    return lower_incomplete_gamma(n + 0.5, x) / (2 * x**(n + 0.5))

def W_gaussian(rij):
    sigma = 0.5
    charge_i = + 1.0
    charge_j = - 1.0

    k_electric = 138.935458
    k_electric_qi_qj = k_electric * charge_i * charge_j
    pi = np.arccos(-1.0)
    Wij = k_electric_qi_qj * Fn(0, rij**2 / (4 * sigma**2)) / (sigma * np.sqrt(pi))  # noqa: E501
    return Wij


def W_coulomb(rij, charge_i = + 1.0, charge_j = - 1.0):
    k_electric = 138.935458
    k_electric_qi_qj = k_electric * charge_i * charge_j
    return k_electric_qi_qj / rij

### Accesss simulation files
def get(file_path, plot = False):
    f = h5py.File(file_path,"r")
    energy = f["/observables/field_q_energy/value"]
    time = f["/observables/field_q_energy/time"] # in picoseconds
    positions = f["/particles/all/position/value"]

    last_frame = int(101)
    pico_to_nano = 1e-3

    time = np.array(time[0:last_frame]) #*pico_to_nano
    positions = np.array(positions)
    shapes = np.shape(positions)
    energy = np.array(energy)

    pos = np.zeros((shapes[0],2,3))

    for i in range(shapes[0]):
        for j in range(shapes[1]):
            if j == 55200:
                for k in range(shapes[2]):
                    pos[i,0,k] = np.float(positions[i,j,k])
            if j == 55201:
                for k in range(shapes[2]):
                    pos[i,1,k] = np.float(positions[i,j,k])

    ## sort
    ri = np.zeros(shapes[0])
    rj = np.zeros(shapes[0])

    for i in range(shapes[0]):
        ri[i] = pos[i,0,0]
        rj[i] = pos[i,1,0]


    x = np.linspace(1,shapes[0], num = shapes[0])
    if plot is True:
        plt.plot(x,ri)
        plt.plot(x,rj)
        plt.show()
    return [ri,rj, energy]

### plot details
fs = 30
width = 3
ms = 14
fs_leg = 25
rij = np.linspace(0.1,5.0, num = 1000) # mesh for coulomb
###

## GPE
file_path = "./GPE-results/results-coulomb-NVE-sigma03/sim.H5"
file_path2 = "./GPE-results/results-coulomb-NVE-sigma05/sim.H5"
file_path3 = "./GPE-results/results-coulomb-NVE-sigma07/sim.H5"
ri,rj, energy = get(file_path)
ri2,rj2, energy2 = get(file_path2)
ri3,rj3, energy3 = get(file_path3)

## PE
file_p = "./PE-results/results-coulomb-NVE-PE-sigma03/sim.H5"
file_p2 = "./PE-results/results-coulomb-NVE-PE-sigma05/sim.H5"
file_p3 = "./PE-results/results-coulomb-NVE-PE-sigma07/sim.H5"
rii,rjj, en = get(file_p)
rii2,rjj2, en2 = get(file_p2)
rii3,rjj3, en3 = get(file_p3)
# touches at frame 64-1 = 63 (starting at 0)
L = "dotted"
l = "dashed"
s = "solid"

### mesh100
## GPE
file_path = "./mesh100/results-coulomb-NVE-sigma03/sim.H5"
file_path2 = "./mesh100/results-coulomb-NVE-sigma05/sim.H5"
file_path3 = "./mesh100/results-coulomb-NVE-sigma07/sim.H5"
ri,rj, energy = get(file_path)
ri2,rj2, energy2 = get(file_path2)
ri3,rj3, energy3 = get(file_path3)

## PE
file_p = "./mesh100/results-coulomb-NVE-PE-sigma03/sim.H5"
file_p2 = "./mesh100/results-coulomb-NVE-PE-sigma05/sim.H5"
file_p3 = "./mesh100/results-coulomb-NVE-PE-sigma07/sim.H5"
rii,rjj, en = get(file_p)
rii2,rjj2, en2 = get(file_p2)
rii3,rjj3, en3 = get(file_p3)
# touches at frame 64-1 = 63 (starting at 0)
L = "dotted"
l = "dashed"
s = "solid"
end2 = 63
W_c0 = W_coulomb(rij)[-1]
plt.figure(figsize = (10,8))
plt.plot(np.abs(ri[0:end2]-rj[0:end2]), energy[0:end2] - np.max(energy[0:end2]) + W_c0,linestyle = s ,marker = ".", markersize = ms, linewidth = width, label = r"GPE $\sigma = 0.3$")
plt.plot(np.abs(ri2[0:65]-rj2[0:65]), energy2[0:65] - np.max(energy2[0:65]) + W_c0,linestyle = s,marker= "|", markersize = ms, linewidth = width, label = r"GPE $\sigma = 0.5$")
plt.plot(np.abs(ri3[0:65]-rj3[0:65]), energy3[0:65] - np.max(energy3[0:65]) + W_c0,linestyle = s,marker = "*",markersize = ms, linewidth = width,  label = r"GPE $\sigma = 0.7$")

plt.plot(np.abs(rii[0:end2]-rjj[0:end2]), en[0:end2] - np.max(en[0:end2]) + W_c0,linestyle = l,marker =".",markersize = ms,  linewidth = width, label = r"PE $\sigma = 0.3$")
plt.plot(np.abs(rii2[0:65]-rjj2[0:65]), en2[0:65] - np.max(en2[0:65]) + W_c0 ,linestyle = l,marker= "|",markersize = ms, linewidth = width,  label = r"PE $\sigma = 0.5$")
plt.plot(np.abs(rii3[0:64]-rjj3[0:64]), en3[0:64] - np.max(en3[0:64]) + W_c0,linestyle = l,marker = "*",markersize = ms, linewidth = width,  label = r"PE $\sigma = 0.7$")
plt.plot(rij,W_coulomb(rij),"-", color = "black", label = "coulomb",linewidth = width)
plt.plot(rij,W_gaussian(rij),"--", color = "black", label = r"Gaussian, $\sigma = 0.5$",linewidth = width)
plt.xlabel(r"|$r_j - r_i$| [nm]",fontsize = fs)
plt.ylabel(r" W(r) [kJ mol$^{-1}$]",fontsize = fs)
plt.legend(fontsize = fs_leg)
plt.xticks(fontsize = fs)
plt.yticks(fontsize = fs)
plt.ylim([-250,-20])
plt.tight_layout()
plt.savefig("./figs/W100-v2.pdf", format = "pdf")
plt.show()

### mesh40
## GPE
#file_path = "./mesh40/results-coulomb-NVE-sigma03/sim.H5"
file_path2 = "./mesh40/results-coulomb-NVE-sigma05/sim.H5"
file_path3 = "./mesh40/results-coulomb-NVE-sigma07/sim.H5"
#ri,rj, energy = get(file_path)
ri2,rj2, energy2 = get(file_path2)
ri3,rj3, energy3 = get(file_path3)

## PE
file_p = "./mesh40/results-coulomb-NVE-PE-sigma03/sim.H5"
file_p2 = "./mesh40/results-coulomb-NVE-PE-sigma05/sim.H5"
file_p3 = "./mesh40/results-coulomb-NVE-PE-sigma07/sim.H5"
rii,rjj, en = get(file_p)#plot=  True)
rii2,rjj2, en2 = get(file_p2)
rii3,rjj3, en3 = get(file_p3)
# touches at frame 64-1 = 63 (starting at 0)
L = "dotted"
l = "dashed"
s = "solid"

end2 = 80
plt.figure(figsize = (10,8))
W_c0 = W_coulomb(rij)[-1]
#plt.plot(np.abs(ri[0:64]-rj[0:64]), energy[0:64],linestyle = s ,marker = ".", label = r"GPE $\sigma = 0.3$")
plt.plot(np.abs(ri2[0:64]-rj2[0:64]), energy2[0:64] - np.max(energy2) + W_c0,linestyle = s,marker= "|",markersize = ms, linewidth = width, label = r"GPE $\sigma = 0.5$")
plt.plot(np.abs(ri3[0:65]-rj3[0:65]), energy3[0:65] - np.max(energy3) + W_c0,linestyle = s,marker = "*",markersize = ms, linewidth = width, label = r"GPE $\sigma = 0.7$")

#plt.plot(np.abs(rii[0:end2]-rjj[0:end2]), en[0:end2],linestyle = l,marker =".",markersize = ms, linewidth = width, label = r"PE $\sigma = 0.3$")
plt.plot(np.abs(rii2[0:65]-rjj2[0:65]), en2[0:65] - np.max(en2) + W_c0,linestyle = l,marker= "|",markersize = ms,  linewidth = width,label = r"PE $\sigma = 0.5$")
plt.plot(np.abs(rii3[0:63]-rjj3[0:63]), en3[0:63] -np.max(en3) + W_c0,linestyle = l,marker = "*",markersize = ms, linewidth = width, label = r"PE $\sigma = 0.7$")
plt.plot(rij,W_coulomb(rij),"-", color = "black", label = "coulomb",linewidth = width)
plt.plot(rij,W_gaussian(rij),"--", color = "black", label = r"Gaussian, $\sigma = 0.5$",linewidth = width)
plt.xlabel(r"|$r_j - r_i$| [nm]",fontsize = fs)
plt.ylabel(r" W(r) [kJ mol$^{-1}$]",fontsize = fs)
plt.legend(fontsize = fs_leg)
plt.xticks(fontsize = fs)
plt.yticks(fontsize = fs)
plt.ylim([-165,-25])
plt.tight_layout()
plt.savefig("./figs/W40-v2.pdf", format = "pdf")
plt.show()

print(np.abs(ri2[63]-rj2[63]))
