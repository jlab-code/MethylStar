#!/bin/bash

# Optimizing cores for parallelization 

npar=$(cat /proc/cpuinfo | awk '/^processor/{print $3}' | wc -l)

if [ "$1" = "trimm" ]; 
then
	n_th=6
	if [ $npar -gt 88 ]; then npar=18; n_th=16;
		elif [ $npar -gt 64 -a $npar -le 88 ]; then npar=16; n_th=16;
		elif [ $npar -gt 32 -a $npar -le 64 ]; then npar=8; n_th=16;
		elif [ $npar -gt 16 -a $npar -le 32 ]; then npar=4; n_th=16;
		elif [ $npar -gt 2 -a $npar -le 16 ]; then  npar=2; 
	fi
	sed -i "s/n_th=.*/n_th=$n_th/g" $curr_dir/tmp.conf
	sed -i "s/npar=.*/npar=$npar/g" $curr_dir/tmp.conf
fi