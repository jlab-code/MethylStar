#!/usr/bin/env Rscript

source("./src/bash/r-lib.R")
library(doParallel)

#----------------------------------------------
# test if arguments are supplied
#-------------------------------------------------------------
args <- commandArgs()
try(system("ls -1v ../methimpute-out/*.txt > list-files.lst" ,intern = TRUE))
fileName <-fread("list-files.lst",skip = 0,header = FALSE)

# wd = args[6]  # result pipeline folder
# statistic = args[7]
# nCores = as.numeric(args[8])
# OutputFolder = args[9]
# Cytosine_context = args[10]
# q = as.numeric(args[11])
# diff = as.numeric(args[12])
# qv = as.numeric(args[13])
# mc = as.numeric(args[14])
# lo_count= args[15]
# lo_perc = args[16]
# hi_count = args[17]
# hi_perc = args[18]
# win = as.numeric(args[19])
# step = as.numeric(args[20])
#-----------------------------------------------------------------------------
library(doParallel)
library(data.table)
library(dplyr)
wd = "/home/yadi/TESTING/result_test_pipeline"  # result pipeline folder
statistic = "Fishers.testDMB"
nCores = 4
OutputFolder = "/home/yadi/TESTING/result_test_pipeline/methylkit-output"
Cytosine_context = "CpG"
q = 0.01
diff = 25
qv = .01
mc = 25
lo_count= 10
lo_perc = NULL
hi_count = NULL
hi_perc = 99.9
win = 1000
step = 1000




print(args)
#----------------------------------------------------
# function for reading methimpute files into Methylkit
#-----------------------------------------------------
readMethimputeForMethylkit <- function(filename) {
  print(paste0("Reading Methimpute file: ", filename))
  MethOut <- fread(filename, skip = 0, header = TRUE)
  name <- gsub(pattern ="^.*?_","", basename(filename))
  print(name)
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
}
#-------------------------------------------------------------
# converts methimpute files to methylkit format if donot exist
#-------------------------------------------------------------
setwd(paste0(wd,"/","methylkit-format"))
#filenames <-list.files(paste0(wd,"/methimpute-out"), pattern='\\.txt$', full.names = TRUE)
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
print(paste0("Found: ",length(files_to_go$V1))," Files.")

  for (i in 1:length(files_to_go$V1)){
    going_file <- files_to_go$V1[i:i]
    readMethimputeForMethylkit(going_file)
    fileConn<-"file-processed.lst"
    cat(going_file, file = fileConn, append = TRUE, sep = "\n" )
    print(paste0("Converted file", going_file))
    }

no_cores <- detectCores() - 1  
cl <- makeCluster(no_cores, type="FORK")  
registerDoParallel(cl)  
result<-foreach(i=1:length(files_to_go$V1)) %dopar% readMethimputeForMethylkit(files_to_go$V1[i:i])
stopCluster(cl)  


rm(list=ls())
gc(reset=TRUE)
