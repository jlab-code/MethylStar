#!/usr/bin/env Rscript


list.of.packages = c("devtools","data.table","dplyr","ggplot2","doParallel","stringr")

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


