#!/bin/bash
#SBATCH --output=matheus1.slurm
#SBATCH --job-name=matheus1

echo Iniciando...
source /home/matheus/.prep-g09.sh

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

while [ $i -le 33 ]; do
    echo Rodando a entrada $i no Gaussian 09...
    g09 /home/matheus/.tcc/Inputs/Inputs-$1/H2O2-Kr_$i.com /home/matheus/.tcc/Logs/Logs-$1/H2O2-Kr_$i.log &
    pid=$!
    # If this script is killed, kill the `g09'.
    trap "kill $pid 2> /dev/null" EXIT
    
    sleep 1
    # While g16 is running...
    while kill -0 $pid 2> /dev/null; do
        tail -f --pid=$pid /home/matheus/.tcc/Logs/Logs-$1/H2O2-Kr_$i.log
        sleep 1
    done

    #formchk -3 /home/matheus/.tcc/chk/H2O2-Kr_$i.chk /home/matheus/.tcc/chk/H2O2-Kr_$i.fchk
    echo Pronto!
    i=$(( i+17 ))
    sleep 10
done

# for i in $( ls *.log ); do
#      mv $i ./logs/
#      echo Pronto!
# done
