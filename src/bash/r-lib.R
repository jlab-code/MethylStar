#!/usr/bin/env Rscript

# installing libraries
if(!any(installed.packages()[,"Package"]=="BiocInstaller") | !any(installed.packages()[,"Package"]=="BiocParallel"))
  source("https://bioconductor.org/biocLite.R")

list.of.packages = c("DMRcaller","GenomicRanges","devtools","annotatr","GenomicFeatures","methylKit","data.table","dplyr","ggplot2","doParallel","stringr")
new.packages = list.of.packages[!(list.of.packages %in% installed.packages()[,"Package"])]
if(length(new.packages)) BiocInstaller::biocLite(new.packages)

# libraries source file 
req_pkg<-function(packages){
  new.pkg <- list.of.packages[!(list.of.packages %in% installed.packages()[,"Package"])]
  if(length(new.pkg)) 
    install.packages(new.pkg)
  sapply(list.of.packages, require, character.only = TRUE)
}
req_pkg(list.of.packages)



list.pkg<- c("methimpute")
req_pkg<-function(packages){
  new.pkg <- list.pkg[!(list.pkg %in% installed.packages()[,"Package"])]
  if(length(new.pkg))
  install_github("ataudt/methimpute")
  sapply(list.pkg, require, character.only = TRUE)
}
req_pkg(list.pkg)


