#!/bin/bash
curr_dir="$(dirname "$0")"
com1=$(awk '/^\[/ { } /=/ { print $0 }' config/pipeline.conf > $curr_dir/tmp.conf)
. $curr_dir/tmp.conf


Rscript ./src/bash/dmr-caller.R $result_pipeline --no-save --no-restore --verbose
sed -i "s/st_dmrcaller=.*/st_dmrcaller=2/g" config/pipeline.conf


: '

# check if everyfiles finished, then delete queue list 
if [ -z $(comm -23 <(sort -u $tmp_meth_out/file-processed.lst) <(sort -u $tmp_meth_out/list-files.lst)) ]  
then
	com=$(sed -i "s/st_methimpute=.*/st_methimpute=2/g" config/pipeline.conf)
	remove=$(rm $tmp_meth_out/file-processed.lst)
fi
'
# docker part 
if $docker_mode; 
then
	perm=$(chmod 777 -R $result_pipeline)
fi