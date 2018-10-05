#!/usr/bin/env Rscript

source("./src/bash/r-lib.R")

# reading base directory from config.cfg
args <- commandArgs()
#print(args)
wd=(args[6])          # result direcory
setwd(paste0(wd,"/","methimpute-out"))
genome_ref=(args[7])  # genome reference directory
name_genome=(args[8]) # name of genome
rdata=(args[9])       # file for genes/TEs/etc.(annotation files)
intermediate<-as.logical(toupper((args[10])))

#regenerating new list of CX files to process
#system('chmod a+x list-files.txt')
try(system("ls -1v ../cx-reports/*.txt > list-files.lst" ,intern = TRUE))
fileName <-fread("list-files.lst",skip = 0,header = FALSE)

#-------------------------------------------------
# Modifying the main writing function from "write.table" to "fwrite" in data.table
#-------------------------------------------------
modifiedexportMethylome <- function( model, filename, original_file) {
  data <- model$data
  df <-  methods::as(data, 'data.frame')
  df <- df[,c('seqnames', 'start', 'strand', 'context', 'counts.methylated', 'counts.total', 'posteriorMax', 'posteriorMeth', 'posteriorUnmeth', 'status','rc.meth.lvl')]
  #df$seqnames <- as.numeric(as.character(df$seqnames))
  # ------------ reading CX file
  col.names <- c("seqnames","start","context.trinucleotide")
  Cx <- fread(original_file, skip=0, sep='\t', col.names =col.names, select=c(1,2,7) )
  #Cx$seqnames <- as.numeric(as.character(Cx$seqnames))
  # applying CX column
  final_dataset <- df %>% left_join(Cx, by = c("seqnames", "start"))
  #------------------------
  # dropping columns 
  drops <- c("posteriorMeth","posteriorUnmeth")
  final_dataset<- final_dataset[ , !(names(final_dataset) %in% drops)]
  #------------------------------------------------------------------
  # converting to M,I,U to save in size
  # converting chachter to M,U,I
  final_dataset <- data.frame(lapply(final_dataset, function(x) {
    gsub("Intermediate", "I", x)
  }),stringsAsFactors=F)
  
  final_dataset <- data.frame(lapply(final_dataset, function(x) {
    gsub("Methylated", "M", x)
  }),stringsAsFactors=F)
  #----------------------------
  final_dataset <- data.frame(lapply(final_dataset, function(x) {
    gsub("Unmethylated", "U", x)
  }),stringsAsFactors=F)
  
 
  #-------------------------------------------------------------
  # take 4 digit of decimal value posteriorMax column 
  floor_dec <- function(x, level=1) round(x - 5*10^(-level-1), level)
  final_dataset$posteriorMax <-floor_dec(as.numeric(as.character(final_dataset$posteriorMax)),4)
  final_dataset$rc.meth.lvl <-floor_dec(as.numeric(as.character(final_dataset$rc.meth.lvl)),4)
  
  #--------------------------------------------------------------
  #final_dataset<-as.data.table(final_dataset)
  fwrite(final_dataset,file = filename, quote = FALSE, sep ='\t', row.names = FALSE, col.names = TRUE)
  rm(data,df,Cx,final_dataset)
}
#-------------------------------------------------


files_to_go <-NULL
file_processed<-"file-processed.lst"
if (!file.exists(file_processed)){
  print("It's first time you are running the script! ")
  files_to_go <- fileName
} else {
  file_processed <-fread("file-processed.lst",skip = 0,header = FALSE)
  files_to_go <- as.data.table(anti_join (fileName , file_processed, by = c("V1")))
  print("Resuming the job...  ")
}


# data import
list<- list.files(path = rdata, pattern = "*.RData")
for (i in 1:length(list)){
  load(paste0(rdata,'/',list[i]))
}

arabidopsis_chromosomes$chromosome <-sub('chr', '', arabidopsis_chromosomes$chromosome)   # change here 
fasta.file <-paste0(genome_ref,"/",name_genome)
cytosine.positions <-extractCytosinesFromFASTA(fasta.file, contexts = c('CG', 'CHG', 'CHH'))

startCompute <- function(files_to_go) {

  # storing the file which is done
  going_file <- NULL
  ptm <- proc.time()
  for (i in 1:length(files_to_go$V1)){

    possibleError <- tryCatch(
      thing(),
      error=function(e) e
    )

    if(inherits(possibleError, "error"))
      going_file <- files_to_go$V1[i:i]
    
    print(paste0("Running...", going_file))
    #-------------------------------------------------------------------------------------
    # meth impute part

    name <- gsub(pattern = "\\.CX_report.txt$", "", basename(going_file))
    bismark.data <-importBismark(going_file, chrom.lengths = arabidopsis_chromosomes)      # change here 
    methylome <- inflateMethylome(bismark.data, cytosine.positions)
    distcor <- distanceCorrelation(methylome)
    fit <- estimateTransDist(distcor)
    pdf(paste0(wd, "/fit-reports/fit_", name, ".pdf", sep = ""))
    print(fit)
    dev.off()

    model <- callMethylation(data = methylome, transDist = fit$transDist, include.intermediate=intermediate)
    modifiedexportMethylome(model, filename = paste0("methylome_", name, ".txt"),going_file)
    #---------------------------------------------------------------------------
    # generating reports

    model$data$category <- factor('covered', levels=c('missing', 'covered'))
    model$data$category[model$data$counts[,'total']>=1] <- 'covered'
    model$data$category[model$data$counts[,'total']==0] <- 'missing'
    df.list <- NULL
    #A1 <- plotEnrichment(model$data, annotation=TEs, range = 2000, category.column='category', plot = TRUE, df.list = NULL)
    A2 <- plotEnrichment(model$data, annotation=TEs, range = 2000, category.column='category', plot = FALSE)
    #B1 <- plotEnrichment(model$data, annotation=genes, range = 2000, category.column='category', plot = TRUE, df.list = NULL)
    B2 <- plotEnrichment(model$data, annotation=genes, range = 2000, category.column='category', plot = FALSE)
    write.table(A2, paste0(wd,"/tes-reports/TEs_",name,".txt"), row.names=FALSE, sep="\t", quote=FALSE)
    write.table(B2, paste0(wd,"/gen-reports/genes_",name,".txt"), row.names=FALSE, sep="\t", quote=FALSE)
    #---------------------------------------------------------------------------
    fileConn<-"file-processed.lst"
    cat(going_file, file = fileConn, append = TRUE, sep = "\n" )
    print("Done! writing to processed list.")

    rm(model,methylome)
    print(proc.time() - ptm)
  }


}


startCompute(files_to_go)

rm(list=ls())
gc(reset=TRUE)
