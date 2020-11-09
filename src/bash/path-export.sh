#!/bin/bash
curr_dir="$(dirname "$0")"
com1=$(awk '/^\[/ { } /=/ { print $0 }' config/pipeline.conf > $curr_dir/tmp.conf)
. $curr_dir/tmp.conf


if [ ! -d $bismark_path ]; then
	echo "Error: we require Bismark! But it's not installed. See the configuration file 'config.cfg'."
	exit 1
fi

if ! [ -x "$(command -v bowtie2)" ]; then
  echo "Error: we couldn't find 'Bowtie2' in your PATH. See the configuration file 'config.cfg'."
  exit 1
 else 
 	bow=$(echo $(command -v bowtie2)) 
 	echo $bow
	export PATH="$PATH:$bow"
fi

if ! [ -x "$(command -v $samtools_path)" ]; then
  echo "Error: we couldn't find 'samtools' in the specified location. See the configuration file 'config.cfg'."
  exit 1
fi
