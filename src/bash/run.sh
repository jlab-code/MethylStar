#!/bin/bash
. $(dirname "$0")/config.cfg

#-------------------------------------------------------
: '
job0= preparing.sh
job1= trimmomatic.sh
job2= qc-fastq-report.sh
job3= bismark-mapper.sh
job4= qc-bam-report.sh
job5= bismark-deduplicate.sh
job6= bismark-meth-extractor.sh
job7= methimpute.sh
'
#-------------------------------------------------------



# to run separately

	qsub -N job0 -V -cwd -o $result_pipeline/cluster_logs/logs.txt -e $result_pipeline/cluster_logs/message.txt preparing.sh
	#qsub -N job1 -V -cwd -o $result_pipeline/cluster_logs/logs.txt -e $result_pipeline/cluster_logs/message.txt trimmomatic.sh

	##echo "qc part..."
	#qsub -N job2 -V -cwd -o $result_pipeline/cluster_logs/logs.txt -e $result_pipeline/cluster_logs/message.txt qc-fastq-report.sh

	##echo "bismark..."
	#qsub -N job3 -V -cwd -o $result_pipeline/cluster_logs/logs.txt -e $result_pipeline/cluster_logs/message.txt bismark-mapper.sh

	##echo "qc-bqm part..."
	#qsub -N job4 -V -cwd -o $result_pipeline/cluster_logs/logs.txt -e $result_pipeline/cluster_logs/message.txt qc-bam-report.sh

	##echo "deduplicate..."
	#qsub -N job5 -V -cwd -o $result_pipeline/cluster_logs/logs.txt -e $result_pipeline/cluster_logs/message.txt bismark-deduplicate.sh

	#echo "second run deduplicate..."
	#qsub -N job6 -V -cwd  -o -o $result_pipeline/cluster_logs/logs.txt -e $result_pipeline/cluster_logs/message.txt bismark-meth-extractor.sh
	#methout
	#qsub -N job7 -V -cwd -o $result_pipeline/cluster_logs/logs.txt -e $result_pipeline/cluster_logs/message.txt methimpute.sh




# run automatically
: '
	# running first script - preparing
	qsub -N job0 -V -cwd  -o $result_pipeline/cluster_logs/logs.txt -e $result_pipeline/cluster_logs/message.txt preparing.sh
	qsub -N job1 -V -cwd  -o $result_pipeline/cluster_logs/logs.txt -e $result_pipeline/cluster_logs/message.txt trimmomatic.sh
	# waiting for J1 then start J2
	qsub -hold_jid job1 -N job2 -V -cwd -o $result_pipeline/cluster_logs/logs.txt -e $result_pipeline/cluster_logs/message.txt qc-fastq-report.sh

	# waiting for J1 then start J3
	qsub -hold_jid job1 -N job3 -V -cwd -o $result_pipeline/cluster_logs/logs.txt -e $result_pipeline/cluster_logs/message.txt bismark-mapper.sh

	# waiting for J3 then start J4
	qsub -hold_jid job3 -N job4 -V -cwd -o $result_pipeline/cluster_logs/logs.txt -e $result_pipeline/cluster_logs/message.txt qc-bam-report.sh

	# waiting for J3 then start J5
	qsub -hold_jid job3 -N job5 -V -cwd -o $result_pipeline/cluster_logs/logs.txt -e $result_pipeline/cluster_logs/message.txt bismark-deduplicate.sh

	# waiting for j3, J5 then start J6
	qsub -hold_jid job3,job5 -N job6 -V -cwd -o $result_pipeline/cluster_logs/logs.txt -e $result_pipeline/cluster_logs/message.txt bismark-meth-extractor.sh

	qsub -hold_jid job5,job6 -N job7 -V -cwd -o $result_pipeline/cluster_logs/logs.txt -e $result_pipeline/cluster_logs/message.txt methimpute.sh

'
