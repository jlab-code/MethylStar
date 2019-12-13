#!/bin/bash
curr_dir="$(dirname "$0")"
com1=$(awk '/^\[/ { } /=/ { print $0 }' config/pipeline.conf > $curr_dir/tmp.conf)
. $curr_dir/tmp.conf
. $curr_dir/detect.sh  $genome_type  sort $npar;
. $curr_dir/tmp.conf


: '
Generate Sorting bam files.
'

#generating up-to-date list of files
# check point

type=$1

if [ "$type" = "deduplicate" ]; 
then
		tmp_dir=$tmp_dide
		st_status=st_dedsort
else
		tmp_dir=$tmp_bismap
		st_status=st_bissort
fi

gen=$(ls -1v $tmp_dir/*.bam > $tmp_covseq/list-files.lst)

if [ -f $tmp_covseq/list-finished.lst ]
	then
		echo -e "-- Resuming process ...\n" 
		proc_a= $(sort $tmp_covseq/list-files.lst -o $tmp_covseq/list-files.lst)
		proc_b= $(sort $tmp_covseq/list-finished.lst -o $tmp_covseq/list-finished.lst)
		proc_c= $(comm -23 $tmp_covseq/list-files.lst $tmp_covseq/list-finished.lst > $tmp_covseq/tmpsort.lst)
		input="$tmp_covseq/tmpsort.lst"
		while read line
			do
				arr+=("$line")
			done < $input;
	else
		echo -e "-- Starting to sort bam files ...\n" 
		input="$tmp_covseq/list-files.lst"
		while read line
		do
			arr+=("$line")
		done < $input;
	fi

#--------------------------------------------------------

if $parallel_mode; then
		echo -e "-- Running in Parallel mode, number of jobs: $npar .\n" 
		start=$(date +%s)
		doit() {
				. "$1"
				label=$(echo $(echo "$2" | sed 's/.*\///') | sed -e 's/.bam//g')						
				# Sleep up to 10 seconds
				echo "-- Running sort for $label ..." 2>&1 | tee -a $tmp_clog/bismark-sorting.log
				ded=$(samtools sort -@ 4 -m 4G -o $tmp_covseq/sorted-$label.bam "$2")
				: '
				if [ -f $tmp_covseq/sorted-$label.bam ]
				then
					rem=$(rm "$2")
				fi
				'
				echo "$2" >> $tmp_covseq/list-finished.lst;  
				
		}
		export -f doit
		par=$(echo $curr_dir/tmp.conf) 
		cat  "$input"  | parallel -j $npar --lb doit "$par"
		runtime=$((($(date +%s)-$start)/60))
		echo -e "-- Sort finished. Total time $runtime minutes." 2>&1 | tee -a $tmp_clog/bismark-sorting.log
		echo -e "**You can find the result in $tmp_covseq folder.**\n"

else
	#running in single mode
	echo -e "-- Running in single mode! \n"  
	totaltime=0
	for bamfile in "${arr[@]}"
			do
				start=$(date +%s)
				label=$(echo $(echo $bamfile | sed 's/.*\///') | sed -e 's/.bam//g')
				echo "-- Running sort for $label ..." 
				ded=$(samtools sort -@ 4 -m 4G -o $tmp_covseq/sorted-$label.bam $bamfile )
				: '
				if [ -f $tmp_covseq/sorted-$label.bam ]
				then
					rem=$(rm $bamfile)
				fi
				'
				runtime=$((($(date +%s)-$start)/60))
				echo $bamfile >> $tmp_covseq/list-finished.lst;
				
				echo "-- Sorting finished, for $label finished in $runtime minutes." 2>&1 | tee -a $tmp_clog/bismark-sorting.log
				totaltime=$(($runtime + $totaltime))
				echo -e "-----------------------------------" 
			done
	echo -e "Sort finished. Total time $totaltime minutes."  2>&1 | tee -a $tmp_clog/bismark-sorting.log

fi



if [ -f $tmp_covseq/tmpsort.lst ]
then 
	remove=$(rm $tmp_covseq/tmpsort.lst)
fi

# check if everyfiles done then delete queue list 
if [ -z $(comm -23 <(sort -u $tmp_covseq/list-files.lst) <(sort -u $tmp_covseq/list-finished.lst)) ]  
then
	com=$(sed -i "s/$st_status=.*/$st_status=2/g" config/pipeline.conf)
	remove=$(rm $tmp_covseq/list-*.lst)
fi
# docker part 
if $docker_mode; 
then
	perm=$(chmod 777 -R $result_pipeline)
fi