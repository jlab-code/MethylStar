#!/bin/bash
curr_dir="$(dirname "$0")"
com1=$(awk '/^\[/ { } /=/ { print $0 }' config/pipeline.conf > $curr_dir/tmp.conf)
. $curr_dir/tmp.conf


Rscript ./src/bash/methylkit.R $result_pipeline --no-save --no-restore --verbose 

# check if everyfiles done then delete queue list 
if [ -z $(comm -23 <(sort -u $tmp_methyl_fmt/list-files.lst) <(sort -u $tmp_methyl_fmt/file-processed.lst)) ]  
then
	com=$(sed -i "s/st_methykit=.*/st_methykit=2/g" config/pipeline.conf)
	remove=$(rm $tmp_methyl_fmt/file-processed.lst)
fi

# docker part 
if $docker_mode; 
then
	perm=$(chmod 777 -R $result_pipeline)
fi