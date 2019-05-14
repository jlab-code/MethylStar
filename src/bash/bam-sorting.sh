#!/bin/bash
curr_dir="$(dirname "$0")"
com1=$(awk '/^\[/ { } /=/ { print $0 }' config/pipeline.conf > $curr_dir/tmp.conf)
. $curr_dir/detect.sh sort;
. $curr_dir/tmp.conf


: '
Generate Sorting files.
'

#generating up-to-date list of files
# check point
gen=$(ls -1v $tmp_dide/*.bam > $tmp_dide/list-files.lst)

if [ -f $tmp_dide/list-finished.lst ]
	then
		echo "Resuming process ..." 
		proc_a= $(sort $tmp_dide/list-files.lst -o $tmp_dide/list-files.lst)
		proc_b= $(sort $tmp_dide/list-finished.lst -o $tmp_dide/list-finished.lst)
		proc_c= $(comm -23 $tmp_dide/list-files.lst $tmp_dide/list-finished.lst > $tmp_dide/tmp.lst)
		input="$tmp_dide/tmp.lst"
		while read line
			do
				arr+=("$line")
			done < $input;
	else
		echo "Starting to sort bam files ..." 
		input="$tmp_dide/list-files.lst"
		while read line
		do
			arr+=("$line")
		done < $input;
	fi
# running main prog
#--------------------------------------------------------

if $parallel_mode; then
		echo "Running in Parallel mode, number of jobs: $npar ." 
		start=$(date +%s)
		doit() {
				. "$1"
				label=$(echo $(echo "$2" | sed 's/.*\///') | sed -e 's/.bam//g')						
				# Sleep up to 10 seconds
				echo "Running sort for $label ..." 2>&1 | tee -a $tmp_clog/bismark-sorting.log
				ded=$(samtools sort -@ 4 -m 4G -o $tmp_dide/$label-sorted.bam "$2")
				if [ -f $tmp_dide/$label-sorted.bam ]
				then
					rem=$(rm "$2")
				fi
				echo $2 >> $tmp_dide/list-finished.lst;   
				
		}
		export -f doit
		par=$(echo $curr_dir/tmp.conf) 
		cat  "$input"  | parallel -j $npar doit "$par"
		runtime=$((($(date +%s)-$start)/60))
		echo "Sort finished. Total time $runtime minutes." 2>&1 | tee -a $tmp_clog/bismark-sorting.log
		echo "You can find the result in $tmp_dide folder."

else
	#running in single mode
	echo "Running in single mode!"  
	totaltime=0
	for bamfile in "${arr[@]}"
			do
				start=$(date +%s)
				label=$(echo $(echo $bamfile | sed 's/.*\///') | sed -e 's/.bam//g')
				echo "Running sort for $label ..." 
				ded=$(samtools sort -@ 4 -m 4G -o $tmp_dide/$label-sorted.bam $bamfile )
				
				if [ -f $tmp_dide/$label-sorted.bam ]
				then
					rem=$(rm $bamfile)
				fi
				
				runtime=$((($(date +%s)-$start)/60))
				echo $bamfile >> $tmp_dide/list-finished.lst;
				
				echo "Sort finished, for $label finished in $runtime minutes." 2>&1 | tee -a $tmp_clog/bismark-sorting.log
				totaltime=$(($runtime + $totaltime))
			done
	echo "Sort finished. Total time $totaltime minutes."  2>&1 | tee -a $tmp_clog/bismark-sorting.log
	echo "You can find the result in $tmp_dide folder." 

fi



if [ -f $tmp_dide/tmp.lst ]
then 
	remove=$(rm $tmp_dide/tmp.lst)
fi

# check if everyfiles done then delete queue list 
if [ -z $(comm -23 <(sort -u $tmp_dide/list-files.lst) <(sort -u $tmp_dide/list-finished.lst)) ]  
then
	com=$(sed -i "s/st_bissort=.*/st_bissort=2/g" config/pipeline.conf)
	remove=$(rm $tmp_dide/list-finished.lst)
fi
