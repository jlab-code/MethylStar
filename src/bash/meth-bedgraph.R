#!/usr/bin/env Rscript
rm(list=ls())
options(warn=-1)
source("./src/bash/r-lib.R")
#-------------------------------------------------------------
# test if arguments are supplied
#-------------------------------------------------------------
args <- commandArgs(trailingOnly = TRUE)
wd = args[1] 
setwd(paste0(wd,"/bedgraph-format/"))

#----------------------------------------------------
# function for reading methimpute files into Methylkit
#-----------------------------------------------------
MethimputeTobedGraph <- function(file1, chrom_sizes) {
  cat(paste0("Reading Methimpute file: ", file1))
  fname <- fread(file1, skip = 1, select = c("V1","V2","V3","V4","V9"))
  fname <- fname %>% filter(fname$V1 != "M" & fname$V1 != "C")
  fChrlen <- fread(chrom_sizes, skip = 0, header = FALSE)
  name <- gsub(pattern = "\\.txt$", "", basename(file1))
  context <- c("CG","CHG","CHH")

  mycontext <- lapply(context, function(x){
    print(paste0("Running for context... ", x))
    fn <- fname %>% filter(fname$V4==x)
    name <- gsub(pattern = "\\.txt$", "", basename(file1))
    chrs <- unique(fn$V1)
    chrs <- chrs[order(chrs)]
    df <- data.frame(
      chr = factor(fn$V1, levels = chrs), 
      pos_start = as.integer(fn$V2),
      meth_lvl = ifelse(fn$V3 == "-", as.numeric(fn$V9) * -1, as.numeric(fn$V9)))
    df$pos_end <- df$pos_start+1
    
    print(paste0("Filter out rows that exceed chr length... ", name))
    Chr <- fChrlen$V1
    Chrlen <- fChrlen$V2
    dfnew <- lapply(1:length(Chr), function(x) {
      dplyr::filter(df, df$chr==Chr[x] & df$pos_end<=Chrlen[x])
      })

    dfnew <- do.call("rbind", dfnew)
    dfnew <- dfnew[,c("chr","pos_start","pos_end","meth_lvl")]
    print(paste0("Building data-set format...",name))
    dfnew$pos_start <- format(dfnew$pos_start, scientific = FALSE) 
    dfnew$pos_end <- format(dfnew$pos_end, scientific = FALSE)
    print(paste0("Writing to bedGraph format....",name))
    fwrite(x= dfnew, file=paste0(name,"-", x,".bedGraph"), sep="\t", 
           quote=FALSE, row.names=FALSE, col.names=FALSE)

  fileConn<-paste0("file-processed.lst")
  cat(file1, file = fileConn, append = TRUE, sep = "\n" )
})
}


#-------------------------------------------------------------
# converts methimpute files to methylkit format if donot exist
#-------------------------------------------------------------

try(system("ls -1v ../methimpute-out/*.txt > list-files.lst", intern = TRUE))

chrom_sizes <-list.files("../rdata/", pattern='\\.txt$', full.names = TRUE)

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
print(paste0("Max. of cores to use to proccess the files: ",no_cores))
cl <- makeCluster(no_cores, type="FORK")  
registerDoParallel(cl)
result<-foreach(i=1:length(files_to_go$V1)) %dopar% MethimputeTobedGraph(files_to_go$V1[i:i],chrom_sizes)
stopCluster(cl)  
print("Cleaning list and workspace.")
print("Proccessing files done!")
rm(list=ls())
#gc(reset=TRUE)
