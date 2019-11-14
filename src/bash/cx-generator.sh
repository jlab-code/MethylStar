#!/bin/bash
curr_dir="$(dirname "$0")"
com1=$(awk '/^\[/ { } /=/ { print $0 }' config/pipeline.conf > $curr_dir/tmp.conf)
. $curr_dir/tmp.conf
. $curr_dir/detect.sh  $genome_type  qcFast $npar;
. $curr_dir/tmp.conf


: '

run bismark deduplicate &
run bismark_methylation_extractor: atypical command to extract context-dependent (CpG/CHG/CHH) methylation
'
#-------------------------------------------------------------------------------
#generating up-to-date list of files
gen=$(ls -1v $tmp_dme/*.cov.gz > $tmp_cx_report/list-files.lst)

if [ -f $tmp_cx_report/list-finished.lst ]
	then
		echo "Resuming process ..."  >> $tmp_clog/cx-report.log
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
		echo "Starting CX-report ..." > $tmp_clog/cx-report.log
		input="$tmp_cx_report/list-files.lst"
		while read line
		do
			arr+=("$line")
		done < $input;
	fi


if $parallel_mode; then
			#running in parallel mode
			echo "Running in Parallel mode, number of jobs: $npar ." >>  $tmp_clog/cx-report.log
			start=$(date +%s)
			doit() {
				. "$1"
				tmp=$(echo "$2" | sed 's/.*\///')
				label=$(echo ${tmp%%.*})
				echo "Generating cx-report for $label" >>  $tmp_clog/cx-report.log
				cmd=$($bismark_path/coverage2cytosine --CX_context --genome_folder $genome_ref --output $tmp_cx_report/$label.CX_report.txt  "$2" )
				echo $2 >> $tmp_cx_report/list-finished.lst   
			}
			export -f doit
			par=$(echo $curr_dir/tmp.conf) 
			cat  "$input"  | parallel -j $npar doit "$par"
			runtime=$((($(date +%s)-$start)/60))
			echo "CX-reports generated . Total time $runtime minutes." >> $tmp_clog/cx-report.log
			echo "You can find the result in $tmp_cx_report folder." >> $tmp_clog/cx-report.log				
	else
			echo "Running in single mode.(Parallel mode disabled.)"  >> $tmp_clog/cx-report.log	
			totaltime=0
			for cx in "${arr[@]}"
			do
				start=$(date +%s)
				tmp=$(echo $cx | sed 's/.*\///')
				label=$(echo ${tmp%%.*})
				echo "Generating cx-report for $label" >>  $tmp_clog/cx-report.log
				run_cx=$($bismark_path/coverage2cytosine --CX_context --genome_folder $genome_ref --output $tmp_cx_report/$label.CX_report.txt  $cx)
				echo $cx >> $tmp_cx_report/list-finished.lst;
				runtime=$((($(date +%s)-$start)/60))
				echo "CX report for $label finished in $runtime minutes."  >> $tmp_clog/cx-report.log
				totaltime=$(($runtime + $totaltime))
			done;
			echo "CX-reports generated . Total time $totaltime minutes." >> $tmp_clog/cx-report.log
			echo "You can find the result in $tmp_cx_report folder." >> $tmp_clog/cx-report.log
	fi


if [ -f $tmp_cx_report/tmp.lst ]
then 
	remove=$(rm $tmp_cx_report/tmp.lst)
fi

# check if everyfiles done then delete queue list 
if [ -z $(comm -23 <(sort -u $tmp_cx_report/list-files.lst) <(sort -u $tmp_cx_report/list-finished.lst)) ]  
then
	com=$(sed -i "s/st_cx=.*/st_cx=2/g" config/pipeline.conf)
	remove=$(rm $tmp_cx_report/list-finished.lst)
fi
# docker part 
if $docker_mode; 
then
	perm=$(chmod 777 -R $result_pipeline)
fi