#!/bin/sh

curr_dir="$(dirname "$0")"
com1=$(awk '/^\[/ { } /=/ { print $0 }'  config/pipeline.conf > $curr_dir/tmp.conf)
. $curr_dir/tmp.conf


#-------------------------------------------------------------------------------
# System checking
#-------------------------------------------------------------------------------
: '
if ! [ -x "$(command -v $fastq_path)" ]; then
  echo "Error: we require FASTQC but its not installed. see the configuration file 'config.cfg'" >&2
  exit 1
fi

if ! [ -x "$(command -v $trim_path/$trim_jar)" ]; then
  echo "Error: we require Trimmomatic but its not installed. see the configuration file 'config.cfg'"
  exit 1
fi

if [ ! -d $bismark_path ]; then
	echo "Error: we require Bismark! but its not installed. see the configuration file 'config.cfg'"
	exit 1
fi
'
#-------------------------------------------------------------------------------
# config directories.
#-------------------------------------------------------------------------------
#step2: select all input datasets (Columbia accessions)

# check user input directories
if [ ! -d $raw_dataset ]; then
	echo "Directory of data-sets is not exist. see the configuration file 'config.cfg'"
	exit 1
fi

if [ ! -d $result_pipeline ]; then
	mkdir $result_pipeline
	echo "creating result folder in $result_pipeline"
	echo "All the results will save in $result_pipeline folder"

fi

#creating folders
if [ ! -d $tmp_fq ]; then
		mkdir $tmp_fq
fi

if [ ! -d $tmp_log ]; then
		mkdir $tmp_log
fi

if [ ! -d $tmp_qcfast ]; then
    mkdir $tmp_qcfast
fi

if [ ! -d $tmp_bismap ]; then
    mkdir $tmp_bismap
fi

if [ ! -d $tmp_qcbam ]; then
    mkdir $tmp_qcbam
fi

if [ ! -d $tmp_dide ]; then
    mkdir $tmp_dide
fi

if [ ! -d $tmp_dme ]; then
    mkdir $tmp_dme
fi

if [ ! -d $tmp_clog ]; then
		mkdir $tmp_clog
fi

if [ ! -d $tmp_meth_out ]; then
		mkdir $tmp_meth_out
fi

if [ ! -d $tmp_cx_report ]; then
		mkdir $tmp_cx_report
fi

if [ ! -d $tmp_rdata ]; then
		mkdir $tmp_rdata
fi

if [ ! -d $tmp_tes_out ]; then
		mkdir $tmp_tes_out
fi
if [ ! -d $tmp_gen_out ]; then
		mkdir $tmp_gen_out
fi
if [ ! -d $tmp_fit_out ]; then
		mkdir $tmp_fit_out
fi

if [ ! -d $tmp_methal ]; then
		mkdir $tmp_methal
fi
if [ ! -d $tmp_dmr ]; then
		mkdir $tmp_dmr
fi
if [ ! -d $tmp_methyl_fmt ]; then
		mkdir $tmp_methyl_fmt
fi





# reading all raw-files and creating a list, the script will be read this file and start to process the file. ("list-files")
# the first script is "trimmomatic" so the file that we created above will be feed to this script.
# The "list-files.txt"  is in '$tmp_fq' folder.
: '
if [ -f "$tmp_fq/list-files.lst" ]
then
	del=$(rm $tmp_fq/list-files.lst)
else
	echo "Creating list of files..."
fi

for entry in "$raw_dataset"

do
        if [ -d "$entry" ];then
                 $(ls -1v $entry/*.gz >> $tmp_fq/list-files.lst )
        fi
        if [ -f "$entry"*.gz ];then
                echo "$entry" >> $tmp_fq/list-files.lst
        fi

done
'