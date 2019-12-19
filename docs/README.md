# ![shahryary/MethylStar](docs/MethylStar_logo.png)

### An efficient and flexible pipeline for population-level analysis of WGBS data

To process a large number of WGBS samples in a consistent, documented and reproducible manner it is advisable to use a pipeline system. MethylStar is a comprehensive, fast and flexible pipeline specifically suited for processing large amounts of BS-Seq datasets.

(1) It provides a user-friendly interface for experts/non-experts that runs on a Unix based enviroment.

(2) MethylStar offers multithreading and multi-core processing support during aligning and Methylation Calling steps.

(3) Greater flexibility to the user to adjust parameters, execute and re-execute individual steps.

**Pipeline Steps**

Here our pipeline comprises of custom bash scripts together with pre-installed softwares such as:

(A) Trimmomatic-0.36 : A flexible read trimming tool (Java based) for Illumina NGS data

(B) Bismark-v0.19.0 : Bismark is a program to map bisulfite treated sequencing reads to a genome of interest and perform methylation calls. Bisulfite treated reads are mapped using the short read aligner Bowtie 2, and  therefore it  is  a  requirement  that  Bowtie 1 or  Bowtie  2 (c) are also installed on your machine. Bismark also requires SAMtools (f) to be pre-installed on the computer.

(C) Bowtie 1.2.2: An ultrafast, memory-efficient short read aligner.

(D) FastQC : A Java based quality control tool for high throughput sequence data.

(E) Methimpute: A R package for imputation of DNA methylation from WGBS data

(F) SAMtools : Samtools is a suite of programs for interacting with high-throughput sequencing data.

### Documentation

1. [Installation and Configuration](installation.html)
2. [Running The Pipeline](runPipeline.html)
<!-- 3. [Interpret Outputs/Results](docs/directory.md) -->
<!-- 5. [FAQs](docs/faq.md) --->


### Contributors:

- Yadi Shahryary - y.shahryary@tum.de
- Rashmi Hazarika - rashmi.hazarika@tum.de
- Frank Johannes - frank@johanneslab.org