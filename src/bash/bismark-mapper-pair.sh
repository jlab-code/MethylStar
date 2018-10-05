#!/bin/bash
curr_dir="$(dirname "$0")"
com1=$(awk '/^\[/ { } /=/ { print $0 }' config/pipeline.conf > $curr_dir/tmp.conf)
. $curr_dir/tmp.conf


## Bismark Mapper

## Creating reference genome folders FOR FIRST TIME

if [ ! -d $genome_ref/Bisulfite_Genome ]; then
	gen=$($bismark_path/bismark_genome_preparation --verbose $genome_ref/)
	current_modified=$(stat -c "%Y" $genome_ref/$genome_name)
	sed -i "s/modified_time=.*/modified_time=$current_modified/g" config/pipeline.conf
	com1=$(awk '/^\[/ { } /=/ { print $0 }' config/pipeline.conf > $curr_dir/tmp.conf)
	. $curr_dir/tmp.conf

fi

## Checking if the references genome "TAIR10_chr_all.fa" is modified!
## if modified then regenerate the reference genome.


current_modified=$(stat -c "%Y" $genome_ref/$genome_name)
if [ "$modified_time" -lt "$current_modified" ]; then
	sed -i "s/modified_time=.*/modified_time=$current_modified/g" config/pipeline.conf
	echo "reference file modified, generating the new one..." ;
	gen=$($bismark_path/bismark_genome_preparation --verbose $genome_ref/)
	com1=$(awk '/^\[/ { } /=/ { print $0 }' config/pipeline.conf > $curr_dir/tmp.conf)
	. $curr_dir/tmp.conf
else
     echo "No changes in Ref.genome.";

fi

gen=$(ls -1v $tmp_fq/*.gz > $tmp_bismap/list-files.lst)

if [ -f $tmp_bismap/list-finished.lst ]
	then
		echo "Resuming process ..."
		proc_a= $(sort $tmp_bismap/list-files.lst -o $tmp_bismap/list-files.lst)
		proc_b= $(sort $tmp_bismap/list-finished.lst -o $tmp_bismap/list-finished.lst)
		proc_c= $(comm -23 $tmp_bismap/list-files.lst $tmp_bismap/list-finished.lst > $tmp_bismap/tmp.lst)
		input="$tmp_bismap/tmp.lst"
		while read line
			do
				arr+=("$line")
			done < $input;
	else

		input="$tmp_bismap/list-files.lst"
		gen=$(cp $tmp_bismap/list-files.lst  $tmp_bismap/tmp.lst)
		while read line
		do
			arr+=("$line")
		done < $input;
	fi


#changing directory to write in folder path
tmp_path=$tmp_bismap/
cd "${tmp_path%/*}"


if $run_pair_bismark; then 

	# start to run bismark mapper JUST FOR TWO PAIR
	for fq in $(grep "_paired$first_pattern" $tmp_bismap/tmp.lst)
		do 
			start=$(date +%s)
			echo "-----------------------------------------------------------"
			# get file name -extension
			#label=$(echo $(echo $fq |sed 's/.*\///') | sed -e 's/.fq.gz//g');

			label=$(echo $(echo $fq | sed 's/.*\///') | sed -e "s/$first_pattern//g")
			file1=$label"$first_pattern"
			file2=$label"$secnd_pattern"
			echo "Starting bismark for $file1 and $file2"
			
			if $nucleotide; then
				# generating nucleotide report 
				result=$($bismark_path/bismark -N 1 -L 32 --parallel $bis_parallel --nucleotide_coverage --genome $genome_ref -1 $tmp_fq/$file1 -2 $tmp_fq/$file2 -o $tmp_bismap/ 2>&1 | tee -a $tmp_bismap/$label.log ) 
			else
				echo "Nucleotide coverage is disabled." 
				result=$($bismark_path/bismark -N 1 -L 32 --parallel $bis_parallel --genome $genome_ref -1 $tmp_fq/$file1 -2 $tmp_fq/$file2 -o $tmp_bismap/ 2>&1 | tee -a $tmp_bismap/$label.log)
			fi
			echo $tmp_fq/$file1 >> $tmp_bismap/list-finished.lst;
			echo $tmp_fq/$file2 >> $tmp_bismap/list-finished.lst;
			#--------------------------------------------------
			end=$(date +%s)
			runtime=$((($(date +%s)-$start)/60)) 
			#-------------------------------------------------------
			echo "Bismark for $label finished. Duration $runtime Minutes."
			echo "--------------------------------------------------------"
		done

else
	# start to run bismark default -- 4 pairs --> pair_1,unpaired_1 & paired_2, unpaired_2
	for fq in $(grep "_paired$first_pattern" $tmp_bismap/tmp.lst)
		do 
			start=$(date +%s)
			echo "-----------------------------------------------------------"
			label=$(echo $(echo $fq | sed 's/.*\///') | sed -e "s/_paired$first_pattern//g")
			file1=$label"_paired$first_pattern"
			file2=$label"_unpaired$first_pattern"
			file3=$label"_paired$secnd_pattern"
			file4=$label"_unpaired$secnd_pattern"
			echo "Starting bismark for $file1 , $file2 and $file3 , $file4 ..."
			if $nucleotide; then
				# generating nucleotide report 
				result=$($bismark_path/bismark -s 0 -u 0 -n 0 -l 20 --parallel $bis_parallel --nucleotide_coverage --genome $genome_ref -1 $tmp_fq/$file1 $tmp_fq/$file2 -2 $tmp_fq/$file3 $tmp_fq/$file4 -o $tmp_bismap/ 2>&1 | tee -a $tmp_bismap/$label.log ) 
			else
				echo "Nucleotide coverage is disabled." 
				result=$($bismark_path/bismark -s 0 -u 0 -n 0 -l 20 --parallel $bis_parallel --genome $genome_ref -1 $tmp_fq/$file1 $tmp_fq/$file2 -2 $tmp_fq/$file3 $tmp_fq/$file4 -o $tmp_bismap/ 2>&1 | tee -a $tmp_bismap/$label.log)
			fi
			
			echo $tmp_fq/$file1 >> $tmp_bismap/list-finished.lst;
			echo $tmp_fq/$file2 >> $tmp_bismap/list-finished.lst;
			echo $tmp_fq/$file3 >> $tmp_bismap/list-finished.lst;
			echo $tmp_fq/$file4 >> $tmp_bismap/list-finished.lst;
			
			#--------------------------------------------------
			end=$(date +%s)
			runtime=$((($(date +%s)-$start)/60)) 
			#-------------------------------------------------------
			echo "Bismark for $label finished. Duration $runtime Minutes."
			echo "--------------------------------------------------------"


		done

fi

if [ -f $tmp_bismap/tmp.lst ]
then 
	remove=$(rm $tmp_bismap/tmp.lst)
fi


#------------------------------------ Renaming
for file in $(ls -1v $tmp_bismap/*.bam)
	do
		echo $file
		tmp=$(echo $file | sed 's/.*\///')
		fname=$(echo ${tmp%%.*})
		mv $file $tmp_bismap/$fname.bam
	done
# rename logs to fq
for file in $(ls -1v $tmp_bismap/*.txt)
	do
		tmp=$(echo $file | sed 's/.*\///')
		fname=$(echo ${tmp%%.*})
		mv $file $tmp_bismap/$fname.txt
	done
#--------------------------------------

echo "Bismark part finished. Please check the $tmp_bismap directory for logs."

