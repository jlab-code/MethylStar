#!/usr/bin/env Rscript
options(warn=-1)
source("./src/bash/r-lib.R")

# reading base directory from config.cfg
args <- commandArgs(trailingOnly = TRUE)
#----------------------------
#needs a sorted bam file
#---------------------------
wd=(args[1])          # result direcory
setwd(paste0(wd,"/","methimpute-out"))
genome_ref=(args[2])  # genome reference directory
name_genome=(args[3]) # name of genome
rdata=(args[4])       # file for genes/TEs/etc.(annotation files)
intermediate<-as.logical(toupper((args[5])))
fit_output=as.logical(toupper((args[6])))
enrichment_plot=as.logical(toupper((args[7])))
full_report=as.logical(toupper((args[8])))
minCov=as.numeric(as.character(((args[9]))))
intermediate_mode=(args[10])

file<-(args[15])


#try(system("ls -1v ../bismark-deduplicate/*.bam > list-files.lst" ,intern = TRUE))
#fileName <-fread("list-files.lst",skip = 0,header = FALSE)

#------------------------------------------------------------------
# parallel function to extract cytosine
#------------------------------------------------------------------
#no_cores <- detectCores() - 2
fun1<-function(file)  {
  my.methRaw.CpG=methylKit::processBismarkAln(location = file,
                                   sample.id="file1", assembly="TAIR10", mincov=minCov,
                                   minqual=20, phred64=FALSE,
                                   read.context="CpG")
  CpG <- cbind(my.methRaw.CpG, context='CG')
  return(CpG)
}
fun2<-function(file)  {
  my.methRaw.CHG=methylKit::processBismarkAln(location = file,
                                   sample.id="file1", assembly="TAIR10", mincov=minCov,
                                   minqual=20, phred64=FALSE,
                                   read.context="CHG")
  CHG <- cbind(my.methRaw.CHG, context='CHG')
  return(CHG)
}
fun3<-function(file)  {
  my.methRaw.CHH=methylKit::processBismarkAln(location = file,
                                   sample.id="file1", assembly="TAIR10", mincov=minCov,
                                   minqual=20, phred64=FALSE,
                                   read.context="CHH")
  CHH <- cbind(my.methRaw.CHH, context='CHH')
  return(CHH)
}
tasks = list(job1 = function(x) fun1(x),
             job2 = function(x) fun2(x),
             job3 = function(x) fun3(x))  

#------------------------------------------------------------------
# import bam file

import_aln <- function(file, chrom.lengths=NULL, skip=0){

  cat("Registering cluster ... number of cores: 3\n")
  cl = makeCluster(3)
  registerDoParallel(cl)
  cat("Extracting cytosines ...\n")
  clusterExport(cl, c('fun1', 'fun2', 'fun3','file','minCov'))
  out = clusterApply(cl,tasks, function(f) f(file))
  stopCluster(cl)
  
  CpG<-out[[1]]
  CHG<-out[[2]]
  CHH<-out[[3]]
  cat("Binding cytosine...\n")
  my.methRaw <- rbind(CpG, CHG, CHH)
  data <- GRanges(seqnames=my.methRaw$chr, 
                  ranges=IRanges(start=my.methRaw$start, end=my.methRaw$end), 
                  strand=my.methRaw$strand, context=my.methRaw$context)
  
  counts <- array(NA, dim=c(length(data), 2), dimnames=list(NULL, c("methylated", "total")))
  counts[,"methylated"] <- my.methRaw$numCs
  counts[,"total"] <- my.methRaw$coverage
  data$counts <- counts
  
  if (!is.null(chrom.lengths)) {
    if (is.character(chrom.lengths)) {
      df <- fread(chrom.lengths, header=TRUE)
    } else if (is.data.frame(chrom.lengths)) {
      df <- chrom.lengths
    }
    chrom.lengths <- df[,2]
    names(chrom.lengths) <- df[,1]
    # Filter by chromosomes supplied in chrom.lengths
    data <- keepSeqlevels(data, seqlevels(data)[seqlevels(data) %in% names(chrom.lengths)], pruning.mode="coarse")
    seqlengths(data) <- chrom.lengths[names(seqlengths(data))]
  }
  rm(CpG, CHG, CHH, my.methRaw,out,file)
  cat("Making data-frame...\n")
  return(data)
}

#------------------------------------------------------------------
# customized export function
#------------------------------------------------------------------

modifiedexportMethylome <- function( model, filename) {
  data <- model$data
  df <-  methods::as(data, 'data.frame')
  df <- df[,c('seqnames', 'start', 'strand', 'context', 'counts.methylated', 'counts.total', 'posteriorMax', 'posteriorMeth', 'posteriorUnmeth', 'status','rc.meth.lvl')]
  #----------------------------------------------------------------
  # dropping columns 
  drops <- c("posteriorMeth","posteriorUnmeth")
  df<- df[ , !(names(df) %in% drops)]
  #------------------------------------------------------------------
  # converting to M,I,U to save in size
  # converting chachter to M,U,I
  cat("Reducing data-set size...\n")
  df$status<-str_replace_all(df$status, pattern = "Unmethylated", replacement = "U") # all
  df$status<-str_replace_all(df$status, pattern = "Intermediate", replacement = "I") # all
  df$status<-str_replace_all(df$status, pattern = "Methylated", replacement = "M") # all
  #-----------------------------------------------------------------
  # take 4 digit of decimal value posteriorMax column 
  floor_dec <- function(x, level=1) round(x - 5*10^(-level-1), level)
  df$posteriorMax <-floor_dec(as.numeric(as.character(df$posteriorMax)),5)
  df$rc.meth.lvl <-floor_dec(as.numeric(as.character(df$rc.meth.lvl)),5)
  #-----------------------------------------------------------------
  #final_dataset<-as.data.table(final_dataset)
  cat("Writing to the file...\n")
  fwrite(df,file = filename, quote = FALSE, sep ='\t', row.names = FALSE, col.names = TRUE)
  rm(data,df)
}
#-------------------------------------------------------------------
# files_to_go <-NULL
# file_processed<-"file-processed.lst"
# if (!file.exists(file_processed)){
#   cat("It's first time you are running Methimpute for this data-set!\n")
#   files_to_go <- fileName
# } else {
#   file_processed <-fread("file-processed.lst",skip = 0,header = FALSE)
#   files_to_go <- as.data.table(anti_join (fileName , file_processed, by = c("V1")))
#   cat("Resuming the job...\n")
# }
# Rdata import
list<- list.files(path = rdata, pattern = "*.RData")
for (i in 1:length(list)){
  load(paste0(rdata,'/',list[i]))
}

fasta.file <-paste0(genome_ref,"/",name_genome)
cytosine.positions <-extractCytosinesFromFASTA(fasta.file, contexts = c('CG', 'CHG', 'CHH'))

startCompute <- function(file) {
  # storing the file which is done
  going_file <- NULL
  
    tryCatch({
      ptm <- proc.time()
      going_file <- file
      
      #----------------------------------------------------------------------------
      name <- gsub(pattern = "\\.bam$", "", basename(going_file))
      name <-gsub(pattern = "sorted-", "", basename(name))
      cat(paste0("Running...", name),"\n")
      cat("Preparing Alignments... \n")
      methylome.data <- import_aln(going_file, chrom.lengths = Ref_Chr)
      methylome <- inflateMethylome(methylome.data, cytosine.positions)
      rm(methylome.data)
      distcor <- distanceCorrelation(methylome)
      fit <- estimateTransDist(distcor)

      if (intermediate==TRUE){
        model <- callMethylation(data = methylome, transDist = fit$transDist, include.intermediate=intermediate , update=intermediate_mode)
        }else{
        model <- callMethylation(data = methylome, transDist = fit$transDist, include.intermediate=intermediate)    
      }

      modifiedexportMethylome(model, filename = paste0("methylome_", name, ".txt"))
      
      #---------------------------------------------------------------------------
      # generating reports
      model$data$category <- factor('covered', levels=c('missing', 'covered'))
      model$data$category[model$data$counts[,'total']>=1] <- 'covered'
      model$data$category[model$data$counts[,'total']==0] <- 'missing'
      df.list <- NULL
      if (fit_output==TRUE){
        print(paste0("Generating fit plot...", name))
        pdf(paste0(wd, "/fit-reports/fit_", name, ".pdf", sep = ""))
        print(fit)
        dev.off()
      }
      if (enrichment_plot==TRUE){
        
        print(paste0("Generating enrichment plot for TEs...", name))
        A1 <- plotEnrichment(model$data, annotation=TEs, range = 2000, category.column='category', plot = TRUE, df.list = NULL)
        pdf(paste0(wd, "/tes-reports/TEs_", name, ".pdf", sep = "")) 
        print(A1)
        dev.off()
        
        print(paste0("Generating enrichment plot for genes...", name))
        B1 <- plotEnrichment(model$data, annotation=genes, range = 2000, category.column='category', plot = TRUE, df.list = NULL)
        pdf(paste0(wd, "/gene-reports/gene_", name, ".pdf", sep = "")) 
        print(B1)
        dev.off()
      }
      if (full_report==TRUE){
        print(paste0("Generating TEs reports...", name))
        A2 <- plotEnrichment(model$data, annotation=TEs, range = 2000, category.column='category', plot = FALSE)  
        write.table(A2, paste0(wd,"/tes-reports/TEs_",name,".txt"), row.names=FALSE, sep="\t", quote=FALSE)
        print(paste0("Generating genes reports...", name))
        B2 <- plotEnrichment(model$data, annotation=genes, range = 2000, category.column='category', plot = FALSE)
        write.table(B2, paste0(wd,"/gene-reports/genes_",name,".txt"), row.names=FALSE, sep="\t", quote=FALSE)
      }
      #---------------------------------------------------------------------------
      fileConn<-"file-processed.lst"
      cat(going_file, file = fileConn, append = TRUE, sep = "\n" )
      cat("Processing file is done.\n")
      rm(model,methylome,going_file)
      print(proc.time() - ptm)
    },error=function(e){cat("ERROR :",conditionMessage(e), "\n")})
  
  
}
      
startCompute(file)

