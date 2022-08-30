# Lipid A start frame
* Created Feb 2022 -  LS
* Converting the starting frame of Lipid-A simulation from gro to h5

Note: The lipid-A hexa is set up after the first molecule in gro. Do in terminal
"more frame90ns.gro". Must match for correct gro to h5.

28 beads, 29 bonds

atomname and residuename must correspond

PS PS: top and names of beads must be in order they appear in gro file.

NOTE: It seems that the topologyparser doesn't read the last line (spacing issue?). Thus added
a random one --> now all beads in lipid A connected, as of feb 2022.

----------------------------------------------------
