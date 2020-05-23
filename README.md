
# ![shahryary/MethylStar](docs/MethylStar_logo.png)



### A fast and robust pre-processing pipeline for bulk or single-cell whole-genome bisulfite sequencing (WGBS) data

To process a large number of WGBS samples in a consistent, documented and reproducible manner it is advisable to use a pipeline system. MethylStar is a fast, stable and flexible pre-processing pipeline for bulk or single-cell (de-multiplexed) WGBS data.

**Key features**

(1) MethylStar provides a user-friendly interface for experts/non-experts that runs on a Unix based environment.

(2) Offers efficient memory usage and multithreading/multi-core processing support during all pipeline steps.

(3) Greater flexibility to the user to adjust parameters, execute and re-execute individual steps.

(4) Generates standard outputs for downstream analysis (formats compatible with DMR-callers such as Methylkit, DMRcaller) and visualisation on genome browsers (bedGraph/BigWig).

**Pipeline Steps**

In its current implementation, MethylStar comprises of the following core NGS components:

(A) Trimmomatic: A flexible read trimming tool (Java based) for processing of raw fastq reads for both single- and paired-end data.

(B) Bismark: Alignment, removal of PCR duplicates and cytosine context extraction steps are performed with the Bismark software suite. Alignments can be performed for both WGBS and Post Bisulfite Adapter tagging (PBAT) approaches for single-cell libraries. Bisulfite treated reads are mapped using the short read aligner Bowtie 2, and therefore it is a requirement that Bowtie 1 or Bowtie 2 are also installed on your machine. Bismark also requires SAMtools to be pre-installed on the computer.

(C) FastQC and bedtools: Tools for assessing data quality.

(D) METHimpute: Cytosine-level methylation calls can be obtained with METHimpute, a Bioconductor package for inferring the methylation status/level of individual cytosines, even in the presence of low sequencing depth and/or missing data.

*Note: For information on specific software versions, please refer to [Installation and Configuration](docs/installation.md) section.*

### Documentation

1. [Installation and Configuration](docs/installation.md)
2. [Running The Pipeline](docs/runPipeline.md)
3. [MethylStar tutorial on YouTube](#MethylStar_tutorial_on_YouTube)<a name="MethylStar_tutorial_on_YouTube"> (https://www.youtube.com/watch?v=ll8mbPjVwnM)
<!-- 5. [FAQs](docs/faq.md) --->

### Contributors:

- Yadi Shahryary - y.shahryary@tum.de
- Rashmi Hazarika - rashmi.hazarika@tum.de
- Frank Johannes - frank@johanneslab.org
