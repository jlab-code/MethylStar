#!/bin/bash

curr_dir="$(dirname "$0")"
orgPip=$(pwd)
com1=$(awk '/^\[/ { } /=/ { print $0 }' config/pipeline.conf > $curr_dir/tmp.conf)
. $curr_dir/tmp.conf
. $curr_dir/detect.sh $genome_type bismap $npar;
. $curr_dir/tmp.conf

if [ `ls $tmp_bismap/*temp* 2>/dev/null | wc -l ` -gt 0 ]
then
  remove=$(rm $tmp_bismap/*temp*)
fi

if ! $pairs_mode; then
  echo "MethylStar does not support single-end data for the PBAT-based workflow right now." 2>&1 | tee -a $tmp_clog/bismark-mapper.log
  exit 1
fi

gen=$(ls -1v $tmp_fq/*_R1_trimmed.fq.gz $tmp_fq/*_R2_trimmed.fq.gz 2>/dev/null > $tmp_bismap/list-files.lst)

if [ -f $tmp_bismap/list-finished.lst ]
then
  echo -e "Resuming process ...\n"
  sort $tmp_bismap/list-files.lst -o $tmp_bismap/list-files.lst
  sort $tmp_bismap/list-finished.lst -o $tmp_bismap/list-finished.lst
  comm -23 $tmp_bismap/list-files.lst $tmp_bismap/list-finished.lst > $tmp_bismap/tmp.lst
else
  echo -e "Starting Bismark mapper ...\n"
  gen=$(cp $tmp_bismap/list-files.lst $tmp_bismap/tmp.lst)
fi

input="$tmp_bismap/tmp.lst"
echo -e "Genome Type: $genome_type \n"
echo -e "Bismark mapping mode for PBAT-based data: PE \n"

run_pbat_pe() {
  . "$1"
  tmp_path=$tmp_bismap/
  cd "${tmp_path%/*}"

  label=$(echo $(echo $2 | sed 's/.*\///') | sed -e "s/_R1_trimmed.fq.gz//g")
  file1=$label"_R1_trimmed.fq.gz"
  file2=$label"_R2_trimmed.fq.gz"
  instart=$(date +%s)

  if $nucleotide; then
    echo "-- Nucleotide coverage is enabled." 2>&1 | tee -a $tmp_clog/bismark-mapper.log
    echo "-- Running Bismark PBAT-based PE mapping for $file1 and $file2 ..." 2>&1 | tee -a $tmp_clog/bismark-mapper.log
    result=$($bismark_path/bismark -X 1000 --non_directional --local --un \
      --samtools_path $samtools_path --parallel $bis_parallel -p $Nthreads --nucleotide_coverage \
      --genome $genome_ref --bowtie2 -1 $tmp_fq/$file1 -2 $tmp_fq/$file2 \
      -o $tmp_bismap/ 2>&1 | tee -a $tmp_bismap/$label.log)
  else
    echo "-- Nucleotide coverage is disabled." 2>&1 | tee -a $tmp_clog/bismark-mapper.log
    echo "-- Running Bismark PBAT-based PE mapping for $file1 and $file2 ..." 2>&1 | tee -a $tmp_clog/bismark-mapper.log
    result=$($bismark_path/bismark -X 1000 --non_directional --local --un \
      --samtools_path $samtools_path --parallel $bis_parallel -p $Nthreads \
      --genome $genome_ref --bowtie2 -1 $tmp_fq/$file1 -2 $tmp_fq/$file2 \
      -o $tmp_bismap/ 2>&1 | tee -a $tmp_bismap/$label.log)
  fi

  echo $tmp_fq/$file1 >> $tmp_bismap/list-finished.lst;
  echo $tmp_fq/$file2 >> $tmp_bismap/list-finished.lst;
  echo "Bismark PBAT-based PE mapping for $file1 and $file2 finished. Duration time $((($(date +%s)-$instart)/60)) Minutes." 2>&1 | tee -a $tmp_clog/bismark-mapper.log
}

if $parallel_mode; then
  echo -e "Running Bismark Mapper in Parallel mode, number of jobs that proccessing at same time: $npar .\n"
  start=$(date +%s)
  par=$(echo $curr_dir/tmp.conf)
  export -f run_pbat_pe
  grep "_R1_trimmed.fq.gz" "$input" | parallel -j $npar --lb run_pbat_pe "$par"
  runtime=$((($(date +%s)-$start)/60))
  echo "Bismark Mapper finished. Duration $runtime Minutes." 2>&1 | tee -a $tmp_clog/bismark-mapper.log
else
  totaltime=0
  for fq in $(grep "_R1_trimmed.fq.gz" $tmp_bismap/tmp.lst)
  do
    start=$(date +%s)
    par=$(echo $curr_dir/tmp.conf)
    run_pbat_pe "$par" "$fq"
    runtime=$((($(date +%s)-$start)/60))
    totaltime=$(($runtime + $totaltime))
    echo -e "-------------------------------------------- \n"
  done
  echo "Bismark Mapper done. Total running time $totaltime Minutes." 2>&1 | tee -a $tmp_clog/bismark-mapper.log
fi

if [ -f $tmp_bismap/tmp.lst ]
then
  remove=$(rm $tmp_bismap/tmp.lst)
fi

#----------------------- Rename
for file in $(ls -1v $tmp_bismap/*_bismark_bt2_pe.bam 2>/dev/null)
do
  label=$(echo $(echo $file | sed 's/.*\///') | sed -e "s/_bismark_bt2_pe.bam//g")
  tmp=$(echo $label | sed "s/_R1_trimmed//g")
  mv $file $tmp_bismap/$tmp.bam
done

for file in $(ls -1v $tmp_bismap/*_bismark_bt2_PE_report.txt 2>/dev/null)
do
  label=$(echo $(echo $file | sed 's/.*\///') | sed -e "s/_bismark_bt2_PE_report.txt//g")
  tmp=$(echo $label | sed "s/_R1_trimmed//g")
  mv $file $tmp_bismap/$tmp.txt
done

for file in $(ls -1v $tmp_bismap/*nucleotide_stats.txt 2>/dev/null)
do
  label=$(echo $(echo $file | sed 's/.*\///') | sed -e "s/_bismark_bt2_pe.nucleotide_stats.txt//g")
  tmp=$(echo $label | sed "s/_R1_trimmed//g")
  mv $file $tmp_bismap/${tmp}_nu_stats.txt
done

cd $orgPip

if [ -z $(comm -23 <(sort -u $tmp_bismap/list-files.lst) <(sort -u $tmp_bismap/list-finished.lst)) ]
then
  com=$(sed -i "s/st_bismark=.*/st_bismark=2/g" config/pipeline.conf)
  remove=$(rm $tmp_bismap/list-finished.lst)
fi

if $docker_mode;
then
  perm=$(chmod 777 -R $result_pipeline)
fi
