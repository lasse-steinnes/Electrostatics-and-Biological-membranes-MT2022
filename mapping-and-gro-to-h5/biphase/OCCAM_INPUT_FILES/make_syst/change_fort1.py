import sys

#Charge
lines=open('fort.1').readlines()
line = open( "fort.5").readlines()[-1]
N=int(line.split()[0])
lines[3]="%d"%(N)

fp=open('fort.1','w')
for i in range(len(lines)):
    fp.write('%s\n'%(' '.join(lines[i].split())))


fp.close()
