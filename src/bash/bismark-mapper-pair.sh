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
input="$tmp_bismap/tmp.lst"
#-------------------------------------------------------------------------------
#changing directory to write in folder path
tmp_path=$tmp_bismap/
cd "${tmp_path%/*}"

echo -e "Genome Type: $genome_type \n"

if $run_pair_bismark; then 

	# start to run bismark default -- 4 pairs --> pair_1,unpaired_1 & paired_2, unpaired_2
	totaltime=0
	for fq in $(grep "_paired$first_pattern" $tmp_bismap/tmp.lst)
		do 
			start=$(date +%s)
			label=$(echo $(echo $fq | sed 's/.*\///') | sed -e "s/_paired$first_pattern//g")
			file1=$label"_paired$first_pattern"
			file2=$label"_unpaired$first_pattern"
			file3=$label"_paired$secnd_pattern"
			file4=$label"_unpaired$secnd_pattern"
			if $nucleotide; then
				echo "-- Nucleotide coverage is enabled." 2>&1 | tee -a $tmp_clog/bismark-mapper.log  
				echo "-- Running bismark for $file1 , $file2 and $file3 , $file4 ..." 2>&1 | tee -a $tmp_clog/bismark-mapper.log
				result=$($bismark_path/bismark -s 0 -u 0 -n 0 -l 20 --samtools_path $samtools_path --parallel $bis_parallel -p $Nthreads  --nucleotide_coverage --genome $genome_ref -1 $tmp_fq/$file1 $tmp_fq/$file2 -2 $tmp_fq/$file3 $tmp_fq/$file4 -o $tmp_bismap/ 2>&1 | tee -a $tmp_bismap/$label.log ) 
			else
				echo "-- Nucleotide coverage is disabled." 2>&1 | tee -a $tmp_clog/bismark-mapper.log
				echo "-- Running bismark for $file1 , $file2 and $file3 , $file4 ..." 2>&1 | tee -a $tmp_clog/bismark-mapper.log
				result=$($bismark_path/bismark -s 0 -u 0 -n 0 -l 20 --samtools_path $samtools_path --parallel $bis_parallel  -p $Nthreads --genome $genome_ref -1 $tmp_fq/$file1 $tmp_fq/$file2 -2 $tmp_fq/$file3 $tmp_fq/$file4 -o $tmp_bismap/ 2>&1 | tee -a $tmp_bismap/$label.log)
			fi	
			echo $tmp_fq/$file1 >> $tmp_bismap/list-finished.lst;
			echo $tmp_fq/$file2 >> $tmp_bismap/list-finished.lst;
			echo $tmp_fq/$file3 >> $tmp_bismap/list-finished.lst;
			echo $tmp_fq/$file4 >> $tmp_bismap/list-finished.lst;
			echo "Bismark for $file1 , $file2 , $file3 , $file4 finished." 
			runtime=$((($(date +%s)-$start)/60)) 
			echo "-- Bismark for $file1 , $file2 , $file3 , $file4 finished. Duration time $runtime Minutes." >> $tmp_clog/bismark-mapper.log
			echo -e "-------------------------------------------- \n"
			totaltime=$(($runtime + $totaltime))
		done
		echo "Bismark Mapper finished. Total time $totaltime Minutes." 2>&1 | tee -a $tmp_clog/bismark-mapper.log
		
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
				result=$($bismark_path/bismark -N 1 -L 32 --samtools_path $samtools_path --parallel $bis_parallel  -p $Nthreads --nucleotide_coverage --genome $genome_ref -1 $tmp_fq/$file1 -2 $tmp_fq/$file2 -o $tmp_bismap/ 2>&1 | tee -a $tmp_bismap/$label.log ) 
			else
				echo "-- Nucleotide coverage is disabled." 2>&1 | tee -a $tmp_clog/bismark-mapper.log
				echo "-- Running bismark for $file1 and $file2 ..." 2>&1 | tee -a $tmp_clog/bismark-mapper.log
				result=$($bismark_path/bismark -N 1 -L 32 --samtools_path $samtools_path --parallel $bis_parallel -p $Nthreads --genome $genome_ref -1 $tmp_fq/$file1 -2 $tmp_fq/$file2 -o $tmp_bismap/ 2>&1 | tee -a $tmp_bismap/$label.log)
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
for file in $(ls -1v $tmp_bismap/*.bam)
	do
		label=$(echo $(echo $file | sed 's/.*\///') | sed -e "s/_bismark_bt2_pe.bam//g")
		tmp=$(echo $label | sed "s/_paired_.//g")
		#tmp=$(echo $file | sed 's/.*\///')
		#fname=$(echo ${tmp%%.*})
		mv $file $tmp_bismap/$tmp.bam
	done
# rename logs to fq
for file in $(ls -1v $tmp_bismap/*_bismark_bt2_PE_report.txt)
        do
                label=$(echo $(echo $file | sed 's/.*\///') | sed -e "s/_bismark_bt2_PE_report.txt//g")
                tmp=$(echo $label | sed "s/_paired_.//g")
                mv $file $tmp_bismap/$tmp.txt
        done

for file in $(ls -1v $tmp_bismap/*nucleotide_stats.txt)
        do
                label=$(echo $(echo $file | sed 's/.*\///') | sed -e "s/_bismark_bt2_pe.nucleotide_stats.txt//g")
                #tmp=$(echo $label | sed "s/_paired_.//g")
                mv $file $tmp_bismap/$label_ns.txt
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

