#!/bin/bash
curr_dir="$(dirname "$0")"
com1=$(awk '/^\[/ { } /=/ { print $0 }' config/pipeline.conf > $curr_dir/tmp.conf)
. $curr_dir/tmp.conf


: '
Generate QC report using FastQC for the Bismark-aligned bam files.
'

#generating up-to-date list of files
gen=$(ls -1v $tmp_bismap/*.bam > $tmp_qcbam/list-files.lst)

if [ -f $tmp_qcbam/list-finished.lst ]
	then
		echo "Resuming process ..."
		a_proc= $(sort $tmp_qcbam/list-files.lst -o $tmp_qcbam/list-files.lst)
		b_proc= $(sort $tmp_qcbam/list-finished.lst -o $tmp_qcbam/list-finished.lst)
		c_proc= $(comm -23 $tmp_qcbam/list-files.lst $tmp_qcbam/list-finished.lst > $tmp_qcbam/tmp.lst)
		#running main prog
		input="$tmp_qcbam/tmp.lst"
		while read line
			do
				arr+=("$line")
			done < $input;
	else
		input="$tmp_qcbam/list-files.lst"
		while read line
		do
			arr+=("$line")
		done < $input;
fi
# running main prog
#--------------------------------------------------------

if $parallel_mode; then
	#running in parallel mode
		echo "Running in Parallel mode, number of jobs: $npar ."
		start=$(date +%s)
		doit() {
			. "$1"
			label=$(echo $(echo $2 |sed 's/.*\///') | sed -e 's/.fq.gz//g')
			echo "Running fastQC report for $label ..."
			fast=$($fastq_path --noextract -f bam $2 -o $tmp_qcbam)
			echo $2 >> $tmp_qcbam/list-finished.lst;
		}
		export -f doit
		par=$(echo $curr_dir/tmp.conf) 
		cat  "$input"  | parallel -j $npar doit "$par"
		end=$(date +%s)
		runtime=$((($(date +%s)-$start)/60))
		echo "QC report for $label finished in $runtime minutes."
else
#running in single mode
	echo "running in single mode!"
	start=$(date +%s)
	for fq in "${arr[@]}"
		do
			# get file name -extension
			label=$(echo $(echo $fq |sed 's/.*\///') | sed -e 's/.fq.gz//g')
			echo "Running fastQC report for $label ..."
			fast=$($fastq_path --noextract -f bam $fq -o $tmp_qcbam)
			echo $fq >> $tmp_qcbam/list-finished.lst;
		done
		end=$(date +%s)
		runtime=$((($(date +%s)-$start)/60))
		echo "QC report for $label finished in $runtime minutes."
fi


if [ -f $tmp_qcbam/tmp.lst ]
then 
	remove=$(rm $tmp_qcbam/tmp.lst)
fi