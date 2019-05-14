#!/bin/bash
curr_dir="$(dirname "$0")"
com1=$(awk '/^\[/ { } /=/ { print $0 }' config/pipeline.conf > $curr_dir/tmp.conf)
. $curr_dir/tmp.conf

Rscript ./src/bash/methimpute-bam.R $result_pipeline $genome_ref $genome_name $tmp_rdata $intermediate $fit_output $enrichment_plot $TES_report $genes_report $mincov --no-save --no-restore --verbose 

# check if everyfiles finished, then delete queue list 
if [ -z $(comm -23 <(sort -u $tmp_meth_out/list-files.lst) <(sort -u $tmp_meth_out/file-processed.lst)) ]  
then
	com=$(sed -i "s/st_methimpute=.*/st_methimpute=2/g" config/pipeline.conf)
	remove=$(rm $tmp_meth_out/file-processed.lst)
fi