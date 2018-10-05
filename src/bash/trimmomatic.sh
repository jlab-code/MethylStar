#!/bin/bash
curr_dir="$(dirname "$0")"
com1=$(awk '/^\[/ { } /=/ { print $0 }' config/pipeline.conf > $curr_dir/tmp.conf)
. $curr_dir/tmp.conf


#---------------------------------------------------------------
# check point

if [ -f $tmp_fq/list-finished.lst ]
	then
		echo "Resuming process ..."
		proc_a= $(sort $tmp_fq/list-files.lst -o $tmp_fq/list-files.lst)
		proc_b= $(sort $tmp_fq/list-finished.lst -o $tmp_fq/list-finished.lst)
		proc_c= $(comm -23 $tmp_fq/list-files.lst $tmp_fq/list-finished.lst > $tmp_fq/tmp.lst)
		input="$tmp_fq/tmp.lst"
		while read line
			do
				arr+=("$line")
			done < $input;
	else
		input="$tmp_fq/list-files.lst"
		while read line
		do
			arr+=("$line")
		done < $input;
	fi

#---------------------------------------------------------------

# running main prog

if $parallel_mode; then

		start=$(date +%s)
	doit() {
					
		. "$1"              
		tmp=$(echo $2| sed 's/.*\///')
		label=$(echo ${tmp%%.*})
		echo $label
		echo -e "running trimmomatic.... $2 \n"
		run=$($java_path -jar $trim_jar $end_mode -threads $n_th -phred33  $2 $tmp_fq/$label.fq.gz ILLUMINACLIP:$name_adap:$ill_clip LEADING:$LEADING TRAILING:$TRAILING SLIDINGWINDOW:$SLIDINGWINDOW MINLEN:$MINLEN 2>&1 | tee -a $tmp_log/trimmomatic-log-$label.log)
		echo -e "Summary: \n"
		cat $tmp_log/trimmomatic-log-$label.log     
		echo $2 >> $tmp_fq/list-finished.lst;
								   
		}
		export -f doit
		par=$(echo $curr_dir/tmp.conf) 
		cat "$input"  | parallel -j $npar doit "$par"
		end=$(date +%s)
		runtime=$((($(date +%s)-$start)/60)) 
		echo "Trimmomatic $label finished. Duration $runtime Minutes."
						
else
	for file in "${arr[@]}"
		do
		echo "running for " $file;
		start=$(date +%s)
		tmp=$(echo $file| sed 's/.*\///')
		label=$(echo ${tmp%%.*})
		echo "------------------------------------------------------------------"
		echo -e "running trimmomatic.... $file \n"
		run=$($java_path -jar $trim_jar $end_mode -threads $n_th -phred33  $file $tmp_fq/$label.fq.gz ILLUMINACLIP:$name_adap:$ill_clip LEADING:$LEADING TRAILING:$TRAILING SLIDINGWINDOW:$SLIDINGWINDOW MINLEN:$MINLEN 2>&1 | tee -a $tmp_log/trimmomatic-log-$label.log)
		echo -e "Summary: \n"
		cat $tmp_log/trimmomatic-log-$label.log                                 
		end=$(date +%s)
		runtime=$((($(date +%s)-$start)/60))
		echo "Trimmomatic $file finished in $runtime Minutes."
		echo "------------------------------------------------------------------"
		echo $tmp_fq
		echo $file >> $tmp_fq/list-finished.lst;
		done;
fi

if [ -f $tmp_fq/tmp.lst ]
then 
	remove=$(rm $tmp_fq/tmp.lst)
fi