import numpy as np
import sys
import string
from string import digits
#Gro-file
fp1=open(sys.argv[1], 'r')
lines=fp1.readlines()
N_atoms = int(lines[1])


x=lines[-3].split()[0]
all=string.maketrans('','')
nodigs=all.translate(all, string.digits)
x=x.translate(all, nodigs)
N_mols  = int(x)

L=[float(j) for j in lines[-2].split()[:3]]


#Connectivity file
fp2=open(sys.argv[2], 'r')
lines2=fp2.readlines()

n_mol_type=0
mol=[]
mols=[]
names=[]
nmol=0
a=False
for i in range(len(lines2)):
    
    l=lines2[i].split()
    if (a and len(l)==1):
        mols.append(mol)
        mol=[]
        names.append(l[0])
    elif(len(l)==1): 
        names.append(l[0])

    else:
        mol.append(lines2[i].split())
    a=True
mols.append(mol)


#fort.5
fp3=open('fort.5','w')
fp3.write('box:\n')
fp3.write('%f %f %f 0\n'%(L[0],L[1],L[2]))
fp3.write('Total number of molecules:\n')
fp3.write('%d\n'%(N_mols))

n_atom=1
for nmol in range(N_mols):
    x=lines[n_atom+1][:].split()[0]
    all=string.maketrans('','')
    mol_name=x.translate(None, digits)

    index=names.index(mol_name)

    fp3.write('Molecule number %d\n'%(nmol+1))
    fp3.write('%d\n'%(len(mols[index])))
    temp_natom=n_atom-1
    for mol in mols[index]:
        line=lines[n_atom+1]
        l=line.split()
        bonds=""
        for b in mol[2:8]:
            bonds=bonds+ "%d " % (int(b)+temp_natom*(int(b)>0))
        #        fp3.write('%d %s %s %s %s %s %s %s %s %s %s %s %s\n'% (n_atom,mol[-2],mol[1],mol[-1],l[-3],l[-2],l[-1],mol[2],mol[3],mol[4],mol[5],mol[6],mol[7]))
        fp3.write('%d %s %s %s %s %s %s %s\n'% (n_atom,mol[-2],mol[1],mol[-1],l[-3],l[-2],l[-1],bonds))
        n_atom=n_atom+1

    

