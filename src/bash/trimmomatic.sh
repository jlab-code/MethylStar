#!/bin/bash
curr_dir="$(dirname "$0")"
com1=$(awk '/^\[/ { } /=/ { print $0 }' config/pipeline.conf > $curr_dir/tmp.conf)
. $curr_dir/tmp.conf


#---------------------------------------------------------------
# check point

if [ -f $tmp_fq/list-finished.lst ]
	then
		echo "Resuming process ..." >> $tmp_clog/trimmomatic.log
		proc_a= $(sort $tmp_fq/list-files.lst -o $tmp_fq/list-files.lst)
		proc_b= $(sort $tmp_fq/list-finished.lst -o $tmp_fq/list-finished.lst)
		proc_c= $(comm -23 $tmp_fq/list-files.lst $tmp_fq/list-finished.lst > $tmp_fq/tmp.lst)
		input="$tmp_fq/tmp.lst"
		while read line
			do
				arr+=("$line")
			done < $input;
	else
		echo "Starting Trimmomatic ..." > $tmp_clog/trimmomatic.log
		input="$tmp_fq/list-files.lst"
		while read line
		do
			arr+=("$line")
		done < $input;
	fi
#---------------------------------------------------------------

#---------------------------------------------------------------
# running main prog
if $parallel_mode; then
	
	echo "Running in Parallel mode, number of jobs that proccessing at same time: $npar ." >> $tmp_clog/trimmomatic.log;
	start=$(date +%s)
	doit() {
					
		. "$1"              
		tmp=$(echo $2| sed 's/.*\///')
		label=$(echo ${tmp%%.*})
		echo  "Running ..." $label >> $tmp_clog/trimmomatic.log;
		run=$($java_path -jar $trim_jar $end_mode -threads $n_th -phred33  $2 $tmp_fq/$label.fq.gz ILLUMINACLIP:$name_adap:$ill_clip LEADING:$LEADING TRAILING:$TRAILING SLIDINGWINDOW:$SLIDINGWINDOW MINLEN:$MINLEN 2>&1 | tee  $tmp_log/trimmomatic-log-$label.log)
		
		getinfo=$(echo $(sed -n -e 5p $tmp_log/trimmomatic-log-$label.log))
		echo $label ":" $getinfo >> $tmp_clog/trimmomatic.log;
		echo $2 >> $tmp_fq/list-finished.lst;
								   
		}
	export -f doit
	par=$(echo $curr_dir/tmp.conf) 
	cat "$input"  | parallel -j $npar doit "$par"
	runtime=$((($(date +%s)-$start)/60)) 
	echo "Trimmomatic finished. Duration $runtime Minutes." >> $tmp_clog/trimmomatic.log;
						
else
	
	totaltime=0	
	for file in "${arr[@]}"
		do
			start=$(date +%s)
			echo "Running Trimmomatic for " $file >> $tmp_clog/trimmomatic.log;
			tmp=$(echo $file| sed 's/.*\///')
			label=$(echo ${tmp%%.*})
			run=$($java_path -jar $trim_jar $end_mode -threads $n_th -phred33  $file $tmp_fq/$label.fq.gz ILLUMINACLIP:$name_adap:$ill_clip LEADING:$LEADING TRAILING:$TRAILING SLIDINGWINDOW:$SLIDINGWINDOW MINLEN:$MINLEN 2>&1 | tee $tmp_log/trimmomatic-log-$label.log)
			getinfo=$(echo $(sed -n -e 5p $tmp_log/trimmomatic-log-$label.log))
			echo $label ":" $getinfo >> $tmp_clog/trimmomatic.log;
			echo $file >> $tmp_fq/list-finished.lst;
			runtime=$((($(date +%s)-$start)/60))
			echo "Trimmomatic finished. Duration $runtime Minutes." >> $tmp_clog/trimmomatic.log;
			totaltime=$(($runtime + $totaltime))
		done;
		echo "Trimmomatic finished. Total time $totaltime Minutes." >> $tmp_clog/trimmomatic.log;

fi

if [ -f $tmp_fq/tmp.lst ]
then 
	remove=$(rm $tmp_fq/tmp.lst)
fi

sed -i "s/st_trim=.*/st_trim=3/g" config/pipeline.conf

if [ -f $tmp_fq/list-finished.lst ]
then 
	remove=$(rm $tmp_fq/list-finished.lst)
fi