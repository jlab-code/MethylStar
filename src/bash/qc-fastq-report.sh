#!/bin/bash
curr_dir="$(dirname "$0")"
com1=$(awk '/^\[/ { } /=/ { print $0 }' config/pipeline.conf > $curr_dir/tmp.conf)
. $curr_dir/tmp.conf
. $curr_dir/detect.sh  $genome_type  qcFast $npar;
. $curr_dir/tmp.conf

: '
Generating FastQC reports.
'

#generating up-to-date list of files
gen=$(ls -1v $tmp_fq/*.gz > $tmp_qcfast/list-files.lst)

if [ -f $tmp_qcfast/list-finished.lst ]
	then
		echo -e "\nResuming process ..." 
		a_proc= $(sort $tmp_qcfast/list-files.lst -o $tmp_qcfast/list-files.lst)
		b_proc= $(sort $tmp_qcfast/list-finished.lst -o $tmp_qcfast/list-finished.lst)
		c_proc= $(comm -23 $tmp_qcfast/list-files.lst $tmp_qcfast/list-finished.lst > $tmp_qcfast/tmp.lst)
		#running main prog
		input="$tmp_qcfast/tmp.lst"
		while read line
			do
				arr+=("$line")
			done < $input;
	else
		echo -e "\nStarting Fasqc-report ..." 
		input="$tmp_qcfast/list-files.lst"
		while read line
		do
			arr+=("$line")
		done < $input;
fi
# running main prog
#--------------------------------------------------------
if $parallel_mode; then
	#running in parallel mode
	start=$(date +%s)
	echo "Running in Parallel mode, number of jobs: $npar " 2>&1 | tee -a $tmp_clog/qc-fastq.log
	doit() {

		. "$1"
		label=$(echo $(echo $2 |sed 's/.*\///') | sed -e 's/.fq.gz//g')
		echo "Running fastQC report for $label ..." 
		fast=$($fastq_path --noextract -f fastq $2 -o $tmp_qcfast)
		echo $2 >> $tmp_qcfast/list-finished.lst;
	}
	export -f doit
	par=$(echo $curr_dir/tmp.conf) 
	cat  "$input"  | parallel -j $npar doit "$par"
	end=$(date +%s)
	runtime=$((($(date +%s)-$start)/60))
	echo "FastqC report finished. Duration $runtime Minutes." 2>&1 | tee -a $tmp_clog/qc-fastq.log;
	echo -e "You can find the results in $tmp_qcfast folder. \n"

else
#running in single mode
	echo -e "Running in single mode. (parallel mode disabled.) \n"
	start=$(date +%s)
	for fq in "${arr[@]}"
		do
		# get file name -extension
		label=$(echo $(echo $fq |sed 's/.*\///') | sed -e 's/.fq.gz//g')
		echo "Running fastQC report for $label ..." 2>&1 | tee -a $tmp_clog/qc-fastq.log
		fast=$($fastq_path --noextract -f fastq $fq -o $tmp_qcfast)
		echo $fq >> $tmp_qcfast/list-finished.lst
		echo -e "\n"
		done
	end=$(date +%s)
	runtime=$((($(date +%s)-$start)/60))
	echo "QC report finished in $runtime minutes." 2>&1 | tee -a $tmp_clog/qc-fastq.log
	echo -e "You can find the results in $tmp_qcfast folder. \n "
	

fi

if [ -f $tmp_qcfast/tmp.lst ]
then 
	remove=$(rm $tmp_qcfast/tmp.lst)
fi



# check if everyfiles done then delete queue list 
if [ -z $(comm -23 <(sort -u $tmp_qcfast/list-files.lst) <(sort -u $tmp_qcfast/list-finished.lst)) ]  
then
	com=$(sed -i "s/st_fastq=.*/st_fastq=2/g" config/pipeline.conf)
	remove=$(rm $tmp_qcfast/list-finished.lst)
fi


# docker part 
if $docker_mode; 
then
	perm=$(chmod 777 -R $result_pipeline)
fi