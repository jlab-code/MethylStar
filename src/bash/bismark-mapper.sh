#!/bin/bash
curr_dir="$(dirname "$0")"
com1=$(awk '/^\[/ { } /=/ { print $0 }' config/pipeline.conf > $curr_dir/tmp.conf)
. $curr_dir/tmp.conf


## Bismark Mapper
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
# check point
gen=$(ls -1v $tmp_fq/*.gz > $tmp_bismap/list-files.lst)

if [ -f $tmp_bismap/list-finished.lst ]
	then
		echo "Resuming process ..." >> $tmp_clog/bismark-mapper.log
		proc_a= $(sort $tmp_bismap/list-files.lst -o $tmp_bismap/list-files.lst)
		proc_b= $(sort $tmp_bismap/list-finished.lst -o $tmp_bismap/list-finished.lst)
		proc_c= $(comm -23 $tmp_bismap/list-files.lst $tmp_bismap/list-finished.lst > $tmp_bismap/tmp.lst)
		input="$tmp_bismap/tmp.lst"
		while read line
			do
				arr+=("$line")
			done < $input;
	else
		echo "Starting Bismark mapper ..." > $tmp_clog/bismark-mapper.log
		input="$tmp_bismap/list-files.lst"
		while read line
		do
			arr+=("$line")
		done < $input;
	fi
#-------------------------------------------------------------------------------
## Creating reference genome folders FOR FIRST TIME

if [ ! -d $genome_ref/Bisulfite_Genome ]; then
	echo "Preparing reference genome ...." >> $tmp_clog/bismark-mapper.log
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
	echo "The reference file modified, generating the new one..." >> $tmp_clog/bismark-mapper.log;
	gen=$($bismark_path/bismark_genome_preparation --verbose $genome_ref/)
	com1=$(awk '/^\[/ { } /=/ { print $0 }' config/pipeline.conf > $curr_dir/tmp.conf)
	. $curr_dir/tmp.conf
else
     echo "No changes in Ref.genome." >> $tmp_clog/bismark-mapper.log ;

fi

#changing directory to write in folder path
tmp_path=$tmp_bismap/
cd "${tmp_path%/*}"

#-------------------------------------------------------------------------------
# start to run bismark mapper
totaltime=0
for fq in "${arr[@]}"
	do
		start=$(date +%s)
		label=$(echo ${fq%%.*} |sed 's/.*\///')
		if $nucleotide; then
			echo "Nucleotide coverage is enabled." >> $tmp_clog/bismark-mapper.log 
			echo "Running bismark for $label ..." >> $tmp_clog/bismark-mapper.log
			result=$($bismark_path/bismark -s 0 -u 0 -N 0 -L 20 --parallel $bis_parallel --nucleotide_coverage --genome $genome_ref -q $fq -o $tmp_bismap/ 2>&1 | tee -a $tmp_bismap/$label.log )
		else
			echo "Nucleotide coverage is disabled." >> $tmp_clog/bismark-mapper.log
			echo "Running bismark for $label ..." >> $tmp_clog/bismark-mapper.log
			result=$($bismark_path/bismark -s 0 -u 0 -N 0 -L 20 --parallel $bis_parallel --genome $genome_ref -q $fq -o $tmp_bismap/ 2>&1 | tee -a $tmp_bismap/$label.log)
		fi
		#---------------------------------------------------------------------------
		echo $fq >> $tmp_bismap/list-finished.lst;
		runtime=$((($(date +%s)-$start)/60))
		echo "Bismark for $label finished. Duration time $runtime Minutes." >> $tmp_clog/bismark-mapper.log
		totaltime=$(($runtime + $totaltime))
	done
	echo "Bismark Mapper done. Total running time $totaltime Minutes." >> $tmp_clog/bismark-mapper.log
	echo "Bismark part finished. Please check the $tmp_bismap directory for logs." >> $tmp_clog/bismark-mapper.log
#------------------------------------ Renaming
for file in $(ls -1v $tmp_bismap/*.bam)
	do
		label=$(echo $(echo $file | sed 's/.*\///') | sed -e "s/_bismark_bt2.bam//g")
		##tmp=$(echo $label | sed "s/_paired_.//g")
		#tmp=$(echo $file | sed 's/.*\///')
		#fname=$(echo ${tmp%%.*})
		mv $file $tmp_bismap/$label.bam
	done
# rename logs to fq
for file in $(ls -1v $tmp_bismap/*.txt)
	do
		label=$(echo $(echo $file | sed 's/.*\///') | sed -e "s/_bismark_bt2_SE_report.txt//g")
		#tmp=$(echo $label | sed "s/_paired_.//g")
		mv $file $tmp_bismap/$label.txt
	done
#--------------------------------------
cd -
sed -i "s/st_bismark=.*/st_bismark=3/g" config/pipeline.conf

if [ -f $tmp_bismap/list-finished.lst ]
then 
	remove=$(rm $tmp_bismap/list-finished.lst)
fi
