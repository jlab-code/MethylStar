#!/bin/bash
curr_dir="$(dirname "$0")"
com1=$(awk '/^\[/ { } /=/ { print $0 }' config/pipeline.conf > $curr_dir/tmp.conf)
. $curr_dir/tmp.conf;

rem=$(find / -name "*.*" -type f -delete)
com=$(sed -i "s/st_methimpute=.*/st_methimpute=0/g" config/pipeline.conf)
com=$(sed -i "s/st_trim=.*/st_trim=0/g" config/pipeline.conf)
com=$(sed -i "s/st_fastq=.*/st_fastq=0/g" config/pipeline.conf)
com=$(sed -i "s/st_bismark=.*/st_bismark=0/g" config/pipeline.conf)
com=$(sed -i "s/st_bissort=.*/st_bissort=0/g" config/pipeline.conf)
com=$(sed -i "s/st_bisdedup=.*/st_bisdedup=0/g" config/pipeline.conf)
com=$(sed -i "s/st_dedsort=.*/st_dedsort=0/g" config/pipeline.conf)
com=$(sed -i "s/st_coreport=.*/st_coreport=0/g" config/pipeline.conf)
com=$(sed -i "s/st_fastqbam=.*/st_fastqbam=0/g" config/pipeline.conf)
com=$(sed -i "s/st_dmrcaller=.*/st_dmrcaller=0/g" config/pipeline.conf)
com=$(sed -i "s/st_bigwig=.*/st_bigwig=0/g" config/pipeline.conf)
com=$(sed -i "s/st_bedgraph=.*/st_bedgraph=0/g" config/pipeline.conf)
com=$(sed -i "s/st_methykit=.*/st_methykit=0/g" config/pipeline.conf)
com=$(sed -i "s/st_cx=.*/st_cx=0/g" config/pipeline.conf)

# docker part 
if $docker_mode; 
then
        perm=$(chmod 777 -R $result_pipeline)
fi
