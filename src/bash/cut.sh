#!/bin/bash
curr_dir="$(dirname "$0")"
com1=$(awk '/^\[/ { } /=/ { print $0 }' config/pipeline.conf > $curr_dir/tmp.conf)
. $curr_dir/tmp.conf



des=/mnt/extStorage/Intermediate_Datasets/columbia_intermediate/analysis
ori=/mnt/extStorage/Intermediate_Datasets/columbia_intermediate/results/methimpute-out
factor=CHH

if [ ! -d $des/$factor ]; then
        mkdir $des/$factor
fi

for file in $(ls -1v $ori/*_merged.txt)
        do 

                label=$(echo $(echo $file |sed 's/.*\///') | sed -e 's/_merged.txt//g');
                awk -F"\t" 'NR==1; NR>1 {if($4 == "CHH" && $7 >=0.99) {print}}' $file > $label.$factor.txt
                echo "$factor created!"
                awk -v OFS='\t' '{print $1,$2,$3,$10 }' $label.$factor.txt > $label.cut.txt
                rm $label.$factor.txt
                echo "cutted and deleted"
                mv $label.cut.txt $des/$factor/
                echo "$label moved."
                echo "----------------------------------------------------------------"

done
