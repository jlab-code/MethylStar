#!/usr/bin/env Rscript

source("./src/bash/r-lib.R")
library(doParallel)
library(data.table)
library(dplyr)
library(DMRcaller)

args <- commandArgs(trailingOnly = TRUE)
wd = args[1] 
setwd(paste0(wd,"/","dmrcaller-format"))

#------------------------------------------------------------
# creating a list

files_to_go <-NULL
file_processed<-"list-files.lst"
if (file.exists(file_processed)){
  print("Found the list of files ...")
} else {
  try(system("ls -1v ../methimpute-out/*.txt > list-files.lst" ,intern = TRUE))
  print("creating list of methimpute-out files... ")
}
list_files <-fread("list-files.lst",skip = 0,header = FALSE)
# if len(files_to_go)==0 --> nothing to do its done for all files before
print(paste0("Found: ",length(list_files$V1)," Files."))

#------------------------------------------------------------
# reading Methimpute output instead of cx-report
#------------------------------------------------------------
readMethimpute <- function(filename) {
  cat(paste0("Reading Methimpute file: ", filename))
  MethOut <- fread(filename, skip = 0, header = TRUE)
  chrs <- unique(MethOut[,c(seqnames)])
  chrs <- chrs[order(chrs)]
  cat("\nconstracting data-frame... ")
  df <- data.frame(
    chr = factor(MethOut[,c(seqnames)], levels = chrs), 
    pos = as.integer(MethOut[,c(start)]),
    strand = factor(MethOut[,c(strand)], levels = c("+","-")),
    context = factor(MethOut[,c(context)], levels = c("CG","CHG","CHH")),
    trinucleotide_context = MethOut[,c(context.trinucleotide)],
    readsM = as.integer(MethOut[,c(counts.methylated)]),
    readsN = as.integer((MethOut[,c(counts.total)])))
  cat("\nConverting to Grange objects... ")
  df <- GRanges(seqnames = df$chr, 
                ranges = IRanges(start = df$pos, end = df$pos),
                strand = df$strand, context = df$context, 
                readsM = df$readsM,
                readsN = df$readsN,
                trinucleotide_context = df$trinucleotide_context)
  cat("\nFinished reading file: ", filename, "\n", sep="")
  return(df)
}

#filenames <- list_files #list.files(paste0(wd,"/methimpute-out"), pattern='\\.txt$', full.names = TRUE)
DataList <- vector(mode="list", length=0)
for (i in seq_along(list_files$V1)){
  input_file <- list_files$V1[i:i]
  name <- gsub(pattern = "\\.txt", "", basename(input_file))
  DataList[[name]] <- readMethimpute(input_file)
}
cat("Finished reading all Methimpute files!", "\n")
current<-format(Sys.time(), "%Y_%m_%d_%H_%M")
Dmr_format<-assign(paste0("dmr_",current),DataList)
cat("\nSaving as RData files...")
save(Dmr_format, file=paste0(wd,"/dmrcaller-format/","dmr_",current,".RData"))
cat("\n",paste0("Converting done! You can find the files in this path: ", wd,"/dmrcaller-format/" ))
rm(list=ls())
#gc(reset=TRUE)



