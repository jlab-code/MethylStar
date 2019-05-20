#!/bin/bash
curr_dir="$(dirname "$0")"
com1=$(awk '/^\[/ { } /=/ { print $0 }' config/pipeline.conf > $curr_dir/tmp.conf)
. $curr_dir/tmp.conf

echo "Converting to bedgraphFormat ..." 
Rscript ./src/bash/meth-bedgraph.R $result_pipeline --no-save --no-restore --verbose 



#download http://hgdownload.soe.ucsc.edu/admin/exe/linux.x86_64/

#chmod +x file 
#./bedGraphToBigWig methylome_Cvi-0-G4_L4-merged.txt.bedGraph ../rdata/TAIR10_chr_all.txt  test.bw


# check if everyfiles done then delete queue list 
if [ -z $(comm -23 <(sort -u $tmp_bed/list-files.lst) <(sort -u $tmp_bed/file-processed.lst)) ]  
then
	com=$(sed -i "s/st_bedgraph=.*/st_bedgraph=2/g" config/pipeline.conf)
	remove=$(rm $tmp_bed/file-processed.lst)
fi

# docker part 
if $docker_mode; 
then
	perm=$(chmod 777 -R $result_pipeline)
fi
