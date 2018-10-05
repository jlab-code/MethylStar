#!/bin/bash
curr_dir="$(dirname "$0")"
com1=$(awk '/^\[/ { } /=/ { print $0 }' config/pipeline.conf > $curr_dir/tmp.conf)
. $curr_dir/tmp.conf


: '

run bismark deduplicate &
run bismark_methylation_extractor: atypical command to extract context-dependent (CpG/CHG/CHH) methylation
'
#generating up-to-date list of files
gen=$(ls -1v $tmp_dme/*.cov.gz > $tmp_cx_report/list-files.lst)

if [ -f $tmp_cx_report/list-finished.lst ]
	then
		echo "Resuming process ..."
		a_proc= $(sort $tmp_cx_report/list-files.lst -o $tmp_cx_report/list-files.lst)
		b_proc= $(sort $tmp_cx_report/list-finished.lst -o $tmp_cx_report/list-finished.lst)
		c_proc= $(comm -23 $tmp_cx_report/list-files.lst $tmp_cx_report/list-finished.lst > $tmp_cx_report/tmp.lst)
		#running main prog
		input="$tmp_cx_report/tmp.lst"
		while read line
			do
				arr+=("$line")
		done < $input;
	else
		input="$tmp_cx_report/list-files.lst"
		while read line
		do
			arr+=("$line")
		done < $input;
	fi


if $parallel_mode; then
			#running in parallel mode
			echo "Running in Parallel mode, number of jobs: $npar ."

			doit() {
				. "$1"
				tmp=$(echo "$2" | sed 's/.*\///')
				label=$(echo ${tmp%%.*})
				cmd=$($bismark_path/coverage2cytosine --CX_context --genome_folder $genome_ref --output $tmp_cx_report/$label.CX_report.txt  "$2" )
				echo $2 >> $tmp_cx_report/list-finished.lst   
			}
			export -f doit
			par=$(echo $curr_dir/tmp.conf) 
			cat  "$input"  | parallel -j $npar doit "$par"
						
						

	else
			for cx in "${arr[@]}"
			do
				echo $cx;
				tmp=$(echo $cx | sed 's/.*\///')
				label=$(echo ${tmp%%.*})
				run_cx=$($bismark_path/coverage2cytosine --CX_context --genome_folder $genome_ref --output $tmp_cx_report/$label.CX_report.txt  $cx)
				echo $cx >> $tmp_cx_report/list-finished.lst;
			done;
	fi


if [ -f $tmp_cx_report/tmp.lst ]
then 
	remove=$(rm $tmp_cx_report/tmp.lst)
fi

