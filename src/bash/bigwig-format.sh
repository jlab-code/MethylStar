#!/bin/bash
curr_dir="$(dirname "$0")"
com1=$(awk '/^\[/ { } /=/ { print $0 }' config/pipeline.conf > $curr_dir/tmp.conf)
. $curr_dir/tmp.conf
. $curr_dir/detect.sh  $genome_type  qcFast $npar;
. $curr_dir/tmp.conf

: '
Converting BedGraph to BIGWIG Format.
'

#generating up-to-date list of files
gen=$(ls -1v $tmp_bed/*.bedGraph > $tmp_bigwig/list-files.lst)

if [ -f $tmp_bigwig/list-finished.lst ]
	then
		echo "Resuming process ..." 
		a_proc= $(sort $tmp_bigwig/list-files.lst -o $tmp_bigwig/list-files.lst)
		b_proc= $(sort $tmp_bigwig/list-finished.lst -o $tmp_bigwig/list-finished.lst)
		c_proc= $(comm -23 $tmp_bigwig/list-files.lst $tmp_bigwig/list-finished.lst > $tmp_bigwig/tmp.lst)
		#running main prog
		input="$tmp_bigwig/tmp.lst"
		while read line
			do
				arr+=("$line")
			done < $input;
	else
		echo "Starting to convert to bigWig format ..." 
		input="$tmp_bigwig/list-files.lst"
		while read line
		do
			arr+=("$line")
		done < $input;
fi
txt_find=$(ls -1v $tmp_rdata/*_chr_all.txt)
# running main prog
#--------------------------------------------------------
if $parallel_mode; then
	#running in parallel mode
	start=$(date +%s)
	echo "Running in Parallel mode, number of jobs: $npar ." 
	doit() {

		. "$1"
		txt_find=$(ls -1v $tmp_rdata/*_chr_all.txt)
		label=$(echo $(echo $2 |sed 's/.*\///') | sed -e 's/.bedGraph//g')
		echo "Running for $label ..."
		fast=$(./bindata/bedGraphToBigWig $2 $txt_find $tmp_bigwig/$label.bw)
		echo $2 >> $tmp_bigwig/list-finished.lst;
	}
	export -f doit
	par=$(echo $curr_dir/tmp.conf) 
	cat  "$input"  | parallel -j $npar doit "$par"
	end=$(date +%s)
	runtime=$((($(date +%s)-$start)/60))
	echo "Converted files. Duration $runtime Minutes." 
else
#running in single mode
	echo "Running in single mode. (Parallel is disabled.)" 
	start=$(date +%s)
	for bedfile in "${arr[@]}"
		do
		# get file name -extension
		label=$(echo $(echo $bedfile |sed 's/.*\///') | sed -e 's/.bedGraph//g')
		echo "Running for $label ..." 
		fast=$(./bindata/bedGraphToBigWig $bedfile $txt_find $tmp_bigwig/$label.bw)
		echo $bedfile >> $tmp_bigwig/list-finished.lst
		done
	end=$(date +%s)
	runtime=$((($(date +%s)-$start)/60))
	echo "Converted files. finished in $runtime minutes." 
	echo "You can find the results in $tmp_bigwig folder." 
	

fi

#-------------------------------------------------------------
# cleaning the folders and list

if [ -f $tmp_bigwig/tmp.lst ]
then 
	remove=$(rm $tmp_bigwig/tmp.lst)
fi

# check if everyfiles finished, then delete queue list 
if [ -z $(comm -23 <(sort -u $tmp_bigwig/list-files.lst) <(sort -u $tmp_bigwig/list-finished.lst)) ]  
then
	com=$(sed -i "s/st_bigwig=.*/st_bigwig=2/g" config/pipeline.conf)
	remove=$(rm $tmp_bigwig/list-finished.lst)
fi
# docker part 
if $docker_mode; 
then
	perm=$(chmod 777 -R $result_pipeline)
fi