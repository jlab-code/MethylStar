#!/bin/bash
curr_dir="$(dirname "$0")"
com1=$(awk '/^\[/ { } /=/ { print $0 }' config/pipeline.conf > $curr_dir/tmp.conf)
. $curr_dir/tmp.conf
. $curr_dir/detect.sh  $genome_type  qcFast $npar;
. $curr_dir/tmp.conf

: '
Generate Coverage report and sequencing depth.
'
if [ `ls $tmp_covseq/*temp* 2>/dev/null | wc -l ` -gt 0   ]
then 
	remove=$(rm $tmp_covseq/*temp*)
fi


if [ "$1" = "mapper" ]
then
		fileName=BismarkMapper
else
		fileName=BismarkDeduplicate
fi

#echo -e "Generating report for $fileName part \n" >> $tmp_covseq/$fileName-report.log
#generating up-to-date list of files
gen=$(ls -1v $tmp_covseq/sorted-*.bam > $tmp_covseq/list-files.lst)

if [ -f $tmp_covseq/list-finished.lst ]
	then
		echo -e "\nResuming coverage  ..." 
		a_proc= $(sort $tmp_covseq/list-files.lst -o $tmp_covseq/list-files.lst)
		b_proc= $(sort $tmp_covseq/list-finished.lst -o $tmp_covseq/list-finished.lst)
		c_proc= $(comm -23 $tmp_covseq/list-files.lst $tmp_covseq/list-finished.lst > $tmp_covseq/tmp.lst)
		#running main prog
		input="$tmp_covseq/tmp.lst"
		while read line
			do
				arr+=("$line")
			done < $input;
	else
		echo -e "\nStarting to calculate sequencing depth and coverage ..." 
		input="$tmp_covseq/list-files.lst"
		while read line
		do
			arr+=("$line")
		done < $input;
fi
# running main prog
#--------------------------------------------------------

if $parallel_mode; then
	#running in parallel mode
	echo -e "Running in Parallel mode, number of jobs: $npar .\n" 
	start=$(date +%s)
	doit() {
		. "$1"
		label=$(echo $(echo $2 |sed 's/.*\///') | sed -e 's/.bam//g')
		echo "-- Running genome coverage and sequencing depth for $label ..." 2>&1 | tee -a $tmp_clog/covseq.log
		gen_size=$(samtools view -H $2  | grep -P '^@SQ' | cut -f 3 -d ':' | awk '{sum+=$1} END {print sum}')
		cmd=$(samtools depth $2 | awk -v gen="$gen_size" '{sum+=$3} END {print "Average sequencing depth(X) = ",sum/gen}')
		echo "# $cmd" 
		#calculating genome coverage
		gencov=$(bedtools genomecov -ibam $2 -bga -g $tmp_rdata/*_chr_all.txt | awk -v gen="$gen_size" '{if($4>0) total += ($3-$2)} END {print "Genome coverage (%) = ", total/gen * 100}')
		echo "# ${gencov}" 

		echo "file: " $label >> $tmp_covseq/$fileName-report.log
		echo "# $cmd" >> $tmp_covseq/$fileName-report.log 
		echo "# $gencov "  >> $tmp_covseq/$fileName-report.log
		echo "---------------------------------" >> $tmp_covseq/$fileName-report.log
		echo "$2" >> $tmp_covseq/list-finished.lst;
		echo -e "---------------------------------\n"

	}
	export -f doit
	par=$(echo $curr_dir/tmp.conf) 
	cat  "$input"  | parallel -j $npar  doit "$par"
	runtime=$((($(date +%s)-$start)/60))
	echo "Reports finished. Total time $runtime minutes." 2>&1 | tee -a $tmp_clog/covseq.log
	echo -e "\nYou can find the result in $tmp_covseq/$fileName-report.log"
else
#running in single mode
	echo -e "Running in single mode!(parallel disabled.) \n"  
	totaltime=0
	for file in "${arr[@]}"
		do
			start=$(date +%s)
			label=$(echo $(echo $file |sed 's/.*\///') | sed -e 's/.bam//g')
			echo "-- Running genome coverage and sequencing depth $label ..." 2>&1 | tee -a $tmp_clog/covseq.log

			gen_size=$(samtools view -H $file  | grep -P '^@SQ' | cut -f 3 -d ':' | awk '{sum+=$1} END {print sum}')
			cmd=$(samtools depth $file | awk -v gen="$gen_size" '{sum+=$3} END {print "Average sequencing depth(X) = ",sum/gen}')
			echo "# $cmd" 
			#calculating genome coverage
			gencov=$(bedtools genomecov -ibam $file -bga -g $tmp_rdata/*_chr_all.txt | awk -v gen="$gen_size" '{if($4>0) total += ($3-$2)} END {print "Genome coverage (%) = ", total/gen * 100}')
			echo "# ${gencov}" 
			echo "file: " $label >> $tmp_covseq/$fileName-report.log
			echo "# $cmd" >> $tmp_covseq/$fileName-report.log
			echo "# $gencov "  >> $tmp_covseq/$fileName-report.log
			echo "---------------------------------" >> $tmp_covseq/$fileName-report.log
			echo $file >> $tmp_covseq/list-finished.lst;
			runtime=$((($(date +%s)-$start)/60))
			echo "Task finished for $label in $runtime minutes."  2>&1 | tee -a $tmp_clog/covseq.log
			echo -e "---------------------------------"
			totaltime=$(($runtime + $totaltime))
		done
	echo "Reports finished. Total time $totaltime minutes."  >> $tmp_clog/covseq.log
	echo -e "\n You can find the result in $tmp_covseq/$fileName-report.log" 
fi


if [ -f $tmp_covseq/tmp.lst ]
then 
	remove=$(rm $tmp_covseq/tmp.lst)
fi

# check if everyfiles done then delete queue list 
if [ -z $(comm -23 <(sort -u $tmp_covseq/list-files.lst) <(sort -u $tmp_covseq/list-finished.lst)) ] 
then
	com=$(sed -i "s/st_coreport=.*/st_coreport=2/g" config/pipeline.conf)

	if [ "$quickrun" = "0" ]
	then
	rem=$(rm $tmp_covseq/sorted*.bam)
	fi
	remove=$(rm $tmp_covseq/list-finished.lst)
fi


if [ -f $tmp_covseq/"-report.log" ]
then 
	remove=$(mv $tmp_covseq/"-report.log" $tmp_covseq/$fileName-report.log )
fi

# docker part 
if $docker_mode; 
then
	perm=$(chmod 777 -R $result_pipeline)
fi