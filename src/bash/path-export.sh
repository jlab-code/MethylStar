#!/bin/bash
curr_dir="$(dirname "$0")"
com1=$(awk '/^\[/ { } /=/ { print $0 }' config/pipeline.conf > $curr_dir/tmp.conf)
. $curr_dir/tmp.conf


if [ ! -d $bismark_path ]; then
	echo "Error: we require Bismark! but its not installed. see the configuration file 'config.cfg'"
	exit 1
fi

if ! [ -x "$(command -v bowtie2)" ]; then
  echo "Error: we could't find 'Bowtie2' in your PATH. see the configuration file 'config.cfg'"
  exit 1
 else 
 	sam=$(echo $(command -v bowtie2)) 
 	echo $bow
	export PATH="$PATH:$bow"
fi

if ! [ -x "$(command -v samtools)" ]; then
  echo "Error: we could't find 'samtools' in your PATH. see the configuration file 'config.cfg'"
  exit 1
 else 
 	sam=$(echo $(command -v samtools)) 
 	echo $sam
	export PATH="$PATH:$sam"
fi
