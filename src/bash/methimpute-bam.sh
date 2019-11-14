#!/bin/bash
curr_dir="$(dirname "$0")"
com1=$(awk '/^\[/ { } /=/ { print $0 }' config/pipeline.conf > $curr_dir/tmp.conf)
. $curr_dir/tmp.conf
. $curr_dir/detect.sh  $genome_type  methimpute $npar;
. $curr_dir/tmp.conf

start=$(date +%s)

gen=$(ls -1v $tmp_covseq/sorted-*.bam > $tmp_meth_out/list-files.lst)


if [ -f $tmp_meth_out/list-finished.lst ]
        then
                echo "Resuming Methimpute jobs ..."
                a_proc= $(sort $tmp_meth_out/list-files.lst -o $tmp_meth_out/list-files.lst)
                b_proc= $(sort $tmp_meth_out/list-finished.lst -o $tmp_meth_out/list-finished.lst)
                c_proc= $(comm -23 $tmp_meth_out/list-files.lst $tmp_meth_out/list-finished.lst > $tmp_meth_out/tmp.lst)
                #running main prog
                input="$tmp_meth_out/tmp.lst"
                while read line
                        do
                                arr+=("$line")
                        done < $input;
        else
                echo "Starting Methimpute job ..."
                input="$tmp_meth_out/list-files.lst"
                while read line
                do
                        arr+=("$line")
                done < $input;
fi

cat  "$input"  | parallel -j $npar --lb  Rscript ./src/bash/methimpute-bam.R $result_pipeline $genome_ref $genome_name $tmp_rdata $intermediate $fit_output $enrichment_plot $full_report  $mincov $intermediate_mode $file --no-save --no-restore --verbose 


# check if everyfiles finished, then delete queue list 
if [ -z $(comm -23 <(sort -u $tmp_meth_out/list-files.lst) <(sort -u $tmp_meth_out/file-processed.lst)) ]  
then
        # all parts done, reset to 0 (new run)
        com=$(sed -i "s/st_methimpute=.*/st_methimpute=0/g" config/pipeline.conf)
        com=$(sed -i "s/st_trim=.*/st_trim=0/g" config/pipeline.conf)
        com=$(sed -i "s/st_fastq=.*/st_fastq=0/g" config/pipeline.conf)
        com=$(sed -i "s/st_bismark=.*/st_bismark=0/g" config/pipeline.conf)
        com=$(sed -i "s/st_bissort=.*/st_bissort=0/g" config/pipeline.conf)
        com=$(sed -i "s/st_bisdedup=.*/st_bisdedup=0/g" config/pipeline.conf)
        com=$(sed -i "s/st_dedsort=.*/st_dedsort=0/g" config/pipeline.conf)
        com=$(sed -i "s/st_coreport=.*/st_coreport=0/g" config/pipeline.conf)
        remove=$(rm $tmp_meth_out/file-processed.lst)
fi
end=$(date +%s)
runtime=$((($(date +%s)-$start)/60))
echo "Running Methimpute finished in $runtime Minutes. " 2>&1 | tee -a $tmp_clog/methimpute.log
# docker part 
if $docker_mode; 
then
        perm=$(chmod 777 -R $result_pipeline)
fi
