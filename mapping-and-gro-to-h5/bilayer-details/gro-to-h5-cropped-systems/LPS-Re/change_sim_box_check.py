"""
Making a 10 by 10 by 9.3 nm^3 system
by reading and writing a gro file,
counting number of molecules for input to h5

PS: After writing new gro file by calling change_sim_box.py,
change number of beads in new gro manually.

Then call gmx_2_hymd.py for conversion to h5.
"""

# reading off the gro file,
# and writing wanted lines

infile = open("./frame90ns_new.gro", "r")
outfile = open("./frame90ns_new_new.gro", 'w')

x_lim = 10.000; y_lim = 10.000; z_lim = 10.000

if infile.mode == "r":
    ### frame info
    lines = infile.readlines()
    outfile.write(lines[0])
    outfile.write(lines[1])

    molsize = 33
    # omission counting:
    o_Lre = 0
    o_CA = 0
    o_W = 0

    i = 2
    count = 0
    while  2 <= i < len(lines) - 1:
        name = lines[i][5:8]
        #print(name)

        if name == 'LRe':
            flag = False
            for j in range(molsize):
                x = lines[i+j][22:28]
                y = lines[i+j][30:36]
                z = lines[i+j][38:44]

                if float(x) > x_lim or  float(y) > y_lim or float(z) > z_lim:
                    flag = True


            if flag is False:
                for j in range(molsize):
                    outfile.write(lines[i + j])
            else:
                o_Lre = o_Lre + 1

            i = i + j + 1

        else:
            x = lines[i][22:28]
            y = lines[i][30:36]
            z = lines[i][38:44]
            flag = False

            if float(x) > x_lim or  float(y) > y_lim or float(z) > z_lim:
                flag = True

            if flag is False:
                outfile.write(lines[i])
                if name == 'N  ':
                    count = count  + 1

            else:

                # PS be aware of whitespace
                # due to number of letters being 2 instead of 3
                if name == 'N  ':
                    o_CA = o_CA + 1

                elif name == 'SOL':
                    o_W = o_W + 1

            i = i + 1

    ### write in new dimensions of box
    outfile.write(" 10.00000  10.00000   10.000")

infile.close()
outfile.close()

## overview: change number of particles in box
numLA =  109
numCA =  218
numW  =  5604
sum_rem = o_Lre + o_W + o_CA
tot = numLA + numCA + numW - sum_rem

print("number of ions", count)

print("-------------------------------------------------------------------------------")
print("      Successfully reduced box-size to dimension", x_lim, " x " ,  y_lim, " x " ,  z_lim, "nm^3")
print("-------------------------------------------------------------------------------")

print("Removed particles:")
print("Lre", o_Lre, "W", o_W, "CA",  o_CA)
print("Remaining particles:")

print("Lre", numLA - o_Lre, "W", numW - o_W, "CA", numCA - o_CA)
print("total number of particles left in box: ", tot)
print("Number of CG beads:", molsize*(numLA - o_Lre) + numW - o_W + numCA - o_CA)
print("^ change manually in gro")
print("NOTE: Can change manually number of CA to match number of LA's")
