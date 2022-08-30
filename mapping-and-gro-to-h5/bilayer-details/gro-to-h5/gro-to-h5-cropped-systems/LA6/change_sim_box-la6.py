"""
Making a 10.1 by 10.1 by 10.0 nm^3 system
by reading and writing a gro file,
counting number of molecules for input to h5

PS: After writing new gro file by calling change_sim_box.py,
change number of beads in new gro manually.

Then call gmx_2_hymd.py for conversion to h5.
"""
import numpy as np

# reading off the gro file,
# and writing wanted lines

infile = open("./frame90ns.gro", "r")
outfile = open("./frame90ns_new.gro", 'w')

x_lim = 10.000; y_lim = 10.000; z_lim = 9.39310
x_lim_ions = 11.000;  y_lim_ions = 11.000;
x_old = 14.29660; y_old = 13.19990 ; z_old =  9.39310

if infile.mode == "r":
    ### frame info
    lines = infile.readlines()
    outfile.write(lines[0])
    outfile.write(lines[1])

    molsize = 28

    # omission counting:
    o_LA = 0
    o_CA = 0
    o_W = 0

    # upper and lower counting to ensure symmetry
    sep_nm = 5.0
    upper_count = 0.0
    lower_count = 0.0
    max_lower = 68

    max_water = 5062
    # ^ to get correct number densities. Set high if you don't want to limit this
    water_count = 0.0

    # counting ions to ensure symmetry
    ion_lower = 0.0
    ion_upper = 0.0
    max_ion_u = max_lower

    i = 2
    while  2 <= i < len(lines) - 1:
        name = lines[i][5:8]
        #print(name)
        # center of mass coordinates
        r_com = np.zeros(3)

        if name == 'LA6':
            flag = False
            for j in range(molsize):
                x = lines[i+j][22:28]
                y = lines[i+j][30:36]
                z = lines[i+j][38:44]

                r_com = r_com + np.array([float(x),float(y),float(z)])

            r_com = (1.0/molsize)*r_com # assume beads have equal mass

            if r_com[0] > x_lim or  r_com[1] > y_lim or r_com[2] > z_lim:
                flag = True

            if flag is False:
                bead_type = lines[i + 2][13:15]# to ensure symmetry
                z = lines[i+2][38:44]

                if bead_type == 'L1': # specific for lipid A
                    if float(z) < sep_nm and lower_count <= max_lower - 1:
                            lower_count = lower_count + 1

                    else:
                        if upper_count <= lower_count - 1:
                            upper_count = upper_count + 1
                        else:
                            flag = True #ommit
                            o_LA = o_LA + 1

                if flag is False: # last check
                    for j in range(molsize):
                        outfile.write(lines[i + j])

            else:
                o_LA = o_LA + 1

            i = i + j + 1

        else:
            x = lines[i][22:28]
            y = lines[i][30:36]
            z = lines[i][38:44]
            flag = False

            if name == 'N  ':

                if float(x) > x_lim_ions or  float(y) > y_lim_ions or float(z) > z_lim:
                    flag = True

                if flag == False:
                    if float(z) > sep_nm  and ion_upper <= max_ion_u - 1:
                        ion_upper = ion_upper + 1
                    else:
                        if ion_lower <= max_ion_u - 1:
                            ion_lower = ion_lower + 1
                        else:
                            flag = True

                    if flag is False:
                        outfile.write(lines[i])
                    else:
                        # PS be aware of whitespace
                        # due to number of letters being 2 instead of 3
                        o_CA = o_CA + 1
                else:
                    if name == 'N  ':
                        o_CA = o_CA + 1

            if name == "SOL":

                if float(x) > x_lim or  float(y) > y_lim or float(z) > z_lim:
                    flag = True

                if flag == False and water_count < max_water:
                    outfile.write(lines[i])
                    water_count = water_count + 1
                else:
                    o_W = o_W + 1

            i = i + 1

    ### write in new dimensions of box
    outfile.write(" 10.00000  10.00000   9.39310")

infile.close()
outfile.close()

## overview: change number of particles in box
numLA =  256
numCA =  256
numW  =  9556
num_old = numLA + numCA + numW
sum_rem = o_LA + o_W + o_CA
tot = numLA + numCA + numW - sum_rem
V_old =(x_old*y_old*z_old)
V_new = (x_lim*y_lim*z_lim)
A_old =(x_old*y_old)
A_new = (x_lim*y_lim)

print("-------------------------------------------------------------------------------")
print("      Successfully reduced box-size to dimension", x_lim, " x " ,  y_lim, " x " ,  z_lim, "nm^3")
print("-------------------------------------------------------------------------------")

print("Removed particles:")
print("LA", o_LA, "W", o_W, "CA",  o_CA)
print("Remaining particles:")

print("LA", numLA - o_LA, "W", numW - o_W, "CA", numCA - o_CA)
print("lower and upper lipids:", lower_count, upper_count)
print("lower and upper ions", ion_lower, ion_upper)
print("total number of particles left in box: ", tot)
print("Number of CG beads:", molsize*(numLA - o_LA) + numW - o_W + numCA - o_CA)
print("^ change manually in gro")
print("\n")
print("Old area per lipid: ", A_old/float(numLA), " new: ", A_new/float(numLA - o_LA))
print("Old density of water: ", float(numW)/V_old, " new: ", float(numW-o_W)/V_new)
print("Old density of ions: ", float(numCA)/V_old, " new: ", float(numCA - o_CA)/V_new)
print("Old density of lipids: ", float(numLA)/V_old, " new: ", float(numLA-o_LA)/V_new)
print("Old particle number density", num_old/V_old , " new: ", tot/V_new)
