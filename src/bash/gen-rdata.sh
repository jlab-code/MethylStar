#!/bin/bash
curr_dir="$(dirname "$0")"
com1=$(awk '/^\[/ { } /=/ { print $0 }' config/pipeline.conf > $curr_dir/tmp.conf)
. $curr_dir/tmp.conf

: '

Generating Rdata file 
'
#generating up-to-date list of files

if [ ! -f $tmp_rdata/Ref_Chr.RData ]
	then
		echo "generating reference chromosome process ..."
		#copy genome_ref  to result directory because of reading/writing probabaly. 
		pre_proc=$(cp $genome_ref/$genome_name $result_pipeline/rdata/)
		a_proc= $(samtools faidx $tmp_rdata/$genome_name)
		tmp=$(echo $genome_name | sed 's/.*\///')
		label=$(echo ${tmp%%.*})
		b_proc= $(cut -f1,2 $tmp_rdata/*.fai > $tmp_rdata/$label.txt )
		# creating R-data files.
		Rscript ./src/bash/gen-rdata.R $result_pipeline --no-save --no-restore --verbose > $tmp_clog/gen-rdata.log
		# copy Gens, Tes to rdata folder
		copy=$(cp ./bindata/*.RData $tmp_rdata)
		if [ -f $tmp_rdata/Ref_Chr.RData ]		
			then
				del=$(rm $tmp_rdata/*.fa)
				del=$(rm $tmp_rdata/*.fai)
				#del=$(rm $tmp_rdata/*.txt)
		fi	
	else
	echo "There is a reference chromosome!"

fi