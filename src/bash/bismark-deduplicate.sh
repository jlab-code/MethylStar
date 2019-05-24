#!/bin/bash
curr_dir="$(dirname "$0")"
com1=$(awk '/^\[/ { } /=/ { print $0 }' config/pipeline.conf > $curr_dir/tmp.conf)
. $curr_dir/tmp.conf


: '

run bismark deduplicate &
run bismark_methylation_extractor: atypical command to extract context-dependent (CpG/CHG/CHH) methylation
'

#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------

# check point
gen=$(ls -1v $tmp_bismap/*.bam > $tmp_dide/list-files.lst)

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
		echo "Starting Bismark Deduplication ..." 
		input="$tmp_dide/list-files.lst"
		while read line
		do
			arr+=("$line")
		done < $input;
	fi


if $parallel_mode; then
		echo "Running in Parallel mode, number of jobs: $npar ." 
		start=$(date +%s)
		doit() {
				. "$1"
				label=$(echo $(echo "$2" | sed 's/.*\///') | sed -e 's/.bam//g')						
				# Sleep up to 10 seconds
				echo ""
				echo "Running Bismark deduplication report for $label ..." 2>&1 | tee -a $tmp_clog/bismark-deduplicate.log
				ded=$($bismark_path/deduplicate_bismark $deduplicate --bam  "$2" --output_dir $tmp_dide/ 2>&1 | tee -a $tmp_dide/$label.log )
				echo $2 >> $tmp_dide/list-finished.lst;   
				sed -n -e 15p  -e 18,22p $tmp_dide/$label.log
		}
		export -f doit
		par=$(echo $curr_dir/tmp.conf) 
		cat  "$input"  | parallel -j $npar doit "$par"
		runtime=$((($(date +%s)-$start)/60))
		echo "Bismark Deduplication finished. Total time $runtime minutes." 2>&1 | tee -a $tmp_clog/bismark-deduplicate.log
		echo "You can find the result in $tmp_dide folder."

else
	#running in single mode
	echo "Running in single mode!"  
	totaltime=0
	for bamfile in "${arr[@]}"
			do
				start=$(date +%s)
				label=$(echo $(echo $bamfile | sed 's/.*\///') | sed -e 's/.bam//g')
				echo ""
				echo "Running Bismark deduplication report for $label ..." 
				ded=$($bismark_path/deduplicate_bismark	$deduplicate --bam $bamfile --output_dir $tmp_dide/ 2>&1 | tee -a $tmp_dide/$label.log)
				runtime=$((($(date +%s)-$start)/60))
				echo $bamfile >> $tmp_dide/list-finished.lst;
				sed -n -e 15p  -e 18,22p $tmp_dide/$label.log;
				echo "Bismark Deduplication for $label finished in $runtime minutes." 2>&1 | tee -a $tmp_clog/bismark-deduplicate.log
				totaltime=$(($runtime + $totaltime))
			done
	echo "Bismark Deduplication finished. Total time $totaltime minutes."  2>&1 | tee -a $tmp_clog/bismark-deduplicate.log
	echo "You can find the result in $tmp_dide folder." 

fi

#------------------------------------ Renaming
for file in $(ls -1v $tmp_dide/*.bam)
	do
		label=$(echo $(echo $file | sed 's/.*\///') | sed -e "s/.deduplicated.bam//g")
		mv $file $tmp_dide/$label.bam
	done
# rename logs to fq
for file in $(ls -1v $tmp_dide/*.txt)
	do
		label=$(echo $(echo $file | sed 's/.*\///') | sed -e "s/.deduplication_report.txt//g")
		mv $file $tmp_dide/$label.txt
	done
#--------------------------------------

: '
for file in $(ls -1v $tmp_dide/*.bam.log)
	do
		label=$(echo $(echo $file | sed 's/.*\///') | sed -e 's/.bam.log//g')
		mv $file $tmp_dide/$label.log

	done

'

if [ -f $tmp_dide/tmp.lst ]
then 
	remove=$(rm $tmp_dide/tmp.lst)
fi

# check if everyfiles done then delete queue list 
if [ -z $(comm -23 <(sort -u $tmp_dide/list-files.lst) <(sort -u $tmp_dide/list-finished.lst)) ]  
then
	com=$(sed -i "s/st_bisdedup=.*/st_bisdedup=2/g" config/pipeline.conf)
	remove=$(rm $tmp_dide/list-finished.lst)
fi
# docker part 
if $docker_mode; 
then
	perm=$(chmod 777 -R $result_pipeline)
fi