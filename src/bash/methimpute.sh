#!/bin/bash
curr_dir="$(dirname "$0")"
com1=$(awk '/^\[/ { } /=/ { print $0 }' config/pipeline.conf > $curr_dir/tmp.conf)
. $curr_dir/tmp.conf

: '
if [ ! -d $tmp_rdata ]; then
	echo "Error: we require .RData file for genes/TEs/etc.(annotation files) see $tmp_rdata in the configuration file 'config.cfg' "
	exit 1
fi

if [ -n "$(ls -A $tmp_rdata/*.RData 2>/dev/null)" ]
then
  echo "Found RData files"
else
	echo "Error: we require '.RData' file for genes/TEs/etc.(annotation files).Please copy the files into $tmp_rdata"
	exit 1
fi
'

#R CMD BATCH $result_pipeline $genome_name --save output.log
Rscript ./src/bash/methimpute.R $result_pipeline $genome_ref $genome_name $tmp_rdata $intermediate $fit_output $enrichment_plot $TES_report $genes_report --no-save --no-restore --verbose > $tmp_clog/methimpute.log
sed -i "s/st_methimpute=.*/st_methimpute=3/g" config/pipeline.conf

# checking files that done. 
diff --brief <(sort $tmp_meth_out/file-processed.lst) <(sort $tmp_meth_out/list-files.lst) >/dev/null
comp_value=$?
if [ $comp_value -eq 1 ]
then
    echo "Keeping list of files that processed."
else
    remove=$(rm $tmp_meth_out/file-processed.lst)
fi

: '
if [ -f $tmp_meth_out/file-processed.lst ]
then 
	remove=$(rm $tmp_meth_out/file-processed.lst)
fi
'