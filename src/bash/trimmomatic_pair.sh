#!/bin/bash
curr_dir="$(dirname "$0")"
com1=$(awk '/^\[/ { } /=/ { print $0 }' config/pipeline.conf > $curr_dir/tmp.conf)
. $curr_dir/detect.sh trimm;
. $curr_dir/tmp.conf;



#-------------------------------------------------------------------------------
# check point
if [ -f $tmp_fq/list-finished.lst ]
	then
		echo "Resuming process ..."
		proc_a= $(sort $tmp_fq/list-files.lst -o $tmp_fq/list-files.lst)
		proc_b= $(sort $tmp_fq/list-finished.lst -o $tmp_fq/list-finished.lst)
		proc_c= $(comm -23 $tmp_fq/list-files.lst $tmp_fq/list-finished.lst > $tmp_fq/tmp.lst)
		input="$tmp_fq/tmp.lst"
	else
		input="$tmp_fq/list-files.lst"
	fi
#-------------------------------------------------------------------------------

#-------------------------------------------------------
# checking point for files
# running main prog


if $parallel_mode; then

	echo "Running in Parallel mode, number of jobs: $npar ."
	start=$(date +%s)
	doit() {

		. "$1"				
		label=$(echo $(echo $2 | sed 's/.*\///') | sed -e "s/$first_pattern//g")
		path=$(echo $(echo $2 | sed -e 's:[^/]*$::'))
		first_file=$label"$first_pattern"
		second_file=$label"$secnd_pattern"
		
		echo "-------------------------------------------------------------" 
		echo -e "Running trimmomatic for $first_file and $second_file ...\n"

		run=$($java_path -jar $trim_jar $end_mode -threads $n_th -phred33  $path$first_file $path$second_file $tmp_fq/$label"_paired"$first_pattern $tmp_fq/$label"_unpaired"$first_pattern $tmp_fq/$label"_paired"$secnd_pattern $tmp_fq/$label"_unpaired"$secnd_pattern ILLUMINACLIP:$name_adap:$ill_clip LEADING:$LEADING TRAILING:$TRAILING SLIDINGWINDOW:$SLIDINGWINDOW MINLEN:$MINLEN 2>&1 | tee -a  $tmp_log/trimmomatic-log-$label.log )
		echo -e "Summary: \n"
		cat $tmp_log/trimmomatic-log-$label.log
		echo $path$first_file >> $tmp_fq/list-finished.lst;
		echo $path$second_file >> $tmp_fq/list-finished.lst;
								   
		}

	export -f doit
	par=$(echo $curr_dir/tmp.conf) 
	grep "$first_pattern" "$input"  | parallel -j $npar doit "$par"

	end=$(date +%s)
	runtime=$((($(date +%s)-$start)/60)) 
	echo "Trimmomatic $label finished. Duration $runtime Minutes." 2>&1 | tee -a $tmp_clog/trimmomatic.log;

else
	for file in $(grep $first_pattern $input)
		do 
		start=$(date +%s)
		# get file name -extension
		label=$(echo $(echo $file | sed 's/.*\///') | sed -e "s/$first_pattern//g")
		path=$(echo $(echo $file | sed -e 's:[^/]*$::'))
		first_file=$label"$first_pattern"
		second_file=$label"$secnd_pattern"
		echo "-------------------------------------------------------------" 
		echo -e "running trimmomatic for $first_file and $second_file ...\n"
		run=$($java_path -jar $trim_jar $end_mode -threads $n_th -phred33  $path$first_file $path$second_file $tmp_fq/$label"_paired"$first_pattern $tmp_fq/$label"_unpaired"$first_pattern $tmp_fq/$label"_paired"$secnd_pattern $tmp_fq/$label"_unpaired"$secnd_pattern ILLUMINACLIP:$name_adap:$ill_clip LEADING:$LEADING TRAILING:$TRAILING SLIDINGWINDOW:$SLIDINGWINDOW MINLEN:$MINLEN 2>&1 | tee -a  $tmp_log/trimmomatic-log-$label.log )
		echo -e "Summary: \n"
		cat $tmp_log/trimmomatic-log-$label.log
		echo $path$first_file >> $tmp_fq/list-finished.lst;
		echo $path$second_file >> $tmp_fq/list-finished.lst;
		end=$(date +%s)
		runtime=$((($(date +%s)-$start)/60)) 
		echo "Trimmomatic $label finished. Duration $runtime Minutes." 2>&1 | tee -a $tmp_clog/trimmomatic.log;
		done;
fi


if [ -f $tmp_fq/tmp.lst ]
then 
	remove=$(rm $tmp_fq/tmp.lst)
fi

# check if everyfiles done then delete queue list 
if [ -z $(comm -23 <(sort -u $tmp_fq/list-files.lst) <(sort -u $tmp_fq/list-finished.lst)) ]  
then
	com=$(sed -i "s/st_trim=.*/st_trim=2/g" config/pipeline.conf)
	remove=$(rm $tmp_fq/list-finished.lst)
fi

# docker part 
if $docker_mode; 
then
	perm=$(chmod 777 -R $result_pipeline)
fi