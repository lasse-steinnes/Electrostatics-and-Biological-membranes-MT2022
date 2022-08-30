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
From Samiran feb 2022 example:
This README starts from scratch and prepared input for HyMD
We want to build a system of lipid A molecules with CA^2+ counter ions in water.
We use the same number of lipid molecules as found in folder `therezafiles` (i have it somewhere locally or inbox:thereza's email) but we are building a CG system.
In Martini mapping, number of water molecules is scaled down by 4. We use an excess of water molecules to ensure vesicular assembly.
` \# LA: 644
  \# CA: 644
  \# W:  210912
`
We use Avogadro to draw a single Lipid A in its CG representation and save it as `lipid\_A.pdb'
`gmx insert-molecules -nmol 644 -ci lipid\_A.pdb -box 30 30 30 -o lipidonly.gro`
`gmx insert-molecules -nmol 210912 -ci W.pdb -f lipidonly.gro  -o lipidW.gro`
`gmx insert-molecules -nmol 644 -ci CA.pdb -f lipidW.gro  -o lipidWCA.gro`

We construct `sys.top` and the `.itp` files inside it. Note that bonds had to be manually entered using reference `lipid_A.pdb`   
We need these to create the input `.h5` for HyMD.  
Look inside: `gmx\_to\_hymd.py` and ensure the following is set.  
```python
atomtype_id     = np.array([  1,    2,     3,     4,    5,    6  ])
atomtype_name   = np.array([ 'P',  'G',   'L',   'C',   'W',  'CA'])
atomtype_mass   = np.array([72.0,  72.0,  72.0,  72.0,  72.0,  72.0] )
atomtype_charge = np.array([-1.0,  0.0,   0.0,   0.0,  0.0,   +2.0 ] )
```
Now we have everything to generate the input `lipidA.h5` (name of file has to be set inside the code)  
`python3 gmx\_to\_hymd.py lipidWCA.gro sys.top`  

Check what was made:
`h5glance lipidA.h5`
```bash
lipidA.h5 (2 attributes)
âbonds	[int32: 229588 Ã 4]
âcharge	[float32: 229588]
âcoordinates	[float64: 1 Ã 229588 Ã 3]
âindices	[int32: 229588]
âmolecules	[int32: 229588]
ânames	[5-byte ASCII string: 229588]
âtypes	[int32: 229588]
âvelocities	[float64: 1 Ã 229588 Ã 3]ce lipidA.h5`
```
