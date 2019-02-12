#!/bin/bash
curr_dir="$(dirname "$0")"
com1=$(awk '/^\[/ { } /=/ { print $0 }' config/pipeline.conf > $curr_dir/tmp.conf)
. $curr_dir/tmp.conf


Rscript ./src/bash/methylkit.R $result_pipeline --no-save --no-restore --verbose > $tmp_clog/methylkit.log
sed -i "s/st_methykit=.*/st_methykit=3/g" config/pipeline.conf

if [ -f $tmp_methyl_fmt/file-processed.lst ]
then 
	remove=$(rm $tmp_methyl_fmt/file-processed.lst)
fi


