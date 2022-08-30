# Box size
Lx="13"
Ly="13"
Lz="26"

#Salt concentration, note that counter ions are also added! 

c[2]='5'
c[3]='2.5'
c[4]='1'
c[5]='0.5'
c[6]='0.25'
c[7]='0.1'
c[8]='0.05'
c[9]='0.025'
c[10]='0.01'
c[11]='0'
#Loop for system
for ci in "${c[@]}"
do 
    python insane_mod.py -x $Lx -y $Ly -z $Lz -l POPG -o POPG.gro -sol WATER  -p topo.top -salt $ci -a 0.69
    python convert_gro_fort5.py POPG.gro con.occ
    rm -r C$ci
    mkdir C$ci
    cp -r Start_files/* C$ci/
    cp fort.5 C$ci
    cd C$ci
    python ../change_fort1.py
    sbatch Jobscript.sh
    cd ..
done


