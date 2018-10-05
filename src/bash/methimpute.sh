#!/bin/bash
curr_dir="$(dirname "$0")"
com1=$(awk '/^\[/ { } /=/ { print $0 }' config/pipeline.conf > $curr_dir/tmp.conf)
. $curr_dir/tmp.conf


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


#R CMD BATCH $result_pipeline $genome_name --save output.log
Rscript ./src/bash/methimpute.R $result_pipeline $genome_ref $genome_name $tmp_rdata $intermediate --save
