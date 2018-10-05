#!/bin/bash
curr_dir="$(dirname "$0")"
com1=$(awk '/^\[/ { } /=/ { print $0 }' config/pipeline.conf > $curr_dir/tmp.conf)
. $curr_dir/tmp.conf


## Bismark Mapper

## Creating reference genome folders FOR FIRST TIME

if [ ! -d $genome_ref/Bisulfite_Genome ]; then
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
	echo "reference file modified, generating the new one..." ;
	gen=$($bismark_path/bismark_genome_preparation --verbose $genome_ref/)
	com1=$(awk '/^\[/ { } /=/ { print $0 }' config/pipeline.conf > $curr_dir/tmp.conf)
	. $curr_dir/tmp.conf
else
     echo "No changes in Ref.genome.";

fi


#-------------------------------------------------------------------------------
# check point
gen=$(ls -1v $tmp_fq/*.gz > $tmp_bismap/list-files.lst)

if [ -f $tmp_bismap/list-finished.lst ]
	then
		echo "Resuming process ..."
		proc_a= $(sort $tmp_bismap/list-files.lst -o $tmp_bismap/list-files.lst)
		proc_b= $(sort $tmp_bismap/list-finished.lst -o $tmp_bismap/list-finished.lst)
		proc_c= $(comm -23 $tmp_bismap/list-files.lst $tmp_bismap/list-finished.lst > $tmp_bismap/tmp.lst)
		input="$tmp_bismap/tmp.lst"
		while read line
			do
				arr+=("$line")
			done < $input;
	else

		input="$tmp_bismap/list-files.lst"
		while read line
		do
			arr+=("$line")
		done < $input;
	fi


#changing directory to write in folder path
tmp_path=$tmp_bismap/
cd "${tmp_path%/*}"

#-------------------------------------------------------------------------------
# start to run bismark mapper
for fq in "${arr[@]}"

	do
		start=$(date +%s)
		echo "----------------------------------------------------------------------"
		label=$(echo ${fq%%.*} |sed 's/.*\///')
		echo "Starting bismark for $label... "
		if $nucleotide; then
			# generating nucleotide report
			result=$($bismark_path/bismark -s 0 -u 0 -n 0 -l 20 --parallel $bis_parallel --nucleotide_coverage --genome $genome_ref -q $fq -o $tmp_bismap/ 2>&1 | tee -a $tmp_bismap/$label.log )
		else
			echo "Nucleotide coverage is disabled."
			result=$($bismark_path/bismark -s 0 -u 0 -n 0 -l 20 --parallel $bis_parallel --genome $genome_ref -q $fq -o $tmp_bismap/ 2>&1 | tee -a $tmp_bismap/$label.log)
		fi
		#---------------------------------------------------------------------------
		echo $fq >> $tmp_bismap/list-finished.lst;
		end=$(date +%s)
		runtime=$((($(date +%s)-$start)/60))
		#---------------------------------------------------------------------------
		echo "Bismark for $label finished. Duration $runtime Minutes."
		echo "----------------------------------------------------------------------"

	done

echo "Bismark part finished. Please check the $tmp_bismap directory for logs."
