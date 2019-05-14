Running MethylStar pipeline
================

The pipeline can be run by typing the following command:

``` bash  
python2 run.py
```

MethylStar provides a visual (TUI) interface which is created with Python. This makes it easy and intuitive to run all steps in the pipeline.

An interactive screen will display the list of following options in the Main menu:




```
Run Pipeline (WGBS)
Output/Reports
Access Jbrowse
Clean-up files
Help

Configuration
```

**_User Controls:_**

**_1: Individual steps of the pipeline can be executed by navigating to the specific step and pressing 'ENTER'._**

**_2: For each individual step, parameters can be set by clicking on the popup menu._**

**_3: The user can return back to the main form by navigating or clicking the 'OK' button at the bottom of the screen and pressing 'ENTER'._**

------------------------------------------------------------------------------------------


##### **1. Run Pipeline (WGBS)**
```
1. Run Trimmomatic
2. Run QC-Fastq-report
3. Run Bismark Mapper
4. Run QC-Bam report
5. Run Bismark-deduplicate
6. Run Bismark Meth.Extractor
7. Generate CX reports
8. Run Methimpute
```
The above options will be displayed upon navigating to 'Run Pipeline (WGBS)' and pressing 'ENTER'. Before running the pipeline, please check the parameters in 'Configuration' or configure them.

##### **2. Output/Reports**

All outputs from the pipeline run will be available in Output/Reports. This option allows the user to convert Methimpute outputs into bedgraph, bigwig and for input into DMRcallers (e,g Methylkit, DMRcaller).

##### **3. Access JBrowse**

Guest users can create an account for the first time by signing up on this site: 
http://jlabdata.org/signup

If you already have an account, please open the following URL in your web browser:
http://jlabdata.org/jbrowse

##### **4. Clean-up files**
In this part you can delete all the files that generated after running pipeline. Just select the item by number and will delete all content inside the target folder.

##### **5. Help**


##### **6. Configuration**

    Path: RAW files
    Path: Export results
    Path: Reference Genome
    Read-trimming parameters
    Path: QC-Fastq
    Alignment parameters
    Methimpute parameters
    Parallel mode

Before, running the pipeline, parameters for each individual step can be specified by navigating to the option 'Configuration'.
Ensure that specific PATHs to RAW files, output folders and reference genome exist.

--------------------------------------------------------------------------------------------------------
### Parameters for individual steps of the pipeline can be configured as follows:

> **Trimming parameters**

Parameters for trimming FASTQ reads. The following values are set as default.

(a) single/paired-end reads 
(b) no. of threads
(b) convert quality scores to phred33
(c) ILLUMINACLIP::::for e.g TruSeq3-SE.fa:1:30:9
(d) Remove leading low quality or N bases (below quality 20) (LEADING:20) 
(e) Remove trailing low quality or N bases (below quality 20) (TRAILING:20)
(f) SLIDINGWINDOW:: Perform a sliding window trimming, cutting once the average quality within the window falls below a threshold. for e.g SLIDINGWINDOW: 4:20 
(g) Drop the read if it is below a specified length for e.g MINLEN:36

> **Pre Alignment quality control**

Running fastQC on the trimmed fastq files provide a comprehensive assessment of the sequencing quality and any remaining adapter contamination.
    
> **Alignment using Bismark Mapper**

Start running bismark mapper on all the trimmed files using the following default parameters or changing accordingly. A Bisulfite genome will be created from the reference fasta for the first time.

(1) -s/--skip : Skip (i.e. do not align) the first <int> reads or read pairs from the input. (Default: set as 0)
(2) -u/--upto : Only aligns the first <int> reads or read pairs from the input. (Default: set as 0)
(3) -N/--seedmms : Sets the number of mismatches allowed in a seed alignment during multiseed alignment (Default: set as 0)
(4) -L/--seedlen : Sets the length of the seed substrings to align during multiseed alignment (Default: set as 20)
(5) use parallel
(6) --nucleotide_coverage : Calculates the mono- and di-nucleotide sequence composition of covered positions in the analysed BAM file and compares it to the genomic average composition once alignments are complete by calling 'bam2nuc'.
(7) --genome

> **Post Alignment quality control**

FASTQC is primarily for pre-alignment and it takes as input FASTQ or FASTA files. Here we will run fastQC on the BAM files to have a quick overview of the aligned files.

> **Run bismark deduplicate**

Bismark includes tools for deduplication, based on identical genomic mapping.
This tool is supposed to remove alignments to the same position in the genome from the Bismark mapping output (both single and paired-end files), which can arise by e.g. excessive PCR amplification. If sequences align to the same genomic position but on different strands they will be scored individually. 

(1) -s/--single : deduplicate single-end Bismark files
(2) --bam : output will be written in BAM format

> **Bismark methylation extractor**

Context-dependent (CpG/CHG/CHH) methylation calls will be extracted. The user can choose which reports should be generated. 

start the run with following default parameters or specify accordingly:

(1) -s/--single : input files are from single-end or paired-end read data
(2) --bedGraph : After finishing the methylation extraction, the methylation output is written into a sorted bedGraph file that reports the position of a given cytosine and its methylation state
(3) --CX/--CX_context : The sorted bedGraph output file contains information on every single cytosine that was covered in the experiment irrespective of its sequence context.
(4) --cytosine_report : After the conversion to bedGraph has completed, the option '--cytosine_report' produces a genome-wide methylation report for all cytosines in the genome.
(5) use --parallel
(6) --buffer_size : This allows you to specify the main memory sort buffer when sorting the methylation information.
(7) specify --genome_folder


> **Run Methimpute**

Impute DNA methylation from WGBS data. Methimpute implements a powerful HMM-based binomial test for methylation status calling. Besides improved accuracy over the classical binomial test, the HMM allows imputation of the methylation status of all cytosines in the genome. It achieves this by borrowing information from neighboring covered cytosines. The confidence in the methylation status call is reported as well. Methimpute also outputs context-specific conversion rates, which might be used to optimize the experimental procedure.

start the run with following parameters:

(1) Intermediate: Run model with Intermediate status of Cytosines. Cytosines will be assigned as Methylated, Intermediate and Unmethylated.
(2) Plot model fits
(3) Enrichment: Methylation level around Genes and transposable elements
(4) Specify the genome


