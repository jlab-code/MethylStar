---
output:
  html_document: default
  pdf_document: default
---
<img src="MethylStar_logo.png" alt="drawing" width="250"/>

### An efficient and flexible pipeline for population-level analysis of Whole Genome Bisulfite Sequencing (WGBS) data

MethylStar is a comprehensive, fast and flexible pipeline specifically suited for processing large amounts of WGBS data. It provides a user-friendly interface for experts/non-experts that runs on a Unix based enviroment MethylStar offers multithreading and multi-core processing support during aligning and Methylation Calling steps. Greater flexibility to the user to adjust parameters, execute and re-execute individual steps in the pipeline are offered. MethylStar is faster than several existing pipelines.


**Pipeline Steps**

To process a large number of WGBS samples in a consistent, documented and reproducible manner it is advisable to use a pipeline system. Here our pipeline comprises of custom bash scripts together with pre-installed softwares such as:

(1) Trimmomatic-0.36 : A flexible read trimming tool (Java based) for Illumina NGS data

(2) Bismark-v0.19.0 : Bismark is a program to map bisulfite treated sequencing reads to a genome of interest (in our case Arabidopsis thaliana) and perform methylation calls. Bisulfite treated reads are mapped using the short read aligner Bowtie 2, and  therefore it  is  a  requirement  that  Bowtie 1 or  Bowtie  2 are also installed on your machine. Bismark also requires SAMtools to be pre-installed on the computer.

(3) Bowtie 1.2.2: An ultrafast, memory-efficient short read aligner.

(4) FastQC : A Java based quality control tool for high throughput sequence data.

(5) Methimpute: A R package for imputation of DNA methylation from WGBS data

(6) SAMtools : Samtools is a suite of programs for interacting with high-throughput sequencing data



**MethylStar Interface**

We provide a visual (TUI) interface which is created with Python using the Npyscreen package. This makes it easy and intuitive to run all steps in the pipeline.

(1) Installation
- Python2 and R > 3.5.1
    - Package required for Python2: Npyscreen - https://pypi.org/project/npyscreen/
<br />
<br />

- FastQC - https://github.com/s-andrews/FastQC
<br />
<br />

- Trimmomatic - http://www.usadellab.org/cms/?page=trimmomatic
    - Java JDK - https://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html
<br />
<br />

- Bismark - https://github.com/FelixKrueger/Bismark
    - Samtools - http://www.htslib.org/
    - Bowtie - http://bowtie-bio.sourceforge.net/index.shtml
<br />
<br />

- METHimpute - https://github.com/ataudt/methimpute

<br />

(2) Configuration
<br />
<br />
(3) Running
<br />
<br />

**Acknowlegdements**

http://www.johanneslab.org/

* Main author
    * Yadi Shahryary - y.shahryary@tum.de

- Contributors:
    - Frank Johannes
    - Rashmi Hazarika
    - Talha Mubeen