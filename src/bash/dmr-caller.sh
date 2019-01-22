#!/bin/bash
curr_dir="$(dirname "$0")"
com1=$(awk '/^\[/ { } /=/ { print $0 }' config/pipeline.conf > $curr_dir/tmp.conf)
. $curr_dir/tmp.conf


Rscript ./src/bash/dmr-caller.R $result_pipeline --no-save --no-restore --verbose > $tmp_clog/dmr.log 
sed -i "s/st_dmrcaller=.*/st_dmrcaller=3/g" config/pipeline.conf