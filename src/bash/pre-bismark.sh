#!/bin/bash
curr_dir="$(dirname "$0")"
com1=$(awk '/^\[/ { } /=/ { print $0 }' config/pipeline.conf > $curr_dir/tmp.conf)
. $curr_dir/tmp.conf


## Bismark Mapper
#-------------------------------------------------------------------------------
# check point
gen=$(ls -1v $tmp_fq/*.gz > $tmp_bismap/list-files.lst)

if [ -f $tmp_bismap/list-finished.lst ]
	then
		echo "Resuming process ..." 
		proc_a= $(sort $tmp_bismap/list-files.lst -o $tmp_bismap/list-files.lst)
		proc_b= $(sort $tmp_bismap/list-finished.lst -o $tmp_bismap/list-finished.lst)
		proc_c= $(comm -23 $tmp_bismap/list-files.lst $tmp_bismap/list-finished.lst > $tmp_bismap/tmp.lst)
	else
		echo "Starting Bismark mapper ..." 
		gen=$(cp $tmp_bismap/list-files.lst  $tmp_bismap/tmp.lst)
	fi
#-------------------------------------------------------------------------------
## Creating reference genome folders FOR FIRST TIME

if [ ! -d $genome_ref/Bisulfite_Genome ]; then
	echo "Preparing reference genome ...."
	gen=$($bismark_path/bismark_genome_preparation --verbose $genome_ref/)
	current_modified=$(stat -c "%Y" $genome_ref/$genome_name)
	sed -i "s/modified_time=.*/modified_time=$current_modified/g" config/pipeline.conf
	com1=$(awk '/^\[/ { } /=/ { print $0 }' config/pipeline.conf > $curr_dir/tmp.conf)
	. $curr_dir/tmp.conf

fi

## Checking if the references genome "TAIR10_chr_all.fa" is modified!
## if modified then regenerate the reference genome.

current_modified=$(stat -c "%Y" $genome_ref/$genome_name)
if [ "$modified_time" -lt "$current_modified" ]; then
	sed -i "s/modified_time=.*/modified_time=$current_modified/g" config/pipeline.conf
	echo "The reference file modified, generating the new one..." 
	gen=$($bismark_path/bismark_genome_preparation --verbose $genome_ref/)
	com1=$(awk '/^\[/ { } /=/ { print $0 }' config/pipeline.conf > $curr_dir/tmp.conf)
	. $curr_dir/tmp.conf
else
     echo "No changes in Ref.genome." 

fi

#-------------------------------------------------------------------------------
