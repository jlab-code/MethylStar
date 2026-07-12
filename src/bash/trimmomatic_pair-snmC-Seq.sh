#!/bin/bash
curr_dir="$(dirname "$0")"
com1=$(awk '/^\[/ { } /=/ { print $0 }' config/pipeline.conf > $curr_dir/tmp.conf)
. $curr_dir/tmp.conf;
. $curr_dir/detect.sh $genome_type trimm $npar;
. $curr_dir/tmp.conf;


#-------------------------------------------------------------------------------
# check point
mkdir -p "$tmp_fq" "$tmp_fq/adaptor_trimmed" "$tmp_log" "$tmp_clog"
step_1_finished=$tmp_fq/adaptor_trimmed/list-finished-step-1.lst
step_2_finished=$tmp_fq/list-finished-step-2.lst

if [ ! -f "$tmp_fq/list-files.lst" ]; then
	if [ -d "$raw_dataset" ]; then
		find "$raw_dataset" -type f -name "*.gz" | sort -V > "$tmp_fq/list-files.lst"
	elif [ -f "$raw_dataset" ]; then
		echo "$raw_dataset" > "$tmp_fq/list-files.lst"
	else
		echo "ERROR: raw_dataset does not exist: $raw_dataset" 2>&1 | tee -a "$tmp_clog/trimmomatic.log"
		exit 1
	fi
fi

if [ -s "$step_2_finished" ]
	then
		echo "Resuming process ..."
		sort $tmp_fq/list-files.lst -o $tmp_fq/list-files.lst
		sort $step_2_finished -o $step_2_finished
		comm -23 $tmp_fq/list-files.lst $step_2_finished > $tmp_fq/tmp.lst
		input="$tmp_fq/tmp.lst"
	else
		touch "$step_1_finished" "$step_2_finished"
		input="$tmp_fq/list-files.lst"
	fi
#-------------------------------------------------------------------------------

trim_snmc_pair() {
	. "$1"
	label=$(echo $(echo $2 | sed 's/.*\///') | sed -e "s/$first_pattern//g")
	path=$(echo $(echo $2 | sed -e 's:[^/]*$::'))
	first_file=$label"$first_pattern"
	second_file=$label"$secnd_pattern"

	adaptor_dir=$tmp_fq/adaptor_trimmed
	r1_adaptor=$adaptor_dir/$label"_R1_adaptor_trimmed.fq.gz"
	r2_adaptor=$adaptor_dir/$label"_R2_adaptor_trimmed.fq.gz"
	r1_trimmed=$tmp_fq/$label"_R1_trimmed.fq.gz"
	r2_trimmed=$tmp_fq/$label"_R2_trimmed.fq.gz"
	step_1_finished=$adaptor_dir/list-finished-step-1.lst
	step_2_finished=$tmp_fq/list-finished-step-2.lst
	step_1_log=$adaptor_dir/$label"_step_1.log"
	step_2_log=$tmp_fq/$label"_step_2.log"

	echo "-------------------------------------------------------------"
	echo -e "Running PBAT-based fastp preset for $first_file and $second_file ...\n"

	mkdir -p "$adaptor_dir"

	log_command_line() {
		local log_file="$1"
		shift
		{
			printf 'Command:'
			for arg in "$@"
			do
				printf ' %q' "$arg"
			done
			printf '\n'
		} 2>&1 | tee -a "$log_file"
	}

	# Step 1. Adapter/poly-G/quality trimming for PBAT-based reads.
	step_1_cmd=(fastp -i "$path$first_file" -I "$path$second_file" -o "$r1_adaptor" -O "$r2_adaptor" \
              --qualified_quality_phred "$fastp_qualified_quality_phred" --thread "$n_th"
              )
	if [ "$fastp_trim_poly_g" = "true" ]; then
		step_1_cmd+=(--trim_poly_g)
	fi
	if [ "$fastp_detect_adapter_for_pe" = "true" ]; then
		step_1_cmd+=(--detect_adapter_for_pe)
	fi

	if [ -f "$step_1_finished" ] && grep -Fxq "$path$first_file" "$step_1_finished" && grep -Fxq "$path$second_file" "$step_1_finished"; then
		echo "Step 1. Adapter/poly-G/quality trimming for $label was already finished." 2>&1 | tee -a "$step_1_log"
	else
		echo "Step 1. Adapter/poly-G/quality trimming for $label." 2>&1 | tee -a "$step_1_log"
		log_command_line "$step_1_log" "${step_1_cmd[@]}"
		"${step_1_cmd[@]}" 2>&1 | tee -a "$step_1_log"
		echo $path$first_file >> $step_1_finished;
		echo $path$second_file >> $step_1_finished;
	fi

	# Step 2. Trimming after adapter removal.
	step_2_cmd=(fastp -i "$r1_adaptor" -I "$r2_adaptor" -o "$r1_trimmed" -O "$r2_trimmed" \
		          --trim_front1 "$fastp_trim_front1" --trim_front2 "$fastp_trim_front2" \
		          --disable_adapter_trimming --length_required "$fastp_length_required" --thread "$n_th"
            )
	if [ "$fastp_trim_tail1" != "0" ]; then
		step_2_cmd+=(--trim_tail1 "$fastp_trim_tail1")
	fi
	if [ "$fastp_trim_tail2" != "0" ]; then
		step_2_cmd+=(--trim_tail2 "$fastp_trim_tail2")
	fi

	if [ -f "$step_2_finished" ] && grep -Fxq "$path$first_file" "$step_2_finished" && grep -Fxq "$path$second_file" "$step_2_finished"; then
		echo "Step 2. Trimming for $label was already finished." 2>&1 | tee -a "$step_2_log"
	else
		echo "Step 2. Trimming for $label." 2>&1 | tee -a "$step_2_log"
		log_command_line "$step_2_log" "${step_2_cmd[@]}"
		"${step_2_cmd[@]}" 2>&1 | tee -a "$step_2_log"
		echo $path$first_file >> $step_2_finished;
		echo $path$second_file >> $step_2_finished;
		echo "PBAT-based trimming for $label finished." 2>&1 | tee -a $tmp_clog/trimmomatic.log;
	fi
}

#-------------------------------------------------------
# checking point for files
# running main prog

if $parallel_mode; then

	echo -e "Running in Parallel mode, number of jobs: $npar .\n"
	start=$(date +%s)
	export -f trim_snmc_pair
	par=$(echo $curr_dir/tmp.conf)
	grep "$first_pattern" "$input"  | parallel -j $npar --lb trim_snmc_pair "$par"

	end=$(date +%s)
	runtime=$((($(date +%s)-$start)/60))
	echo "PBAT-based trimming finished. Duration $runtime Minutes." 2>&1 | tee -a $tmp_clog/trimmomatic.log;

else
	for file in $(grep $first_pattern $input)
		do
		start=$(date +%s)
		par=$(echo $curr_dir/tmp.conf)
		trim_snmc_pair "$par" "$file"
		end=$(date +%s)
		runtime=$((($(date +%s)-$start)/60))
		echo "PBAT-based trimming finished. Duration $runtime Minutes." 2>&1 | tee -a $tmp_clog/trimmomatic.log;
		done;
fi

if [ -f $tmp_fq/tmp.lst ]
then
	remove=$(rm $tmp_fq/tmp.lst)
fi

# check if everyfiles done then delete queue list
if [ -z $(comm -23 <(sort -u $tmp_fq/list-files.lst) <(sort -u $step_2_finished)) ]
then
	com=$(sed -i "s/st_trim=.*/st_trim=2/g" config/pipeline.conf)
	remove_step_2=$(rm $step_2_finished)
	if [ -f $step_1_finished ]; then
		remove_step_1=$(rm $step_1_finished)
	fi
fi

# docker part
if $docker_mode;
then
	perm=$(chmod 777 -R $result_pipeline)
fi
