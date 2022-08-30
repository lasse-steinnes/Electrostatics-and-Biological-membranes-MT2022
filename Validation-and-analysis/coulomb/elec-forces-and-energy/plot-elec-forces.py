"""
Obtain electrostatic forces
"""
import h5py
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cbook
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes, mark_inset
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar


def get(file_path, plot = False):
    f = h5py.File(file_path,"r")
    positions = f["/particles/all/position/value"]

    last_frame = int(101)
    pico_to_nano = 1e-3

    positions = np.array(positions)
    shapes = np.shape(positions)

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
    return [ri,rj]


def get_f(path):
    fe = []
    dp = np.zeros(101)
    dp[0] = 11
    for i in range(0,100):
        dp[i+1] = 11 + dp[i]

    with open(path) as f:
            line = f.readline()# superfluous
            line = f.readline() #start

            sep = line.split(",")
            fe.append(sep[1]) # initial
            i = 1
            while i < 1000:
                line = f.readline()
                if not line:
                    break
                if i in dp:
                    sep = line.split(",")
                    fe.append(float(sep[1]))
                #print(line)
                #print(line.strip())
                i = i + 1
    f.close()
    fe = np.array(fe).astype(np.float)
    return fe

####
fs = 30
width = 3
ms = 14
fs_leg = 25

L = "dotted"
l = "dashed"
s = "solid"
####

### MESH size 100 in x dir
## GPE
file_path = "./mesh100/results-coulomb-NVE-sigma03/sim.H5"
file_path2 = "./mesh100/results-coulomb-NVE-sigma05/sim.H5"
file_path3 = "./mesh100/results-coulomb-NVE-sigma07/sim.H5"
ri,rj = get(file_path)
ri2,rj2 = get(file_path2)
ri3,rj3 = get(file_path3)


p1 = './elec-txts-mesh100/elec_forcesPIC_Spectral_GPE0.30.txt'
p2 = './elec-txts-mesh100/elec_forcesPIC_Spectral_GPE0.50.txt'
p3 = './elec-txts-mesh100/elec_forcesPIC_Spectral_GPE0.70.txt'

f1 = get_f(p1)
f2 = get_f(p2)
f3 = get_f(p3)

## PE
file_p = "./mesh100/results-coulomb-NVE-PE-sigma03/sim.H5"
file_p2 = "./mesh100/results-coulomb-NVE-PE-sigma05/sim.H5"
file_p3 = "./mesh100/results-coulomb-NVE-PE-sigma07/sim.H5"
rii,rjj = get(file_p)# plot = True)
rii2,rjj2 = get(file_p2)
rii3,rjj3 = get(file_p3)

pp1 = './elec-txts-mesh100/elec_forcesPIC_Spectral0.30.txt'
pp2 = './elec-txts-mesh100/elec_forcesPIC_Spectral0.50.txt'
pp3 = './elec-txts-mesh100/elec_forcesPIC_Spectral0.70.txt'

ff1 = get_f(pp1)
ff2 = get_f(pp2)
ff3 = get_f(pp3)

# touches at frame 64-1 = 63 (starting at 0)
# Plot forces  from electrostatic coulomb  as a function of different sigmas #
# Coulomb F
k_electric = 138.935458 # 1/(eps0*4pi)
charge_i = -1.0
charge_j = 1.0
rij = np.linspace(0.5,5.0, num = 1000)
F = k_electric * charge_i * charge_j/(rij)**2

end = 64
end2 = 64
end3 = -1
######## Plot F(r) ##########
plt.figure(figsize = (10,8))
plt.plot(np.abs(ri[0:end]-rj[0:end]), f1[0:end],linestyle = s ,marker = ".",markersize = ms,linewidth = width, label = r"GPE $\sigma = 0.3$")
plt.plot(np.abs(ri2[0:end]-rj2[0:end]), f2[0:end],linestyle = s,marker= "|",markersize = ms,linewidth = width, label = r"GPE $\sigma = 0.5$")
plt.plot(np.abs(ri3[0:end]-rj3[0:end]), f3[0:end],linestyle = s,marker = "*",markersize = ms,linewidth = width, label = r"GPE $\sigma = 0.7$")
linewidth = width,
plt.plot(np.abs(rii[0:end2]-rjj[0:end2]), ff1[0:end2],linestyle = l,marker =".",linewidth = width, label = r"PE $\sigma = 0.3$")
plt.plot(np.abs(rii2[0:end]-rjj2[0:end]), ff2[0:end],linestyle = l,marker= "|",markersize = ms,linewidth = width, label = r"PE $\sigma = 0.5$")
plt.plot(np.abs(rii3[0:end]-rjj3[0:end]), ff3[0:end],linestyle = l,marker = "*",markersize = ms,linewidth = width, label = r"PE $\sigma = 0.7$")
plt.plot(rij,F,"-", color = "black", label = "coulomb",linewidth = width)
plt.legend()
plt.xlim([0.5,5.2])
#plt.xlim([0.01,5.2])
plt.ylim([-275,0])
plt.xlabel(r"|$r_j - r_i$| [nm]", fontsize = fs)
plt.ylabel(r" F(r) [kJ mol$^{-1}$ nm$^{-1}$]", fontsize = fs)
plt.legend(fontsize = fs_leg)
plt.xticks(fontsize = fs)
plt.yticks(fontsize = fs)
plt.tight_layout()
plt.savefig("./figs/F100.pdf", format = "pdf")
plt.show()


### MESH size 40 in x dir
## GPE
#file_path = "./mesh40/results-coulomb-NVE-sigma03/sim.H5"
file_path2 = "./mesh40/results-coulomb-NVE-sigma05/sim.H5"
file_path3 = "./mesh40/results-coulomb-NVE-sigma07/sim.H5"
ri,rj = get(file_path)
ri2,rj2 = get(file_path2)
ri3,rj3 = get(file_path3)


#p1 = './elec-txts-mesh100/elec_forcesPIC_Spectral_GPE0.30.txt'
p2 = './elec-txt-m40/elec_forcesPIC_Spectral_GPE0.50.txt'
p3 = './elec-txt-m40/elec_forcesPIC_Spectral_GPE0.70.txt'

#f1 = get_f(p1)
f2 = get_f(p2)
f3 = get_f(p3)

## PE
file_p = "./mesh100/results-coulomb-NVE-PE-sigma03/sim.H5"
file_p2 = "./mesh100/results-coulomb-NVE-PE-sigma05/sim.H5"
file_p3 = "./mesh100/results-coulomb-NVE-PE-sigma07/sim.H5"
rii,rjj = get(file_p)# plot = True)
rii2,rjj2 = get(file_p2)
rii3,rjj3 = get(file_p3)

pp1 = './elec-txt-m40/elec_forcesPIC_Spectral0.30.txt'
pp2 = './elec-txt-m40/elec_forcesPIC_Spectral0.50.txt'
pp3 = './elec-txt-m40/elec_forcesPIC_Spectral0.70.txt'

ff1 = get_f(pp1)
ff2 = get_f(pp2)
ff3 = get_f(pp3)

# Plot forces  from electrostatic coulomb  as a function of different sigmas #
# Coulomb F
k_electric = 138.935458 # 1/(eps0*4pi)
charge_i = -1.0
charge_j = 1.0
rij = np.linspace(0.1,5.0, num = 1000)
F = k_electric * charge_i * charge_j/(rij)**2

end = 64
end2 = 81
end3 = -1
######## Plot F(r) ##########
plt.figure(figsize = (10,8))
plt.plot(np.abs(ri2[0:end]-rj2[0:end]), f2[0:end],linestyle = s,marker= "|", markersize = ms,linewidth = width, label = r"GPE $\sigma = 0.5$")
plt.plot(np.abs(ri3[0:end]-rj3[0:end]), f3[0:end],linestyle = s,marker = "*",markersize = ms,linewidth = width, label = r"GPE $\sigma = 0.7$")
plt.plot(np.abs(rii2[0:end]-rjj2[0:end]), ff2[0:end],linestyle = l,marker= "|",markersize = ms,linewidth = width, label = r"PE $\sigma = 0.5$")
plt.plot(np.abs(rii3[0:end]-rjj3[0:end]), ff3[0:end],linestyle = l,marker = "*",markersize = ms,linewidth = width, label = r"PE $\sigma = 0.7$")
plt.plot(rij,F,"-", color = "black", label = "coulomb",linewidth = width)
plt.xlim([0.5,5.2])
#plt.xlim([0.01,5.2])
plt.ylim([-100,0])
plt.xlabel(r"|$r_j - r_i$| [nm]",fontsize = fs)
plt.ylabel(r" F(r) [kJ mol$^{-1}$ nm$^{-1}$]",fontsize = fs)
plt.legend(fontsize = fs_leg)
plt.xticks(fontsize = fs)
plt.yticks(fontsize = fs)
plt.tight_layout()
plt.savefig("./figs/F40.pdf", format = "pdf")
plt.show()
