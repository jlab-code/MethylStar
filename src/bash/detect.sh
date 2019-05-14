#!/bin/bash
curr_dir="$(dirname "$0")"
# Optimizing cores for parallelization 

npar=$(cat /proc/cpuinfo | awk '/^processor/{print $3}' | wc -l)
#mem=$(($(getconf _PHYS_PAGES) * $(getconf PAGE_SIZE) / (1024 * 1024 * 1024 )))

if [ "$1" = "trimm" ]; 
then
	n_th=6
	if [ $npar -gt 88 ]; then npar=18; n_th=16;
		elif [ $npar -gt 64 -a $npar -le 88 ]; then npar=16 && n_th=16;
		elif [ $npar -gt 32 -a $npar -le 64 ]; then npar=8 && n_th=16;
		elif [ $npar -gt 16 -a $npar -le 32 ]; then npar=4 && n_th=16;
		elif [ $npar -gt 2 -a $npar -le 16 ]; then  npar=2; 
	fi
	sed -i "s/n_th=.*/n_th=$n_th/g" $curr_dir/tmp.conf
	sed -i "s/npar=.*/npar=$npar/g" $curr_dir/tmp.conf
fi
#---------------------
# Bismark mapper 
#---------------------
if [ "$1" = "bismap" ]; 
then
	bis_parallel=8
	if [ $npar -gt 88 ]; then npar=5; bis_parallel=16;
		elif [ $npar -gt 64 -a $npar -le 88 ]; then npar=4 && bis_parallel=16;
		elif [ $npar -gt 32 -a $npar -le 64 ]; then npar=3 && bis_parallel=16;
		elif [ $npar -gt 16 -a $npar -le 32 ]; then npar=2 && bis_parallel=16;
		elif [ $npar -gt 2 -a $npar -le 16 ]; then  npar=1 && sed -i "s/parallel_mode=.*/parallel_mode=false/g" config/pipeline.conf;
	fi
	sed -i "s/bis_parallel=.*/bis_parallel=$bis_parallel/g" $curr_dir/tmp.conf
	sed -i "s/npar=.*/npar=$npar/g" $curr_dir/tmp.conf
fi

if [ "$1" = "bismeth" ]; 
then
	bis_parallel=6
	if [ $npar -gt 88 ]; then npar=5; bis_parallel=16;
		elif [ $npar -gt 64 -a $npar -le 88 ]; then npar=4 && bis_parallel=16;
		elif [ $npar -gt 32 -a $npar -le 64 ]; then npar=3 && bis_parallel=16;
		elif [ $npar -gt 16 -a $npar -le 32 ]; then npar=2 && bis_parallel=16;
		elif [ $npar -gt 2 -a $npar -le 16 ]; then  npar=1 && sed -i "s/parallel_mode=.*/parallel_mode=false/g" config/pipeline.conf ; 
	fi
	sed -i "s/bis_parallel=.*/bis_parallel=$bis_parallel/g" $curr_dir/tmp.conf
	sed -i "s/npar=.*/npar=$npar/g" $curr_dir/tmp.conf
fi
#-----------------------
# Sorting deduplicate
#-----------------------
if [ "$1" = "sort" ]; 
then
	npar=4
	if [ $npar -gt 88 ]; then npar=32; 
		elif [ $npar -gt 64 -a $npar -le 88 ]; then npar=20; 
		elif [ $npar -gt 32 -a $npar -le 64 ]; then npar=15;
		elif [ $npar -gt 16 -a $npar -le 32 ]; then npar=8; 
		elif [ $npar -gt 2 -a $npar -le 16 ]; then  npar=4; 
	fi
	sed -i "s/npar=.*/npar=$npar/g" $curr_dir/tmp.conf
fi