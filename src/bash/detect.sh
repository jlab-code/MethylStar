#!/bin/bash
curr_dir="$(dirname "$0")"
# Optimizing cores for parallelization 

npar=$(cat /proc/cpuinfo | awk '/^processor/{print $3}' | wc -l)
#mem=$(($(getconf _PHYS_PAGES) * $(getconf PAGE_SIZE) / (1024 * 1024 * 1024 )))

if [ "$3" = "0" ];
then

                if [ "$1" = "Arabidopsis" ]; 
                then

                                        if [ "$2" = "trimm" ]; 
                                        then
                                                n_th=6
                                                if [ $npar -gt 88 ]; then npar=18  && n_th=16;
                                                        elif [ $npar -gt 64 -a $npar -le 88 ]; then npar=12 && n_th=16;
                                                        elif [ $npar -gt 32 -a $npar -le 64 ]; then npar=8 && n_th=16;
                                                        elif [ $npar -gt 16 -a $npar -le 32 ]; then npar=4 && n_th=16;
                                                        elif [ $npar -gt 4 -a $npar -le 16 ]; then  npar=2;
                                                fi
                                                sed -i "s/n_th=.*/n_th=$n_th/g" $curr_dir/tmp.conf
                                                sed -i "s/npar=.*/npar=$npar/g" $curr_dir/tmp.conf
                                        fi
                                        #---------------------
                                        # Bismark mapper 
                                        #---------------------
                                        if [ "$2" = "bismap" ]; 
                                        then
                                                Nthreads=2
                                                bis_parallel=8
                                                if [ $npar -gt 88 ]; then npar=5 && bis_parallel=8 && Nthreads=5 ;
                                                        elif [ $npar -gt 64 -a $npar -le 88 ]; then npar=4 && bis_parallel=8 && Nthreads=4 ;
                                                        elif [ $npar -gt 32 -a $npar -le 64 ]; then npar=3 && bis_parallel=6 && Nthreads=3 ;
                                                        elif [ $npar -gt 16 -a $npar -le 32 ]; then npar=2 && bis_parallel=4 && Nthreads=2 ;
                                                        elif [ $npar -gt 4 -a $npar -le 16 ]; then  npar=1 && bis_parallel=2 ;
                                                fi
                                                sed -i "s/bis_parallel=.*/bis_parallel=$bis_parallel/g" $curr_dir/tmp.conf
                                                sed -i "s/npar=.*/npar=$npar/g" $curr_dir/tmp.conf
                                                sed -i "s/Nthreads=.*/Nthreads=$Nthreads/g" $curr_dir/tmp.conf
                                        fi

                                        if [ "$2" = "bismeth" ]; 
                                        then
                                                bis_parallel=6
                                                if [ $npar -gt 88 ]; then npar=5  && bis_parallel=8;
                                                        elif [ $npar -gt 64 -a $npar -le 88 ]; then npar=4 && bis_parallel=8;
                                                        elif [ $npar -gt 32 -a $npar -le 64 ]; then npar=3 && bis_parallel=6;
                                                        elif [ $npar -gt 16 -a $npar -le 32 ]; then npar=2 && bis_parallel=4;
                                                        elif [ $npar -gt 4 -a $npar -le 16 ]; then  npar=1 && sed -i "s/parallel_mode=.*/parallel_mode=false/g" config/pipeline.conf ;
                                                fi
                                                sed -i "s/bis_parallel=.*/bis_parallel=$bis_parallel/g" $curr_dir/tmp.conf
                                                sed -i "s/npar=.*/npar=$npar/g" $curr_dir/tmp.conf
                                        fi


                elif [ "$1" = "Maize" ];
                then 

                                        if [ "$2" = "trimm" ]; 
                                        then
                                                n_th=1
                                                if [ $npar -gt 88 ]; then npar=5 && n_th=5;
                                                        elif [ $npar -gt 64 -a $npar -le 88 ]; then npar=5 && n_th=4;
                                                        elif [ $npar -gt 32 -a $npar -le 64 ]; then npar=3 && n_th=4;
                                                        elif [ $npar -gt 16 -a $npar -le 32 ]; then npar=2 && n_th=4;
                                                        elif [ $npar -gt 4 -a $npar -le 16 ]; then  npar=1;
                                                fi
                                                sed -i "s/n_th=.*/n_th=$n_th/g" $curr_dir/tmp.conf
                                                sed -i "s/npar=.*/npar=$npar/g" $curr_dir/tmp.conf
                                        fi
                                        #---------------------
                                        # Bismark mapper 
                                        #---------------------
                                        if [ "$2" = "bismap" ]; 
                                        then
                                                Nthreads=2
                                                bis_parallel=2
                                                if [ $npar -gt 88 ]; then npar=3 && bis_parallel=8 && Nthreads=5;
                                                        elif [ $npar -gt 64 -a $npar -le 88 ]; then npar=2 && bis_parallel=6 && Nthreads=4;
                                                        elif [ $npar -gt 32 -a $npar -le 64 ]; then npar=1 && bis_parallel=4 && Nthreads=3;
                                                        elif [ $npar -gt 16 -a $npar -le 32 ]; then npar=1 && bis_parallel=3 && Nthreads=2;
                                                        elif [ $npar -gt 4 -a $npar -le 16 ]; then  npar=1 && sed -i "s/parallel_mode=.*/parallel_mode=false/g" config/pipeline.conf;
                                                fi
                                                sed -i "s/bis_parallel=.*/bis_parallel=$bis_parallel/g" $curr_dir/tmp.conf
                                                sed -i "s/npar=.*/npar=$npar/g" $curr_dir/tmp.conf
                                                sed -i "s/Nthreads=.*/Nthreads=$Nthreads/g" $curr_dir/tmp.conf
                                        fi

                                        if [ "$2" = "bismeth" ]; 
                                        then
                                                bis_parallel=6
                                                if [ $npar -gt 88 ]; then npar=4 && bis_parallel=8;
                                                        elif [ $npar -gt 64 -a $npar -le 88 ]; then npar=2 && bis_parallel=6;
                                                        elif [ $npar -gt 32 -a $npar -le 64 ]; then npar=1 && bis_parallel=5;
                                                        elif [ $npar -gt 16 -a $npar -le 32 ]; then npar=1 && bis_parallel=4;
                                                        elif [ $npar -gt 4 -a $npar -le 16 ]; then  npar=1 && sed -i "s/parallel_mode=.*/parallel_mode=false/g" config/pipeline.conf ;
                                                fi
                                                sed -i "s/bis_parallel=.*/bis_parallel=$bis_parallel/g" $curr_dir/tmp.conf
                                                sed -i "s/npar=.*/npar=$npar/g" $curr_dir/tmp.conf
                                        fi
                elif [ "$1" = "Human" ];
                then 
                                        if [ "$2" = "trimm" ]; 
                                        then
                                                n_th=1
                                                if [ $npar -gt 88 ]; then npar=5 && n_th=5;
                                                        elif [ $npar -gt 64 -a $npar -le 88 ]; then npar=5 && n_th=4;
                                                        elif [ $npar -gt 32 -a $npar -le 64 ]; then npar=3 && n_th=4;
                                                        elif [ $npar -gt 16 -a $npar -le 32 ]; then npar=2 && n_th=4;
                                                        elif [ $npar -gt 4 -a $npar -le 16 ]; then  npar=1;
                                                fi
                                                sed -i "s/n_th=.*/n_th=$n_th/g" $curr_dir/tmp.conf
                                                sed -i "s/npar=.*/npar=$npar/g" $curr_dir/tmp.conf
                                        fi
                                        #---------------------
                                        # Bismark mapper 
                                        #---------------------
                                        if [ "$2" = "bismap" ]; 
                                        then
                                                Nthreads=2
                                                bis_parallel=2
                                                if [ $npar -gt 88 ]; then npar=3 && bis_parallel=8 && Nthreads=5;
                                                        elif [ $npar -gt 64 -a $npar -le 88 ]; then npar=2 && bis_parallel=6 && Nthreads=4;
                                                        elif [ $npar -gt 32 -a $npar -le 64 ]; then npar=1 && bis_parallel=4 && Nthreads=3;
                                                        elif [ $npar -gt 16 -a $npar -le 32 ]; then npar=1 && bis_parallel=3 && Nthreads=2;
                                                        elif [ $npar -gt 4 -a $npar -le 16 ]; then  npar=1 && sed -i "s/parallel_mode=.*/parallel_mode=false/g" config/pipeline.conf;
                                                fi
                                                sed -i "s/bis_parallel=.*/bis_parallel=$bis_parallel/g" $curr_dir/tmp.conf
                                                sed -i "s/npar=.*/npar=$npar/g" $curr_dir/tmp.conf
                                                sed -i "s/Nthreads=.*/Nthreads=$Nthreads/g" $curr_dir/tmp.conf
                                        fi

                                        if [ "$2" = "bismeth" ]; 
                                        then
                                                bis_parallel=6
                                                if [ $npar -gt 88 ]; then npar=4 && bis_parallel=8;
                                                        elif [ $npar -gt 64 -a $npar -le 88 ]; then npar=2 && bis_parallel=6;
                                                        elif [ $npar -gt 32 -a $npar -le 64 ]; then npar=1 && bis_parallel=5;
                                                        elif [ $npar -gt 16 -a $npar -le 32 ]; then npar=1 && bis_parallel=4;
                                                        elif [ $npar -gt 4 -a $npar -le 16 ]; then  npar=1 && sed -i "s/parallel_mode=.*/parallel_mode=false/g" config/pipeline.conf ;
                                                fi
                                                sed -i "s/bis_parallel=.*/bis_parallel=$bis_parallel/g" $curr_dir/tmp.conf
                                                sed -i "s/npar=.*/npar=$npar/g" $curr_dir/tmp.conf
                                        fi

                elif [ "$1" = "scBS-Seq" ];
                then 
                                        if [ "$2" = "trimm" ]; 
                                        then
                                                n_th=1
                                                if [ $npar -gt 88 ]; then npar=5 && n_th=5;
                                                        elif [ $npar -gt 64 -a $npar -le 88 ]; then npar=5 && n_th=4;
                                                        elif [ $npar -gt 32 -a $npar -le 64 ]; then npar=3 && n_th=4;
                                                        elif [ $npar -gt 16 -a $npar -le 32 ]; then npar=2 && n_th=4;
                                                        elif [ $npar -gt 4 -a $npar -le 16 ]; then  npar=1;
                                                fi
                                                sed -i "s/n_th=.*/n_th=$n_th/g" $curr_dir/tmp.conf
                                                sed -i "s/npar=.*/npar=$npar/g" $curr_dir/tmp.conf
                                        fi
                                        #---------------------
                                        # Bismark mapper 
                                        #---------------------
                                        if [ "$2" = "bismap" ]; 
                                        then
                                                Nthreads=2
                                                bis_parallel=2
                                                if [ $npar -gt 88 ]; then npar=3 && bis_parallel=8 && Nthreads=5;
                                                        elif [ $npar -gt 64 -a $npar -le 88 ]; then npar=2 && bis_parallel=6 && Nthreads=4;
                                                        elif [ $npar -gt 32 -a $npar -le 64 ]; then npar=1 && bis_parallel=4 && Nthreads=3;
                                                        elif [ $npar -gt 16 -a $npar -le 32 ]; then npar=1 && bis_parallel=3 && Nthreads=2;
                                                        elif [ $npar -gt 4 -a $npar -le 16 ]; then  npar=1 && sed -i "s/parallel_mode=.*/parallel_mode=false/g" config/pipeline.conf;
                                                fi
                                                sed -i "s/bis_parallel=.*/bis_parallel=$bis_parallel/g" $curr_dir/tmp.conf
                                                sed -i "s/npar=.*/npar=$npar/g" $curr_dir/tmp.conf
                                                sed -i "s/Nthreads=.*/Nthreads=$Nthreads/g" $curr_dir/tmp.conf
                                        fi

                                        if [ "$2" = "bismeth" ]; 
                                        then
                                                bis_parallel=6
                                                if [ $npar -gt 88 ]; then npar=4 && bis_parallel=8;
                                                        elif [ $npar -gt 64 -a $npar -le 88 ]; then npar=2 && bis_parallel=6;
                                                        elif [ $npar -gt 32 -a $npar -le 64 ]; then npar=1 && bis_parallel=5;
                                                        elif [ $npar -gt 16 -a $npar -le 32 ]; then npar=1 && bis_parallel=4;
                                                        elif [ $npar -gt 4 -a $npar -le 16 ]; then  npar=1 && sed -i "s/parallel_mode=.*/parallel_mode=false/g" config/pipeline.conf ;
                                                fi
                                                sed -i "s/bis_parallel=.*/bis_parallel=$bis_parallel/g" $curr_dir/tmp.conf
                                                sed -i "s/npar=.*/npar=$npar/g" $curr_dir/tmp.conf
                                        fi

                fi

                # generals 
                if [ "$2" = "qcFast" ]; 
                then
                        
                        if [ $npar -gt 88 ]; then npar=44;
                                elif [ $npar -gt 64 -a $npar -le 88 ]; then npar=32;
                                elif [ $npar -gt 32 -a $npar -le 64 ]; then npar=16;
                                elif [ $npar -gt 16 -a $npar -le 32 ]; then npar=8;
                                elif [ $npar -gt 4 -a $npar -le 16 ]; then  npar=4;
                        fi
                        sed -i "s/npar=.*/npar=$npar/g" $curr_dir/tmp.conf
                fi

                if [ "$2" = "bisdedu" ]; 
                then
                        
                        if [ $npar -gt 88 ]; then npar=32;
                                elif [ $npar -gt 64 -a $npar -le 88 ]; then npar=22;
                                elif [ $npar -gt 32 -a $npar -le 64 ]; then npar=12;
                                elif [ $npar -gt 16 -a $npar -le 32 ]; then npar=8;
                                elif [ $npar -gt 4 -a $npar -le 16 ]; then  npar=2;
                        fi
                        sed -i "s/npar=.*/npar=$npar/g" $curr_dir/tmp.conf
                fi

                #-----------------------
                # Sorting deduplicate
                #-----------------------
                if [ "$2" = "sort" ]; 
                then
                        
                        if [ $npar -gt 88 ]; then npar=32; 
                                elif [ $npar -gt 64 -a $npar -le 88 ]; then npar=10; 
                                elif [ $npar -gt 32 -a $npar -le 64 ]; then npar=8;
                                elif [ $npar -gt 16 -a $npar -le 32 ]; then npar=4; 
                                elif [ $npar -gt 4 -a $npar -le 16 ]; then  npar=3;
                        fi
                        sed -i "s/npar=.*/npar=$npar/g" $curr_dir/tmp.conf
                fi
                #-----------------------
                # Methimpute
                #-----------------------
                if [ "$2" = "methimpute" ]; 
                then
                        
                        if [ $npar -gt 88 ]; then npar=6; 
                                elif [ $npar -gt 64 -a $npar -le 88 ]; then npar=5; 
                                elif [ $npar -gt 32 -a $npar -le 64 ]; then npar=4;
                                elif [ $npar -gt 16 -a $npar -le 32 ]; then npar=3; 
                                elif [ $npar -gt 4 -a $npar -le 16 ]; then  npar=2;
                        fi
                        sed -i "s/npar=.*/npar=$npar/g" $curr_dir/tmp.conf
                fi
fi

