#!/bin/bash

curr_dir="$(dirname "$0")"
orgPip=$(pwd)
com1=$(awk '/^\[/ { } /=/ { print $0 }' config/pipeline.conf > $curr_dir/tmp.conf)
. $curr_dir/tmp.conf
. $curr_dir/detect.sh  $genome_type  bismap $npar;
. $curr_dir/tmp.conf


## Bismark Mapper- pair mode none-parallel 
#-------------------------------------------------------------------------------
# delete temp file from directory 

if [ `ls $tmp_bismap/*temp* 2>/dev/null | wc -l ` -gt 0   ]
then 
	remove=$(rm $tmp_bismap/*temp*)
fi
#------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
# check point
gen=$(ls -1v $tmp_fq/*.gz | grep "_paired" > $tmp_bismap/list-files.lst)

if [ -f $tmp_bismap/list-finished.lst ]
	then
		echo -e "Resuming process ...\n" 
		proc_a= $(sort $tmp_bismap/list-files.lst -o $tmp_bismap/list-files.lst)
		proc_b= $(sort $tmp_bismap/list-finished.lst -o $tmp_bismap/list-finished.lst)
		proc_c= $(comm -23 $tmp_bismap/list-files.lst $tmp_bismap/list-finished.lst > $tmp_bismap/tmp.lst)
	else
		echo -e "Starting Bismark mapper ...\n" 
		gen=$(cp $tmp_bismap/list-files.lst  $tmp_bismap/tmp.lst)
	fi
#-------------------------------------------------------------------------------



input="$tmp_bismap/tmp.lst"
#-------------------------------------------------------------------------------
#changing directory to write in folder path
tmp_path=$tmp_bismap/
cd "${tmp_path%/*}"

echo -e "Genome Type: $genome_type \n"
if $parallel_mode; then 

	# start to run bismark default -- 4 pairs --> pair_1,unpaired_1 & paired_2, unpaired_2
	# parallel mode
	echo -e "Running Bismark Mapper in Parallel mode, number of jobs that proccessing at same time: $npar . \n" 
	start=$(date +%s)
	doit() {
			. "$1"
			tmp_path=$tmp_bismap/
			cd "${tmp_path%/*}"
			label=$(echo $(echo $2 | sed 's/.*\///') | sed -e "s/_paired$first_pattern//g")
			path=$(echo $(echo $2 | sed -e 's:[^/]*$::'))
			instart=$(date +%s)
			file1=$label"$first_pattern"
			file2=$label"$secnd_pattern"
			if $nucleotide; then
				echo "-- Nucleotide coverage is enabled." 2>&1 | tee -a $tmp_clog/bismark-mapper.log 
				echo "-- Running bismark for $file1 and $file2 ..." 2>&1 | tee -a $tmp_clog/bismark-mapper.log
				result=$($bismark_path/bismark -s 0 -u 0 -n 0 -N 0 -L 20 --parallel $bis_parallel  -p $Nthreads --nucleotide_coverage --genome $genome_ref --bowtie2 --pbat --se $tmp_fq/$file1,$tmp_fq/$file2 -o $tmp_bismap/ 2>&1 | tee -a $tmp_bismap/$label.log ) 
			else
				echo "-- Nucleotide coverage is disabled." 2>&1 | tee -a $tmp_clog/bismark-mapper.log
				echo "-- Running bismark for $file1 and $file2 ..." 2>&1 | tee -a $tmp_clog/bismark-mapper.log
				result=$($bismark_path/bismark -s 0 -u 0 -n 0 -N 0 -L 20 --parallel $bis_parallel -p $Nthreads --genome $genome_ref --bowtie2 --pbat --se $tmp_fq/$file1,$tmp_fq/$file2 -o $tmp_bismap/ 2>&1 | tee -a $tmp_bismap/$label.log)
			fi
			echo $tmp_fq/$file1 >> $tmp_bismap/list-finished.lst;
			echo $tmp_fq/$file2 >> $tmp_bismap/list-finished.lst;
			echo "Bismark for $file1 , $file2 finished. Duration time $((($(date +%s)-$instart)/60)) Minutes." 2>&1 | tee -a $tmp_clog/bismark-mapper.log
			   
		}

	export -f doit
	par=$(echo $curr_dir/tmp.conf) 
	grep "_paired$first_pattern" "$input"  | parallel -j $npar --lb doit "$par"
	runtime=$((($(date +%s)-$start)/60))
	echo "Bismark Mapper finished. Duration $runtime Minutes." 2>&1 | tee -a $tmp_clog/bismark-mapper.log
		
else
	# start to run bismark mapper JUST FOR TWO PAIR
	totaltime=0
	for fq in $(grep "_paired$first_pattern" $tmp_bismap/tmp.lst)
		do 
			start=$(date +%s)
			label=$(echo $(echo $fq | sed 's/.*\///') | sed -e "s/$first_pattern//g")
			file1=$label"$first_pattern"
			file2=$label"$secnd_pattern"
			if $nucleotide; then
				echo "-- Nucleotide coverage is enabled." 2>&1 | tee -a $tmp_clog/bismark-mapper.log 
				echo "-- Running bismark for $file1 and $file2 ..." 2>&1 | tee -a $tmp_clog/bismark-mapper.log
				result=$($bismark_path/bismark -s 0 -u 0 -n 0 -N 0 -L 20 --parallel $bis_parallel  -p $Nthreads --nucleotide_coverage --genome $genome_ref --bowtie2 --pbat --se $tmp_fq/$file1,$tmp_fq/$file2 -o $tmp_bismap/ 2>&1 | tee -a $tmp_bismap/$label.log ) 
			else
				echo "-- Nucleotide coverage is disabled." 2>&1 | tee -a $tmp_clog/bismark-mapper.log
				echo "-- Running bismark for $file1 and $file2 ..." 2>&1 | tee -a $tmp_clog/bismark-mapper.log
				result=$($bismark_path/bismark -s 0 -u 0 -n 0 -N 0 -L 20 --parallel $bis_parallel -p $Nthreads --genome $genome_ref --bowtie2 --pbat --se $tmp_fq/$file1,$tmp_fq/$file2 -o $tmp_bismap/ 2>&1 | tee -a $tmp_bismap/$label.log)
			fi
			echo $tmp_fq/$file1 >> $tmp_bismap/list-finished.lst;
			echo $tmp_fq/$file2 >> $tmp_bismap/list-finished.lst;
			runtime=$((($(date +%s)-$start)/60))
			echo "Bismark for $file1 and $file2 finished. Duration time $runtime Minutes." 2>&1 | tee -a $tmp_clog/bismark-mapper.log
			totaltime=$(($runtime + $totaltime))
			echo -e "-------------------------------------------- \n"
		done
		echo "Bismark Mapper done. Total running time $totaltime Minutes." 2>&1 | tee -a $tmp_clog/bismark-mapper.log

	
fi

if [ -f $tmp_bismap/tmp.lst ]
then 
	remove=$(rm $tmp_bismap/tmp.lst)
fi


#------------------------------------ Renaming
for file in $(ls -1v $tmp_bismap/*.bam | grep "_paired_1" )
	do
		label=$(echo $(echo $file | sed 's/.*\///') | sed -e "s/_paired_1_bismark_bt2.bam//g")
		echo "Merging $label.bam file..."
		
		mer=$(samtools cat -o $tmp_bismap/$label.bam $tmp_bismap/"$label"_paired_1_bismark_bt2.bam $tmp_bismap/"$label"_paired_2_bismark_bt2.bam)
		if [ -f $tmp_bismap/$label.bam ];
		then 
			remove1=$(rm $tmp_bismap/"$label"_paired_1_bismark_bt2.bam)
			remove2=$(rm $tmp_bismap/"$label"_paired_2_bismark_bt2.bam)
		fi
		
	done


cd $orgPip

if [ -f $tmp_bismap/tmp.lst ]
then 
	remove=$(rm $tmp_bismap/tmp.lst)
fi

# check if everyfiles finished, then delete queue list 
if [ -z $(comm -23 <(sort -u $tmp_bismap/list-files.lst) <(sort -u $tmp_bismap/list-finished.lst)) ]  
then
	com=$(sed -i "s/st_bismark=.*/st_bismark=2/g" config/pipeline.conf)
	remove=$(rm $tmp_bismap/list-finished.lst)
fi

# docker part 
if $docker_mode; 
then
	perm=$(chmod 777 -R $result_pipeline)
fi
