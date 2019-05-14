#!/bin/bash
curr_dir="$(dirname "$0")"
com1=$(awk '/^\[/ { } /=/ { print $0 }' config/pipeline.conf > $curr_dir/tmp.conf)
. $curr_dir/tmp.conf


## Bismark Mapper
#-------------------------------------------------------------------------------
# check point

if [ `ls $tmp_bismap/*temp* 2>/dev/null | wc -l ` -gt 0   ]
then 
	remove=$(rm $tmp_bismap/*temp*)
fi

input="$tmp_bismap/tmp.lst"
while read line
do
		arr+=("$line")
done < $input;

#-------------------------------------------------------------------------------
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
			echo "Nucleotide coverage is enabled." 
			echo "Running bismark for $label ..." 2>&1 | tee -a $tmp_clog/bismark-mapper.log
			result=$($bismark_path/bismark -s 0 -u 0 -N 0 -L 20 --parallel $bis_parallel --nucleotide_coverage --genome $genome_ref -q $fq -o $tmp_bismap/ 2>&1 | tee -a $tmp_bismap/$label.log )
		else
			echo "Nucleotide coverage is disabled." 
			echo "Running bismark for $label ..." 2>&1 | tee -a $tmp_clog/bismark-mapper.log
			result=$($bismark_path/bismark -s 0 -u 0 -N 0 -L 20 --parallel $bis_parallel --genome $genome_ref -q $fq -o $tmp_bismap/ 2>&1 | tee -a $tmp_bismap/$label.log)
		fi
		#---------------------------------------------------------------------------
		echo $fq >> $tmp_bismap/list-finished.lst;
		runtime=$((($(date +%s)-$start)/60))
		echo "Bismark for $label finished. Duration time $runtime Minutes." 2>&1 | tee -a $tmp_clog/bismark-mapper.log
		totaltime=$(($runtime + $totaltime))
	done
	echo "Bismark Mapper done. Total running time $totaltime Minutes." 2>&1 | tee -a $tmp_clog/bismark-mapper.log
	echo "Bismark part finished. Please check the $tmp_bismap directory for logs." 
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