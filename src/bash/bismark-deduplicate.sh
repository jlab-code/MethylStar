#!/bin/bash
curr_dir="$(dirname "$0")"
com1=$(awk '/^\[/ { } /=/ { print $0 }' config/pipeline.conf > $curr_dir/tmp.conf)
. $curr_dir/tmp.conf


: '

run bismark deduplicate &
run bismark_methylation_extractor: atypical command to extract context-dependent (CpG/CHG/CHH) methylation
'


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

		input="$tmp_dide/list-files.lst"
		while read line
		do
			arr+=("$line")
		done < $input;
	fi
#-------------------------------------------------------------------------------


if $parallel_mode; then
	
		doit() {
				. "$1"

				label=$(echo $(echo "$2" | sed 's/.*\///') | sed -e 's/.bam//g')						
				# Sleep up to 10 seconds
				ded=$($bismark_path/deduplicate_bismark $deduplicate --bam  "$2" --output_dir $tmp_dide/ 2>&1 | tee -a $tmp_dide/$label.log )
				echo $2 >> $tmp_dide/list-finished.lst;   
				echo "---------------------------------------" 
				sed -n -e 15p  -e 18,22p $tmp_dide/$label.log
		}
		export -f doit
		par=$(echo $curr_dir/tmp.conf) 
		cat  "$input"  | parallel -j $npar doit "$par"


else
	#running in single mode
	echo "running in single mode!"
	for bamfile in "${arr[@]}"
			do
				start=$(date +%s)
				label=$(echo $(echo $bamfile | sed 's/.*\///') | sed -e 's/.bam//g')
				#ded=$($bismark_path/deduplicate_bismark	$deduplicate --bam $bamfile --output_dir $tmp_dide/ 2>&1 | tee -a $tmp_dide/$label.log)
				end=$(date +%s)
				runtime=$((($(date +%s)-$start)/60))
				echo $bamfile >> $tmp_dide/list-finished.lst;
				echo "---------------------------------------" 
				sed -n -e 15p  -e 18,22p $tmp_dide/$label.log
				

			done

fi

if [ -f $tmp_dide/tmp.lst ]
then 
	remove=$(rm $tmp_dide/tmp.lst)
fi
: '
for file in $(ls -1v $tmp_dide/*.bam.log)
	do
		label=$(echo $(echo $file | sed 's/.*\///') | sed -e 's/.bam.log//g')
		mv $file $tmp_dide/$label.log

	done

'