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
		echo "Generating reference chromosome from Ref.genome  ..."
		#copy genome_ref  to result directory because of reading/writing probabaly. 
		pre_proc=$(cp $genome_ref/$genome_name $result_pipeline/rdata/)
		a_proc= $($samtools_path faidx $tmp_rdata/$genome_name)
		tmp=$(echo $genome_name | sed 's/.*\///')
		label=$(echo ${tmp%%.*})
		b_proc= $(cut -f1,2 $tmp_rdata/*.fai > $tmp_rdata/$label.txt )
		# creating R-data files.
		Rscript ./src/bash/gen-rdata.R $result_pipeline --no-save --no-restore --verbose > $tmp_clog/gen-rdata.log
		if [ -f $tmp_rdata/Ref_Chr.RData ]		
			then
				del=$(rm $tmp_rdata/*.fa)
				del=$(rm $tmp_rdata/*.fai)
				#del=$(rm $tmp_rdata/*.txt)
		fi	
	else
	echo -e "Found reference chromosome file.\n"

fi

if [ ! -f $tmp_rdata/TEs.RData ]		
	then
		cop=$(cp ./bindata/TEs.RData $tmp_rdata/)
fi

if [ ! -f $tmp_rdata/genes.RData ]		
	then
		cop=$(cp ./bindata/genes.RData $tmp_rdata/)
fi
