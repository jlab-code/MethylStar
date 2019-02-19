#!/bin/bash
curr_dir="$(dirname "$0")"
com1=$(awk '/^\[/ { } /=/ { print $0 }' config/pipeline.conf > $curr_dir/tmp.conf)
. $curr_dir/tmp.conf


: '

run bismark deduplicate &
run bismark_methylation_extractor: atypical command to extract context-dependent (CpG/CHG/CHH) methylation
'

#-------------------------------------------------------------------------------
# Detecting number of cores 
npar=$(cat /proc/cpuinfo | awk '/^processor/{print $3}' | wc -l)
var=$(expr $npar / 22)
npar=$(echo $var|awk '{print int($1+0.5)}')
if [ $npar -eq 0 ]; then
        npar=1;
fi
#-------------------------------------------------------------------------------
#generating up-to-date list of files
gen=$(ls -1v $tmp_dide/*.bam > $tmp_dme/list-files.lst)

if [ -f $tmp_dme/list-finished.lst ]
	then
		echo "Resuming process ..." >> $tmp_clog/bismark-meth-extract.log
		a_proc= $(sort $tmp_dme/list-files.lst -o $tmp_dme/list-files.lst)
		b_proc= $(sort $tmp_dme/list-finished.lst -o $tmp_dme/list-finished.lst)
		c_proc= $(comm -23 $tmp_dme/list-files.lst $tmp_dme/list-finished.lst > $tmp_dme/tmp.lst)
		#running main prog
		input="$tmp_dme/tmp.lst"
		 while read line
		 	do
		 		arr+=("$line")
		 done < $input;
	else
		echo "Starting Bismark methylation extractor ..." > $tmp_clog/bismark-meth-extract.log
		input="$tmp_dme/list-files.lst"								  
		 while read line
		 do
		 	arr+=("$line")
		 done < $input;
fi
#-------------------------------------------------------------------------------

if $parallel_mode; then 
	echo "Running Bismark Mapper in Parallel mode, number of jobs that proccessing at same time: $npar ." >> $tmp_clog/bismark-meth-extract.log;
	start=$(date +%s)
	doit() {
			. "$1"
			echo "Running Bismark meth extractor for $2" >> $tmp_clog/bismark-meth-extract.log
			tmp=$(echo $2 | sed 's/.*\///')
			label=$(echo ${tmp%%.*})
	        bis_extractor=$($bismark_path/bismark_methylation_extractor $deduplicate  --bedGraph --CX --cytosine_report --parallel $bis_parallel --buffer_size $buf_size"G" --genome_folder $genome_ref $2 -o $tmp_dme/ 2>&1 | tee -a $tmp_dme/$label.log )
			cat  $tmp_dme/$label.deduplicated_splitting_report.txt >> $tmp_clog/bismark-meth-extract.log
			echo $2 >> $tmp_dme/list-finished.lst;
			echo "Moving Cx-reports to the $tmp_cx_report folder." >> $tmp_clog/bismark-meth-extract.log
			comm=$(mv $tmp_dme/*.CX_report.txt $tmp_cx_report/)
			if $del_inter_file; then
				echo "Removing intermediate files... " >> $tmp_clog/bismark-meth-extract.log
				remove_intermediate=$(rm $tmp_dme/*$label*.txt)
			fi	

	}
	export -f doit
	par=$(echo $curr_dir/tmp.conf)
	cat  "$input"  | parallel -j $npar doit "$par"
	runtime=$((($(date +%s)-$start)/60))
	echo "Bismark meth extractor finished. Duration time $runtime Minutes." >> $tmp_clog/bismark-meth-extract.log

else
	totaltime=0
	for bm in "${arr[@]}"
		do
			start=$(date +%s)
			echo "Running Bismark meth extractor for $bm" >> $tmp_clog/bismark-meth-extract.log
			tmp=$(echo $bm | sed 's/.*\///')
			label=$(echo ${tmp%%.*})
	        bis_extractor=$($bismark_path/bismark_methylation_extractor $deduplicate  --bedGraph --CX --cytosine_report --parallel $bis_parallel --buffer_size $buf_size"G" --genome_folder $genome_ref $bm -o $tmp_dme/ 2>&1 | tee -a $tmp_dme/$label.log )
			cat  $tmp_dme/$label.deduplicated_splitting_report.txt >> $tmp_clog/bismark-meth-extract.log
			echo $bm >> $tmp_dme/list-finished.lst;
			echo "Moving Cx-reports to the $tmp_cx_report folder." >> $tmp_clog/bismark-meth-extract.log
			comm=$(mv $tmp_dme/*.CX_report.txt $tmp_cx_report/)
			if $del_inter_file; then
				echo "Removing intermediate files... " >> $tmp_clog/bismark-meth-extract.log
				remove_intermediate=$(rm $tmp_dme/*$label*.txt)
			fi
			runtime=$((($(date +%s)-$start)/60))
			echo "Bismark meth extractor for $label finished in $runtime minutes." >> $tmp_clog/bismark-meth-extract.log
			totaltime=$(($runtime + $totaltime))
	done;
	echo "Bismark meth extractor finished. Total time $totaltime minutes."  >> $tmp_clog/bismark-meth-extract.log
	echo "You can find the result in $tmp_dme folder." >> $tmp_clog/bismark-meth-extract.log
fi


if [ -f $tmp_dme/tmp.lst ]
then 
	remove=$(rm $tmp_dme/tmp.lst)
fi

sed -i "s/st_bismeth=.*/st_bismeth=3/g" config/pipeline.conf

if [ -f $tmp_dme/list-finished.lst ]
then 
	remove=$(rm $tmp_dme/list-finished.lst)
fi

