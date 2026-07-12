#!/usr/bin/env Rscript

# installing libraries
if (!requireNamespace("BiocManager", quietly = TRUE))
  install.packages("BiocManager")


list.of.packages = c("DMRcaller","GenomicRanges","devtools","annotatr","GenomicFeatures","data.table","dplyr","ggplot2","doParallel","stringr","Rhtslib","methylKit")
new.packages = list.of.packages[!(list.of.packages %in% installed.packages()[,"Package"])]
if(length(new.packages)) BiocManager::install(new.packages)

# libraries source file 
req_pkg<-function(packages){
  new.pkg <- list.of.packages[!(list.of.packages %in% installed.packages()[,"Package"])]
  if(length(new.pkg)) 
    install.packages(new.pkg)
  sapply(
		list.of.packages,
		function(pkg) suppressMessages(require(pkg, character.only = TRUE))
	)
}
req_pkg(list.of.packages)



list.pkg<- c("methimpute")
req_pkg<-function(packages){
  new.pkg <- list.pkg[!(list.pkg %in% installed.packages()[,"Package"])]
  if(length(new.pkg))
  install_github("ataudt/methimpute")
  sapply(
		list.pkg,
		function(pkg) suppressMessages(require(pkg, character.only = TRUE))
	)
}
req_pkg(list.pkg)
