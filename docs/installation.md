Installation and Configuration MethylStar
================

###### *last update: NOV-15-2019*

MethylStar is based on several softwares/tools therefore, it is necessary to have all dependencies to be pre-installed in your system and available in the PATH ( [A. Standard installation](#standard) ) or it can be installed as a docker image ( [B. Installation using docker](#docker) ). 

It is highly recommended to use a docker image as it simplifies the process of managing application processes in containers. Containers let you run your applications in resource-isolated processes. They’re similar to virtual machines, but containers are more portable, resource-friendly and dependent on the host operating system.

------------------------------------------------------------------------

#### [A. Standard Installation](#standard)

#### [B. Installation using Docker (recommended)](#docker)

------------------------------------------------------------------------

### <a name="standard" > A. Standard Installation </a>

###### *Approximate time ~ 30 minutes*

Before running MethylStar, you will need to install or check the installation of several packages.

##### Step A.1 — Installing Software

- Python Ver.2 and R > 3.5.x
    
- FastQC (Ver. > 0.11.X  ) - https://github.com/s-andrews/FastQC  
    
- Trimmomatic (Ver. > 0.38) - http://www.usadellab.org/cms/?page=trimmomatic
    
- Bismark (Ver. > 0.19 ) - https://github.com/FelixKrueger/Bismark
    
- METHimpute (Ver. > 1.6 ) - https://github.com/ataudt/methimpute
    
- Samtools (Ver. > 1.9 ) - https://github.com/samtools/samtools.git 
    
- bowtie2 (Ver. >  2.3.X ) - https://github.com/BenLangmead/bowtie2



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


**Step 1** — install a few prerequisite packages which let apt use packages over HTTPS:

###### *Approximate time ~ 10 minutes*

Note: Skip steps 1 and 2 in case that you already installed docker program.

``` bash
$ sudo apt update
$ sudo apt install apt-transport-https ca-certificates curl software-properties-common
$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
$ sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable"
$ sudo apt update
```

Finally, install Docker:

``` bash
$ sudo apt install docker-ce
```

**Step 2**  — **(Optional)** Executing the Docker Command Without Sudo permission. 

If you want to avoid typing sudo whenever you run the docker command, add your username to the docker group:

``` bash
$ sudo usermod -aG docker ${USER}
$ su - ${USER}
```

**Step 3** —  Loading MethylStar docker image

###### *Approximate time ~ 10 minutes*

We prepared MethylStar docker image which is easiest way to import and run the Pipeline, in this case you don't need to wait to install the software.

Here you can download the image file and run by docker:

``` bash
$ wget http://jlabdata.org/methylstar.tar.gz
last update: NOV-15-2019
file size: 1.1 Gb
md5sum: 1d5f5f841b759d516b0f490be36995b3
```
**Step 4** — Import the image file into docker:

``` bash
$ docker load < methylstar.tar.gz
```

**Step 5** — Running docker file

Running the methylstar docker file.

``` bash
$ docker run --rm -it --privileged -v /PATH/TO/RAW-FILES/:/data \
                 -v /PATH/TO/results/:/results \
                 methylstar:ver.1.4
```

NOTE 1: Please change the */PATH/TO/RAW-FILES/* according to the your raw files folder in your system.

NOTE 2: All the pipeline result will save in */PATH/TO/results/* so please change the directory.

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

------------------------------------------------------------------------

After running the docker file you will be in the main directory of pipeline, at this time all the software already installed and you have just run command:

``` bash
$ python2 run.py
```

[For more information about how to use the pipline Please follow this documentation.](runPipeline.md)
