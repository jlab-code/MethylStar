#!/bin/bash
curr_dir="$(dirname "$0")"
com1=$(awk '/^\[/ { } /=/ { print $0 }' config/pipeline.conf > $curr_dir/tmp.conf)
. $curr_dir/tmp.conf



#-------------------------------------------------------------------------------
# check point

if [ -f $tmp_fq/list-finished.lst ]
	then
		echo "Resuming process ..."  >> $tmp_clog/trimmomatic.log
		proc_a= $(sort $tmp_fq/list-files.lst -o $tmp_fq/list-files.lst)
		proc_b= $(sort $tmp_fq/list-finished.lst -o $tmp_fq/list-finished.lst)
		proc_c= $(comm -23 $tmp_fq/list-files.lst $tmp_fq/list-finished.lst > $tmp_fq/tmp.lst)
		input="$tmp_fq/tmp.lst"
	else
		input="$tmp_fq/list-files.lst"
		echo "Starting Trimmomatic ..." > $tmp_clog/trimmomatic.log

	fi
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

if $parallel_mode; then

	echo "Running in Parallel mode, number of jobs that proccessing at same time: $npar ." >> $tmp_clog/trimmomatic.log;
	start=$(date +%s)
	doit() {

		. "$1"

		label=$(echo $(echo $2 | sed 's/.*\///') | sed -e "s/$first_pattern//g")
		path=$(echo $(echo $2 | sed -e 's:[^/]*$::'))
		first_file=$label"$first_pattern"
		second_file=$label"$secnd_pattern"
		echo  "Running ... "$first_file " and " $second_file >> $tmp_clog/trimmomatic.log;

		run=$($java_path -jar $trim_jar $end_mode -threads $n_th -phred33  $path$first_file $path$second_file $tmp_fq/$label"_paired"$first_pattern $tmp_fq/$label"_unpaired"$first_pattern $tmp_fq/$label"_paired"$secnd_pattern $tmp_fq/$label"_unpaired"$secnd_pattern ILLUMINACLIP:$name_adap:$ill_clip LEADING:$LEADING TRAILING:$TRAILING SLIDINGWINDOW:$SLIDINGWINDOW MINLEN:$MINLEN 2>&1 | tee $tmp_log/trimmomatic-log-$label.log )

		getinfo=$(echo $(sed -n -e 5p $tmp_log/trimmomatic-log-$label.log))
		echo  $label ":" $getinfo >> $tmp_clog/trimmomatic.log;

		echo $path$first_file >> $tmp_fq/list-finished.lst;
		echo $path$second_file >> $tmp_fq/list-finished.lst;
								   
		}

	export -f doit
	par=$(echo $curr_dir/tmp.conf) 
	grep "$first_pattern" "$input"  | parallel -j $npar doit "$par"
	runtime=$((($(date +%s)-$start)/60))
	echo "Trimmomatic finished. Duration $runtime Minutes." >> $tmp_clog/trimmomatic.log;
	

else
	totaltime=0
	for file in $(grep $first_pattern $input)
		do
			start=$(date +%s) 
			# get file name -extension
			label=$(echo $(echo $file | sed 's/.*\///') | sed -e "s/$first_pattern//g")
			path=$(echo $(echo $file | sed -e 's:[^/]*$::'))
			first_file=$label"$first_pattern"
			second_file=$label"$secnd_pattern"
			echo  "Running ... "$first_file " and " $second_file >> $tmp_clog/trimmomatic.log;
			run=$($java_path -jar $trim_jar $end_mode -threads $n_th -phred33  $path$first_file $path$second_file $tmp_fq/$label"_paired"$first_pattern $tmp_fq/$label"_unpaired"$first_pattern $tmp_fq/$label"_paired"$secnd_pattern $tmp_fq/$label"_unpaired"$secnd_pattern ILLUMINACLIP:$name_adap:$ill_clip LEADING:$LEADING TRAILING:$TRAILING SLIDINGWINDOW:$SLIDINGWINDOW MINLEN:$MINLEN 2>&1 | tee  $tmp_log/trimmomatic-log-$label.log )

			getinfo=$(echo $(sed -n -e 5p $tmp_log/trimmomatic-log-$label.log))
			echo $label ":" $getinfo >> $tmp_clog/trimmomatic.log;

			echo $path$first_file >> $tmp_fq/list-finished.lst;
			echo $path$second_file >> $tmp_fq/list-finished.lst;
			runtime=$((($(date +%s)-$start)/60)) 
			echo "Trimmomatic for $label finished. Duration $runtime Minutes."  >> $tmp_clog/trimmomatic.log;

			totaltime=$(($runtime + $totaltime))
		done;
		echo "Trimmomatic finished.  Total time $totaltime Minutes." >> $tmp_clog/trimmomatic.log;

	
fi


if [ -f $tmp_fq/tmp.lst ]
then 
	remove=$(rm $tmp_fq/tmp.lst)
fi

sed -i "s/st_trim=.*/st_trim=3/g" config/pipeline.conf