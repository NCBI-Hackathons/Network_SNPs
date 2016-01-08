#!/usr/bin/env R_LIBS=$HOME/RLIB Rscript

#Converting VEGAS output into a simple matrix with 2 columns (Gene Symbol, Summary p-values):

args<-commandArgs(trailingOnly=TRUE)

if(args[1]=="-h"){
print("This script converts VEGAS output into a simple matrix with 2 columns (Gene Symbol, Summary p-values).
The arguments you need are: 
1. A VEGAS output file containing a summary of case-control association by gene. 
2. An output file directory")
}else{}

GenePvalueFileName<-args[1]
OutputPath<-args[3]

###########################

#Reading in Genes and Associated p-values:

print("Currently reading in a VEGAS file containing genes and associated p-values")

#Note: This code is unnecessarily convoluted because earlier versions required removing comment rows.
GenePvalues_textvector<-readLines(GenePvalueFileName)

#Extracting out the rows of non-data that say "Starting chromosome…":
#This may not be necessary with the final complete .out file, only in incomplete files:
GenePvalues_textvectorExtract<-grep("^Starting chromosome +", GenePvalues_textvector,  value=FALSE, invert=F)

print("Number of comment rows that need to be removed from the dataset")
length(GenePvalues_textvectorExtract)

print("If applicable, those comments are…")
GenePvalues_textvector[c(GenePvalues_textvectorExtract)]

#This code chokes if there aren't any lines to extract: currently, I just have it commented and skipped
#GenePvalues<-read.table(textConnection(GenePvalues_textvector[-c(GenePvalues_textvectorExtract)]), sep="", blank.lines.skip=T, header=T) 

#If so, skip to this:
GenePvalues<-read.table(textConnection(GenePvalues_textvector), sep="", blank.lines.skip=T, header=T) 

head(GenePvalues)

geneweight<-GenePvalues[,c(2,8)]
colnames(geneweight)<-c("gene", "weight")

print("This is what your data looks like currently. It should contain only two columns now: Genes and Pvalues")
head(geneweight)

#Check if this needs header=F and whether we need to trim down the matrix in order to feed it into dmGWAS or any other program:
write.table(geneweight, paste(OutputPath, "TestData_OnlyGeneNames_pvalues.txt", sep=""), sep="\t", col.names=TRUE)


