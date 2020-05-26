#!/bin/bash
#SBATCH --output=matheus1.slurm
#SBATCH --job-name=matheus1

echo Iniciando...

# g09root=/usr/local/g09
# GAUSS_SCRDIR=/mnt/driveB/scratch/matheus
# export g09root GAUSS_SCRDIR
# . $g09root/g09/bsd/g09.profile

# for i in $( ls *.com ); do
#      echo Rodando o $i no Gaussian 09
#      g09 $i
#      formchk -3 $i.chk
#      echo Pronto!
# done

i=0

while [ $i -le 0 ]; do
    echo Rodando a entrada $i no Gaussian 09
    g09 /home/matheus/.tcc/Inputs-wb97xd/H2O2-Kr_$i.com /home/matheus/.tcc/Logs-wb97xd/H2O2-Kr_$i.log
    # formchk -3 /home/matheus/.tcc/chk/H2O2-Kr_$i.chk
    echo Pronto!
    i=$(( i+1 ))
done

sleep 10

# for i in $( ls *.log ); do
#      mv $i ./logs/
#      echo Pronto!
# done
