"""
Making a 10.1 by 10.1 by 10.0 nm^3 system
by reading and writing a gro file,
counting number of molecules for input to h5

PS: After writing new gro file by calling change_sim_box.py,
change number of beads in new gro manually.

Then call gmx_2_hymd.py for conversion to h5.
"""

# reading off the gro file,
# and writing wanted lines

infile = open("./frame90ns.gro", "r")
outfile = open("./frame90ns_new.gro", 'w')

x_lim = 10.000; y_lim = 10.000; z_lim = 9.39310

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
    max_lower = 62

    # counting ions to ensure symmetry
    ion_lower = 0.0
    ion_upper = 0.0
    max_ion_u = max_lower

    i = 2
    while  2 <= i < len(lines) - 1:
        name = lines[i][5:8]
        #print(name)

        if name == 'LA6':
            flag = False
            for j in range(molsize):
                x = lines[i+j][22:28]
                y = lines[i+j][30:36]
                z = lines[i+j][38:44]

                if float(x) > x_lim or  float(y) > y_lim or float(z) > z_lim:
                    flag = True

            if flag is False:
                bead_type = lines[i + 2][13:15]# to ensure symmetry
                z = lines[i+2][38:44]
                #print(bead_type)
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

            if float(x) > x_lim or  float(y) > y_lim or float(z) > z_lim:
                flag = True

            if flag is False:
                if name == 'N  ':
                    if float(z) > sep_nm and ion_upper <= max_ion_u - 1:
                        ion_upper = ion_upper + 1

                    else:
                        if ion_lower <= ion_upper - 1:
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
                    outfile.write(lines[i])

            else:
                if name == 'N  ':
                    o_CA = o_CA + 1

                elif name == 'SOL':
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
sum_rem = o_LA + o_W + o_CA
tot = numLA + numCA + numW - sum_rem


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
print("NOTE: Can change manually number of CA to match number of LA's")
