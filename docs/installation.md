Installation and Configuration MethylStar
================

###### *last update: 19-May-2020*

MethylStar is based on several softwares/tools therefore, it is necessary to have all dependencies to be pre-installed in your system and available in the PATH ( [A. Standard installation](#standard) ) or it can be installed as a docker image ( [B. Installation using docker](#docker) ). 

It is highly recommended to use a docker image as it simplifies the process of managing application processes in containers. Containers let you run your applications in resource-isolated processes. They’re similar to virtual machines, but containers are more portable, resource-friendly and dependent on the host operating system.

------------------------------------------------------------------------

#### [A. Standard Installation](#standard)

#### [B. Installation using Docker (recommended)](#docker)

------------------------------------------------------------------------

### <a name="standard" > A. Standard Installation </a>

###### *Approximate time ~ 30 minutes*

Before running MethylStar, you will need to install or check the installation of several packages.

##### Step A.1 — Installing Software (tested version with MethylStar)

- Python Ver.2 and R > 3.5.x
    
- FastQC (Ver. > 0.11.X  ) - https://github.com/s-andrews/FastQC
	
	Download: https://www.bioinformatics.babraham.ac.uk/projects/fastqc/fastqc_v0.11.8.zip
    
- Trimmomatic (Ver. > 0.38) - http://www.usadellab.org/cms/?page=Trimmomatic
	
	Download: http://www.usadellab.org/cms/uploads/supplementary/Trimmomatic/Trimmomatic-Src-0.39.zip
    
- Bismark (Ver. > 0.19.1 ) - https://github.com/FelixKrueger/Bismark
	
	Download: https://github.com/FelixKrueger/Bismark/archive/0.19.1.tar.gz
    
- METHimpute (Ver. > 1.6 ) - https://github.com/ataudt/methimpute
	
	In R use: BiocManager::install("methimpute")
    
- Samtools (Ver. > 1.9 ) - https://github.com/samtools/samtools.git

	Download: https://github.com/samtools/samtools/releases/download/1.9/samtools-1.9.tar.bz2
    
- bowtie2 (Ver. >  2.3.X ) - https://github.com/BenLangmead/bowtie2
	
	Download: https://github.com/BenLangmead/bowtie2/releases/download/v2.3.5.1/bowtie2-2.3.5.1-linux-x86_64.zip

- bedtools (Ver. >  2.29.X ) - https://bedtools.readthedocs.io/en/latest/
	
	In Ubuntu: sudo apt-get install bedtools
	
- (optional) BCF Tools (Ver.1.19 )

	Download https://github.com/samtools/bcftools/releases/download/1.9/bcftools-1.9.tar.bz2

- Htslib (Ver.1.9 )

	Download https://github.com/samtools/htslib/releases/download/1.9/htslib-1.9.tar.bz2 


We are testing MethylStar every month with the new version of software to make sure the stability and compatibility.

##### Step A.2 — Download MethylStar folder from github

``` bash
$ git clone https://github.com/jlab-code/MethylStar

```
##### Step A.3 — ‘cd’ into the MethylStar folder and type the following command

``` bash
python2 run.py
```
------------------------------------------------------------------------


### <a name="docker" > B. Installation using Docker </a>

*This tutorial based on Ubuntu 18.04*


###### *Approximate time ~ 10 minutes*


**(Optional)** Please follow the links in case if you need to install/config the Dcoker in your system. 


Get Docker CE for Ubuntu: https://docs.docker.com/v17.09/engine/installation/linux/docker-ce/ubuntu/


First tutorial: https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-18-04


Second tutorial: https://phoenixnap.com/kb/how-to-install-docker-on-ubuntu-18-04


**Step 1** —  Loading MethylStar docker image

###### *Approximate time ~ 10 minutes*

We prepared MethylStar docker image which is easiest way to import and run the Pipeline, in this case you don't need to wait to install the software.

Here you can download the image file and run by docker:

``` bash
$ wget http://jlabdata.org/methylstar.tar.gz
last update: 16-April-2020
file size: 1.1 Gb
md5sum: deffc84070dd2e5b671d0271f59442e4
```
**Step 2** — Import the image file into docker:

``` bash
$ docker load < methylstar.tar.gz
```

**Step 3** — Running docker file

Running the methylstar docker file.

``` bash
$ docker run --rm -it --privileged -v /PATH/TO/RAWDATA/:/data \
                 -v /PATH/TO/RESULT/FOLDER/:/results \
                 methylstar:latest
```

NOTE 1: Please change the */PATH/TO/RAWDATA/* according to the your raw files folder in your system.

NOTE 2: All the pipeline result will save in */PATH/TO/RESULT/FOLDER/* so please change the directory.

NOTE 3: Please do not change */data and /results*.

------------------------------------------------------------------------

 **(Optional)** Create image by docker file (advanced users)

###### *Approximate time ~ 20 minutes*

If you interested to install/add more package(s)/libraries into your docker image you can edit the Dockerfile to customize the image.

After edit the "Dockerfile" you should build the image from that file, please follow the commands bellow to build the docker image.

Step 1 — create folder eg: myDocker

``` bash
$ mkdir /home/$USER/myDocker
```

Step 2 — move the DockerFile into the direcotry.

``` bash
$ mv Dockerfile  /home/$USER/myDocker 
$ cd /home/$USER/myDocker
```

Step 3 — build the image.

``` bash
$ docker build -t methylstar .    # there is a 'dot' in the end of command.
```
Step 4 — run the docker image.
``` bash
$ docker run --rm -it --privileged -v /PATH/TO/RAWDATA/:/data \
                 -v /PATH/TO/RESULT/FOLDER/:/results \
                 methylstar:latest
```

------------------------------------------------------------------------

After running the docker file you will be in the main directory of pipeline, at this time all the software already installed and you have just run command:

``` bash
$ python2 run.py
```

[For more information about how to use the pipline Please follow this documentation.](runPipeline.md)
