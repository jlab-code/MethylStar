#!/usr/bin/env Rscript

source("./src/bash/r-lib.R")
library(doParallel)
library(data.table)
library(dplyr)
#-------------------------------------------------------------
# test if arguments are supplied
#-------------------------------------------------------------
args <- commandArgs(trailingOnly = TRUE)
wd = args[1] 
setwd(paste0(wd,"/","methylkit-format"))
#----------------------------------------------------
# function for reading methimpute files into Methylkit
#-----------------------------------------------------
readMethimputeForMethylkit <- function(filename) {
  cat(paste0("Reading Methimpute file: ", filename))
  MethOut <- fread(filename, skip = 0, header = TRUE)
  name <- gsub(pattern ="^.*?_","", basename(filename))
  cat(paste0("Starting...",name))
  chrs <- unique(MethOut[,c(seqnames)])
  chrs <- chrs[order(chrs)]
  df <- data.frame(
    chrBase = factor(MethOut[,c(paste0(seqnames,".",start))]),
    chr = factor(MethOut[,c(seqnames)], levels = chrs),
    base = as.integer(MethOut[,c(start)]),
    strand = factor(MethOut[,c(strand)], levels = c("+","-")),
    coverage = as.integer(MethOut[,c(counts.total)]),
    freqC = ifelse(MethOut[,c(counts.methylated)]==0 | MethOut[,c(counts.total)]==0, 0, 
                   MethOut[,c(counts.methylated/counts.total)]*100),
    freqT = ifelse(MethOut[,c(counts.methylated)]==0 | MethOut[,c(counts.total)]==0, 0,
                   MethOut[,c((1-counts.methylated/counts.total)*100)]))
  df$strand <- ifelse(df$strand=="+", "F", "R")
  fwrite(x=df, file=paste0(wd,"/methylkit-format/", "methylkit_", name),
         sep="\t", quote=FALSE, row.names=FALSE, col.names=TRUE)
  cat(paste0("Processing",name, " Finished."))
  fileConn<-"file-processed.lst"
  cat(filename, file = fileConn, append = TRUE, sep = "\n" )
}
#-------------------------------------------------------------
# converts methimpute files to methylkit format if donot exist
#-------------------------------------------------------------

try(system("ls -1v ../methimpute-out/*.txt > list-files.lst" ,intern = TRUE))
filenames <-fread("list-files.lst",skip = 0,header = FALSE)
files_to_go <-NULL
file_processed<-"file-processed.lst"
if (!file.exists(file_processed)){
  print("It's first time you are running the script! ")
  files_to_go <- filenames
} else {
  file_processed <-fread("file-processed.lst",skip = 0,header = FALSE)
  files_to_go <- as.data.table(anti_join (filenames , file_processed, by = c("V1")))
  print("Resuming the job...  ")
}
# if len(files_to_go)==0 --> nothing to do its done for all files before
print(paste0("Found: ",length(files_to_go$V1)," Files."))
no_cores <- detectCores() - 2  
cl <- makeCluster(no_cores, type="FORK")  
registerDoParallel(cl)  
result<-foreach(i=1:length(files_to_go$V1)) %dopar% readMethimputeForMethylkit(files_to_go$V1[i:i])
stopCluster(cl)  

rm(list=ls())
#gc(reset=TRUE)
