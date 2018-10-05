#!/bin/bash
curr_dir="$(dirname "$0")"
com1=$(awk '/^\[/ { } /=/ { print $0 }' config/pipeline.conf > $curr_dir/tmp.conf)
. $curr_dir/tmp.conf


: '

run bismark deduplicate &
run bismark_methylation_extractor: atypical command to extract context-dependent (CpG/CHG/CHH) methylation
'
#generating up-to-date list of files
gen=$(ls -1v $tmp_dide/*.bam > $tmp_dme/list-files.lst)

if [ -f $tmp_dme/list-finished.lst ]
	then
		echo "Resuming process ..."
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
		input="$tmp_cx_report/list-files.lst"
		while read line
		do
			arr+=("$line")
		done < $input;
fi


	for bm in "${arr[@]}"
		do
		echo "Running for file $bm";
		tmp=$(echo $bm | sed 's/.*\///')
		label=$(echo ${tmp%%.*})
        bis_extractor=$($bismark_path/bismark_methylation_extractor $deduplicate  --bedGraph --parallel $bis_parallel --buffer_size $buf_size"G" --genome_folder $genome_ref $bm -o $tmp_dme/ 2>&1 | tee -a $tmp_dme/$label.log )
		echo "==========================================================" 
		cat  $tmp_dme/$label.deduplicated_splitting_report.txt
		echo $bm >> $tmp_dme/list-finished.lst;
		if $del_inter_file; then
			echo "Removing intermediate files... "
			remove_intermediate=$(rm $tmp_dme/*$label*.deduplicated.*txt)
		fi
	done;


if [ -f $tmp_dme/tmp.lst ]
then 
	remove=$(rm $tmp_dme/tmp.lst)
fi

