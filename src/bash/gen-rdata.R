#!/usr/bin/env Rscript


#----------------------------------------------
# test if arguments are supplied
#-------------------------------------------------------------
args <- commandArgs(trailingOnly = TRUE)
wd = args[1]  # result pipeline folder
setwd(paste0(wd,"/","rdata"))
tmp_rdata = (paste0(wd,"/","rdata"))
data.names <-list.files(paste0(tmp_rdata),pattern = "*.txt")
Ref_Chr <- read.table(data.names, header=F)
save(Ref_Chr, file = paste0(tmp_rdata,"/","Ref_Chr.RData"))