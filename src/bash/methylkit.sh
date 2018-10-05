#!/bin/bash
curr_dir="$(dirname "$0")"
com1=$(awk '/^\[/ { } /=/ { print $0 }' config/pipeline.conf > $curr_dir/tmp.conf)
. $curr_dir/tmp.conf


Rscript ./src/bash/methylkit.R $result_pipeline $statistic $NCORES $tmp_methal $Cytosine_context_Methylkit $qvalue $difference $qvalue_cutoff $meth_cutoff $lo_count $lo_perc $hi_count $hi_perc $win_size $step_size --save



