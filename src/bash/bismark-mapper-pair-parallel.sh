#!/bin/bash
curr_dir="$(dirname "$0")"
com1=$(awk '/^\[/ { } /=/ { print $0 }' config/pipeline.conf > $curr_dir/tmp.conf)
. $curr_dir/detect.sh bismap;
. $curr_dir/tmp.conf;

## Bismark Mapper
#-------------------------------------------------------------------------------
gen=$(ls -1v $tmp_fq/*.gz > $tmp_bismap/list-files.lst)

if [ -f $tmp_bismap/list-finished.lst ]
	then
		echo "Resuming process ..." >> $tmp_clog/bismark-mapper.log
		proc_a= $(sort $tmp_bismap/list-files.lst -o $tmp_bismap/list-files.lst)
		proc_b= $(sort $tmp_bismap/list-finished.lst -o $tmp_bismap/list-finished.lst)
		proc_c= $(comm -23 $tmp_bismap/list-files.lst $tmp_bismap/list-finished.lst > $tmp_bismap/tmp.lst)
		input="$tmp_bismap/tmp.lst"
	else
		input="$tmp_bismap/list-files.lst"
		echo "Starting Bismark Mapper ..." > $tmp_clog/bismark-mapper.log

	fi
#------------------------------------------------------------------------------
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

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#changing directory to write in folder path

#tmp_path=$tmp_bismap/
#cd "${tmp_path%/*}"


if $run_pair_bismark; then 

	# start to run bismark default -- 4 pairs --> pair_1,unpaired_1 & paired_2, unpaired_2
	# parallel mode
	echo "Running Bismark Mapper in Parallel mode, number of jobs that proccessing at same time: $npar ." >> $tmp_clog/bismark-mapper.log;
	start=$(date +%s)
	doit() {
		. "$1"
		tmp_path=$tmp_bismap/
		cd "${tmp_path%/*}"
		label=$(echo $(echo $2 | sed 's/.*\///') | sed -e "s/_paired$first_pattern//g")
		path=$(echo $(echo $2 | sed -e 's:[^/]*$::'))
		echo $label >> $tmp_clog/bismark-mapper.log
		instart=$(date +%s)
		file1=$label"_paired$first_pattern"
		file2=$label"_unpaired$first_pattern"
		file3=$label"_paired$secnd_pattern"
		file4=$label"_unpaired$secnd_pattern"
		echo "$file1 , $file2 and $file3 , $file4" >> $tmp_clog/bismark-mapper.log
			if $nucleotide; then
				echo "Nucleotide coverage is enabled." >> $tmp_clog/bismark-mapper.log  
				echo "Running bismark for $file1 , $file2 and $file3 , $file4 ..." >> $tmp_clog/bismark-mapper.log
				result=$($bismark_path/bismark -s 0 -u 0 -n 0 -l 20 --parallel $bis_parallel --nucleotide_coverage --genome $genome_ref -1 $tmp_fq/$file1 $tmp_fq/$file2 -2 $tmp_fq/$file3 $tmp_fq/$file4 -o $tmp_bismap/ 2>&1 | tee -a $tmp_bismap/$label.log ) 
			else
				echo "Nucleotide coverage is disabled." >> $tmp_clog/bismark-mapper.log
				echo "Running bismark for $file1 , $file2 and $file3 , $file4 ..." >> $tmp_clog/bismark-mapper.log
				result=$($bismark_path/bismark -s 0 -u 0 -n 0 -l 20 --parallel $bis_parallel --genome $genome_ref -1 $tmp_fq/$file1 $tmp_fq/$file2 -2 $tmp_fq/$file3 $tmp_fq/$file4 -o $tmp_bismap/ 2>&1 | tee -a $tmp_bismap/$label.log)
			fi	
			echo $tmp_fq/$file1 >> $tmp_bismap/list-finished.lst;
			echo $tmp_fq/$file2 >> $tmp_bismap/list-finished.lst;
			echo $tmp_fq/$file3 >> $tmp_bismap/list-finished.lst;
			echo $tmp_fq/$file4 >> $tmp_bismap/list-finished.lst;
			echo "Bismark for $file1 , $file2 , $file3 , $file4 finished. Duration time $((($(date +%s)-$instart)/60)) Minutes." >> $tmp_clog/bismark-mapper.log
			   
		}

	export -f doit
	par=$(echo $curr_dir/tmp.conf) 
	grep "_paired$first_pattern" "$input"  | parallel -j $npar doit "$par"
	runtime=$((($(date +%s)-$start)/60))
	echo "Bismark Mapper finished. Duration $runtime Minutes." >> $tmp_clog/bismark-mapper.log	

else
	echo "Running Bismark Mapper in Parallel mode, number of jobs that proccessing at same time: $npar ." >> $tmp_clog/bismark-mapper.log;
	start=$(date +%s)
	doit() {
		. "$1"
		tmp_path=$tmp_bismap/
		cd "${tmp_path%/*}"

		label=$(echo $(echo $2 | sed 's/.*\///') | sed -e "s/$first_pattern//g")
		file1=$label"$first_pattern"
		file2=$label"$secnd_pattern"
		if $nucleotide; then
			echo "Nucleotide coverage is enabled." >> $tmp_clog/bismark-mapper.log 
			echo "Running bismark for $file1 and $file2 ..." >> $tmp_clog/bismark-mapper.log
			result=$($bismark_path/bismark -N 1 -L 32 --parallel $bis_parallel --nucleotide_coverage --genome $genome_ref -1 $tmp_fq/$file1 -2 $tmp_fq/$file2 -o $tmp_bismap/ 2>&1 | tee -a $tmp_bismap/$label.log ) 
		else
			echo "Nucleotide coverage is disabled." >> $tmp_clog/bismark-mapper.log
			echo "Running bismark for $file1 and $file2 ..." >> $tmp_clog/bismark-mapper.log
			result=$($bismark_path/bismark -N 1 -L 32 --parallel $bis_parallel --genome $genome_ref -1 $tmp_fq/$file1 -2 $tmp_fq/$file2 -o $tmp_bismap/ 2>&1 | tee -a $tmp_bismap/$label.log)
		fi
		echo $tmp_fq/$file1 >> $tmp_bismap/list-finished.lst;
		echo $tmp_fq/$file2 >> $tmp_bismap/list-finished.lst;
		

	}
	export -f doit
	par=$(echo $curr_dir/tmp.conf) 
	grep "_paired$first_pattern" "$input"  | parallel -j $npar doit "$par"
	runtime=$((($(date +%s)-$start)/60))
	echo "Bismark for $file1 and $file2 finished. Duration time $runtime Minutes." >> $tmp_clog/bismark-mapper.log


fi		



if [ -f $tmp_bismap/tmp.lst ]
then 
	remove=$(rm $tmp_bismap/tmp.lst)
fi

echo "Bismark part finished. Please check the $tmp_bismap directory for logs." >> $tmp_clog/bismark-mapper.log



#------------------------------------ Renaming
for file in $(ls -1v $tmp_bismap/*.bam)
	do
		label=$(echo $(echo $file | sed 's/.*\///') | sed -e "s/_bismark_bt2_pe.bam//g")
		tmp=$(echo $label | sed "s/_paired_.//g")
		#tmp=$(echo $file | sed 's/.*\///')
		#fname=$(echo ${tmp%%.*})
		mv $file $tmp_bismap/$tmp.bam
	done
# rename logs to fq
for file in $(ls -1v $tmp_bismap/*.txt)
	do
		label=$(echo $(echo $file | sed 's/.*\///') | sed -e "s/_bismark_bt2_PE_report.txt//g")
		tmp=$(echo $label | sed "s/_paired_.//g")
		mv $file $tmp_bismap/$tmp.txt
	done
#--------------------------------------
cd -
sed -i "s/st_bismark=.*/st_bismark=3/g" config/pipeline.conf

if [ -f $tmp_bismap/list-finished.lst ]
then 
	remove=$(rm $tmp_bismap/list-finished.lst)
fi

