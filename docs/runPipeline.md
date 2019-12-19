Running MethylStar pipeline
================

Once you are in the main directory of MethylStar, type the following command:

``` bash  
python2 run.py
```

List of following options will be displayed in the Main menu:


```
==================================================

	Welcome to MethylStar

==================================================
Please choose from the menu:

	1. Run Pipeline (WGBS)
	2. Outputs/Reports
	3. Access JBrowse
	4. Clean-up files
	5. Help

	C. Configuration

Q. Quit

```
Select one of the options by typing the corresponding value and pressing 'ENTER'. Type 'Q' to Quit. (Not case sensitive)

> **_NOTE:_** Before running the pipeline, please edit the configuration file under option ```C. Configuration``` .

Selecting ``option '1'`` will display the different options for running the pipeline. 

- Select option ``A. Quick Run...`` to run the entire pipeline in one go.
- Select option ``B. Individual Run ...`` to run individual steps of the pipeline.


#### **1. Run Pipeline (WGBS)**

```
Please choose from the menu:

A. Quick Run: 

	0. Trimmomatic,QC-Fastq-report,Bismark(alignment,remove duplicates),Extract methylation calls,Methimpute.

B. Individual Run: 

	1. Run Trimommatic
	2. Run QC-Fastq-report
	3. Run Bismark Mapper
	4. Run Genome coverage & Sequencing depth (After Mapping)
	5. Run Bismark deduplication
	6. Run Genome coverage & Sequencing depth (After deduplicate)
	7. Run Bismark Methylation Extractor
	8. Generate Cytosine Calls (cx-reports)
	9. Run Methimpute

B. Back to main Menu

```

#### **2. Output/Reports**

All outputs from the pipeline will be available in Output/Reports. This option allows the user to convert Methimpute outputs into bedgraph, bigwig and for input into popular DMRcallers (e,g Methylkit, DMRcaller).

```
Please choose from the menu:

	1. Convert Methimpute output to DMRCaller Format
	2. Convert Methimpute output to Methylkit Format
	3. Convert Methimpute output to bedGraph Format
	4. Convert bedGraph to BigWig Format
```
#### **3. Access JBrowse**
<!--
Guest users can create an account for the first time by signing up on this site: 
http://jlabdata.org/signup
-->
If you already have an account, please open the following URL in your web browser:
http://jlabdata.org/jbrowse

Users can upload bigwig files on to Jbrowse for visualization of regions of interest. 

#### **4. Clean-up files**
Here, you can delete log files that were generated during analysis. 
```
Please choose the menu you want to remove:

	1. Clean Trimmomatic/log file(s).
	2. Clean Qc-fastq-report/log file(s).
	3. Clean bismark mapper/log file(s).
	4. Clean qc-bam report Directory log file(s).
	5. Clean Bismark deduplicate/log file(s).
	6. Clean Bismark Meth. Extractor/log file(s).
	7. Clean Cx reports/log file(s).
	8. Clean Methimpute/log file(s).
	9. Clean DMR Directory/log file(s).
	10. Clean meth-bedgraph/log file(s).
	11. Clean methylkit/log file(s).
	12. Clean bigwig/log file(s).
```

#### **C. Configuration**
```
1. Path: RAW files
2. Path: Export results
3. Path: Reference Genome
4. Read-trimming parameters
5. Path: QC-Fastq
6. Alignment parameters
7. Methimpute parameters
8. Parallel mode
9. E-mail notification
10. See configured parameters

B. Back to main Menu
```

##### **Setting correct paths**
Ensure that specific PATHs to raw files ``option '1'``, output folders ``option '2'``, reference genome ``option '3'``, Trimmomatic software path ``option '4'``, QC-FastQ path ``option '5'``, Bismark & Samtools path ``option '6'`` exist.

##### **Read-trimming parameters**
Configure read trimming parameters by specifying ``option '4'`` and then typing [y/n] to configure the settings.

- Set software path correctly and select Adapter type 
- By default the quality scores are converted to phred33.
- specify SE for single-end reads and PE for paired-end reads
- Remove leading low quality or N bases (below quality 20)
- Remove trailing low quality or N bases (below quality 20)
- Perform a sliding window trimming, cutting once the average quality within the window falls below a threshold
- Drop the read if it is below a specified length with MINLEN

```
4. Read-trimming parameters

Example parameters for trimming FASTQ reads.
You set the location to: /usr/bin/java
Detected Java program in location: /usr/bin/java
Do you want to change the Java Path? [y/n] n
---------------------------------------------------------------------------
	*** Configuration part for Trimmomatic location (location folder) ***

The current status is: /software/Trimmomatic-0.38
Do you want to re-config this part? [y/n] n
--> Keeping the default value.
---------------------------------------------------------------------------
	*** Configuration part for Adapter ***
The current status is: /software/Trimmomatic-0.38/adapters/TruSeq3-PE.fa
Do you want to re-config this part? [y/n] n
--> Keeping the default value.
---------------------------------------------------------------------------
	*** Configuration part for running mode ***
The current status is: SE
Do you want to re-config this part? [y/n] n
--> Keeping the default value.
---------------------------------------------------------------------------
	*** Configuration part for ILLUMINACLIP ***
The current status is: 1:30:9
Do you want to re-config this part? [y/n] n
--> Keeping the default value.
---------------------------------------------------------------------------
	*** Configuration part for LEADING ***
The current status is: 20
Do you want to re-config this part? [y/n] n
--> Keeping the default value.
---------------------------------------------------------------------------
	*** Configuration part for TRAILING ***
The current status is: 20
Do you want to re-config this part? [y/n] n
--> Keeping the default value.
---------------------------------------------------------------------------
	*** Configuration part for SLIDINGWINDOW ***
The current status is: 4:20
Do you want to re-config this part? [y/n] n
--> Keeping the default value.
---------------------------------------------------------------------------
	*** Configuration part for MINLEN ***
The current status is: 36
Do you want to re-config this part? [y/n] n
--> Keeping the default value.
---------------------------------------------------------------------------
	*** Configuration part for Threading ***
The current status is: 8
Do you want to re-config this part? [y/n] n
--> Keeping the default value.

```
##### **Alignment parameters**
Configure 'Bismark' by selecting ``option '6'``. 

During the Bismark Alignment step, a Bisulfite genome will be created from the reference fasta for the first time.

The following settings are set as default for alignment using Bismark.

- -s/--skip : Skip (i.e. do not align) the first <int> reads or read pairs from the input. (Default: set as 0)
- -u/--upto : Only aligns the first <int> reads or read pairs from the input. (Default: set as 0)
- -N/--seedmms : Sets the number of mismatches allowed in a seed alignment during multiseed alignment (Default: set as 0)
- -L/--seedlen : Sets the length of the seed substrings to align during multiseed alignment (Default: set as 20)
- Bismark Nucleotide option calculates the mono- and di-nucleotide sequence composition of covered positions in the analysed BAM file and compares it to the genomic average composition.

Edit other settings by typing [y/n].

Bismark includes tools for deduplication, based on identical genomic mapping.This tool will remove alignments to the same position in the genome from the Bismark mapping output, which can arise by e.g. excessive PCR amplification.Output is in BAM format.

Bismark methylation extractor will extract Context-dependent (CpG/CHG/CHH) methylation calls. 

```
6. Alignment parameters

Example parameters for aligning FASTQ reads.

	*** Alignment parameters (Bismark mapper) ***
You set the location to: /software/Bismark
Do you want to change the location? [y/n] n
We will keep the default value!
---------------------------------------------------------------------------
	*** Configuration part for Bismark Parallel ***
The current status is: 8
Do you want to re-config this part? [y/n] n
--> Keeping the default value.
---------------------------------------------------------------------------
	*** Configuration part for Bismark buffer Size ***
The current status is: 40
Do you want to re-config this part? [y/n] n
--> Keeping the default value.
---------------------------------------------------------------------------
	*** Configuration part for Bismark Nucleotide ***
	**** To change the Nucleotide report option please Enable it.***
The current status is: Disabled
Do you want to re-config this part? [y/n] n
--> Keeping the default value.

```
##### **Imputation of missing cytosines using Methimpute**

Select ``option '7'`` to edit the parameters for running Methimpute.
Methimpute implements a HMM-based binomial test for methylation status calling. It achieves this by borrowing information from neighboring covered cytosines. The confidence in the methylation status call is reported as well.

The following settings can be edited by typing [y/n].

- Run model with Intermediate status of Cytosines. Cytosines will be assigned as Methylated, Intermediate and Unmethylated.
- Methylation level around Genes and transposable elements will be plotted

```
7. Methimpute parameters

Example parameters for running HMM model and generating Methimpute output files.

	*** Include Intermediate status ***

The current status is: Enabled
Do you want to re-config this part? [y/n] y

1- Enable this option.
2- Disable this option.
Please enter the number to select:1

Please specify: independent or constrained 
1 - Independent
2 - Constrained

Please enter the number to select:1
--> Configuration updated!
---------------------------------------------------------------------------
	*** Model Fit reports ***
The current status is: Enabled
Do you want to re-config this part? [y/n] n
--> Keeping the default value.
---------------------------------------------------------------------------
	*** Plot Enrichment (Genes, TEs) ***
The current status is: Enabled
Do you want to re-config this part? [y/n] n
--> Keeping the default value.
---------------------------------------------------------------------------
	*** Output full report (Genes,TEs) ***
The current status is: Enabled
Do you want to re-config this part? [y/n] n
--> Keeping the default value.
---------------------------------------------------------------------------
	*** Run Context: All/ CG| CHG| CHH  ***
The current status is: All
Do you want to re-config this part? [y/n] n
--> Keeping the default value.
---------------------------------------------------------------------------
	*** Minimum read coverage value (just for quick run) ***
The current status is: 1
Do you want to re-config this part? [y/n] n
--> Keeping the default value.

```
##### **Set Parallel mode**
Set parallel mode for Trimmomatic, Bismark-alignment, Bismark-deduplicate removal, Bismark-methylation calling steps. This parallel option works independently of inbuilt parallel processing used by the above tools.

##### **See configured parameters**
Get an overview of configured parameters by selecting ``option '10'``.

```
9. See configured parameters

Here is summary of configuration parameters: 

- RAW files location: /home/user/raw-dataset
- Number and Size of the data-set: 8 Files and Total size: 18.0 Gigabyte
- The directory of results: /home/user
- Genome folder location: /home/user/TAIR10
     -- Genome Reference name: TAIR10_chr_all.fa
- Paired End: Enabled
- Trimmomatic location: /home/user/software/Trimmomatic-0.38
     -- JAVA path: /usr/bin/java
     -- ILLUMINACLIP: software/Trimmomatic-0.38/adapters/TruSeq3-SE.fa:1:30:9
     -- LEADING: 20
     -- TRAILING: 20
     -- SLIDINGWINDOW: 4:20
     -- MINLEN: 36
     -- Number of Threads: 8
- QC-Fastq path: software/FastQC/fastqc
- Bismark parameters: /home/user/software/Bismark_v0.20.0
     -- Nucleotide status: false
     -- Number of Parallel: 8 Threads.
     -- Buffer size: 40 Gigabyte.
     -- Samtools Path: /bin/samtools
     -- Intermediate for MethExtractor: Enabled
- Methylation extraction parameters( Only for quick run)
     -- Minimum read coverage: 1
- Methimpute Part:
     -- Methimpute Intermediate: Enabled
     -- Methimpute probability(Intermediate): constrained
     -- Methimpute Fit reports: Enabled
     -- Methimpute Enrichment plots: Disabled
     -- Methimpute TEs reports: Enabled
     -- Methimpute genes reports: Enabled
     -- Methimpute Context: All
- Parallel mode is: Enabled
     -- Number of Parallel: 4 Cores.
- E-mail notification: Disabled

```
``Return to main Menu``

***

