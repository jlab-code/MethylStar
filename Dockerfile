#Download base image ubuntu 18.04
FROM ubuntu:18.04

MAINTAINER Yadi Shahryary <shahryary@gmail.com>
LABEL version="1.1"
LABEL description="MethylStar Dockerfile."

#---------------------------------------------
# Update Ubuntu Software repository
#---------------------------------------------
RUN apt-get update
RUN apt-get install -y build-essential
RUN apt-get install -y openjdk-11-jdk
RUN apt-get install -y openjdk-11-jre
RUN apt-get install -y curl
RUN apt-get install -y unzip
RUN apt-get install -y bowtie2
RUN apt-get install -y gnupg2
RUN apt-get install -y software-properties-common
RUN apt-get install -y aptitude
RUN apt-get install -y libcurl4-openssl-dev
RUN apt-get install -y libcurl4-gnutls-dev
RUN apt-get install -y libxml2-dev
RUN apt-get install -y libgit2-dev
RUN apt-get install -y libssl-dev
RUN apt-get install -y git
RUN apt-get install -y python 
RUN apt-get install -y python-pip
RUN apt-get install -y libncurses-dev
RUN apt-get install -y zlib1g-dev
RUN apt-get install -y libbz2-dev
RUN apt-get install -y liblzma-dev
RUN apt-get install -y parallel
RUN apt-get install -y wget
RUN apt-get install -y vim
RUN apt-get install -y tmux
RUN apt-get install -y screen
RUN apt-get install -y htop
# cleanup
RUN apt-get -y autoremove

#RUN pip install --upgrade pip
#RUN pip install npyscreen

#---------------------------------------------
# preparing directories 
RUN mkdir -p /home/software
WORKDIR /home/software

#---------------------------------------------
# SAM tools V.19
#---------------------------------------------
RUN wget https://github.com/samtools/samtools/releases/download/1.9/samtools-1.9.tar.bz2
RUN tar -xvf samtools-1.9.tar.bz2
WORKDIR samtools-1.9/
RUN mkdir -p /home/software/samtools
RUN ./configure --prefix=/home/software/samtools
RUN make
RUN make install
ENV PATH "$PATH:/home/software/samtools/bin/samtools"
WORKDIR /home/software/

#---------------------------------------------
# BCF TOOLS V.19
#---------------------------------------------
RUN wget https://github.com/samtools/bcftools/releases/download/1.9/bcftools-1.9.tar.bz2
RUN tar -xvf bcftools-1.9.tar.bz2
WORKDIR bcftools-1.9/
RUN mkdir -p /home/software/bcftools
RUN ./configure --prefix=/home/software/bcftools
RUN make
RUN make install
ENV PATH "$PATH:/home/software/bcftools/bin"
WORKDIR /home/software/

#---------------------------------------------
# HTSLIB V.19
#---------------------------------------------
RUN wget https://github.com/samtools/htslib/releases/download/1.9/htslib-1.9.tar.bz2
RUN tar -xvf htslib-1.9.tar.bz2
WORKDIR htslib-1.9/
RUN mkdir -p /home/software/htslib
RUN ./configure --prefix=/home/software/htslib
RUN make
RUN make install
ENV PATH "$PATH:/home/software/htslib/bin"
WORKDIR /home/software/

#--------------------------------
# Trimmomatic 0.38
#--------------------------------
RUN wget http://www.usadellab.org/cms/uploads/supplementary/Trimmomatic/Trimmomatic-0.38.zip
RUN unzip Trimmomatic-0.38.zip
RUN chmod +x -R Trimmomatic-0.38/
WORKDIR /home/software/

#--------------------------------
# Bismark V 0.20.1
#--------------------------------
RUN wget https://github.com/FelixKrueger/Bismark/archive/0.20.1.zip
RUN unzip 0.20.1.zip
RUN chmod +x -R Bismark-0.20.1/

#--------------------------------
# FASTQC V.0.11.8
#--------------------------------
RUN wget https://www.bioinformatics.babraham.ac.uk/projects/fastqc/fastqc_v0.11.8.zip
RUN unzip fastqc_v0.11.8.zip
RUN chmod +x -R FastQC

#--------------------------------
RUN rm *.bz2
RUN rm *.zip

#--------------------------------
# R and libraries V.0.11.8
#--------------------------------
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E298A3A825C0D65DFD57CBB651716619E084DAB9
RUN add-apt-repository 'deb https://cloud.r-project.org/bin/linux/ubuntu bionic-cran35/'
RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y tzdata
RUN apt-get -y install r-base

RUN R -e "install.packages('BiocManager', version = '3.9')"
RUN R -e "library("BiocManager"); BiocManager::install('data.table')"
RUN R -e "library("BiocManager"); BiocManager::install('devtools')"
RUN R -e "library("BiocManager"); BiocManager::install('dplyr')"
RUN R -e "library("BiocManager"); BiocManager::install('ggplot2')"
RUN R -e "library("BiocManager"); BiocManager::install('doParallel')"
RUN R -e "library("BiocManager"); BiocManager::install('stringr')"
RUN R -e "library("BiocManager"); BiocManager::install('DMRcaller')"
RUN R -e "library("BiocManager"); BiocManager::install('GenomicRanges')"
RUN R -e "library("BiocManager"); BiocManager::install('annotatr')"
RUN R -e "library("BiocManager"); BiocManager::install('GenomicRanges')"
RUN R -e "library("BiocManager"); BiocManager::install('Rhtslib')"
RUN R -e "library("BiocManager"); BiocManager::install('methylKit')"
RUN R -e "library("devtools"); install_github('ataudt/methimpute')"

#--------------------------------
# Pipeline and preparing directories
#--------------------------------
WORKDIR /home/
RUN git clone https://github.com/jlab-code/MethylStar.git
WORKDIR /home/MethylStar/
RUN rm config/pipeline.conf
RUN mv config/pipeline.conf.Docker config/pipeline.conf

RUN mkdir -p /home/shared/reference_genome
RUN chown -R root:root /home/shared/reference_genome
RUN chmod ugo+rxw -R /home/shared/reference_genome

#RUN wget http://10.162.143.56/refgenome/TAIR10_chr_all.fa
RUN wget http://jlabdata.org/refgenome/TAIR10_chr_all.fa
RUN chmod +x TAIR10_chr_all.fa
RUN mv TAIR10_chr_all.fa /home/shared/reference_genome

RUN mkdir -p /data
RUN chmod 777 -R /data







