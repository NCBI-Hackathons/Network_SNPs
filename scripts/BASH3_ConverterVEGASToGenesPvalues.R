#!/usr/bin/env Rscript


#Converting VEGAS output into a simple matrix with 2 columns (Gene Symbol, Summary p-values):

args<-commandArgs(trailingOnly=TRUE)

if(as.character(args[1])=="-h"){
print("This script converts VEGAS output into a simple matrix with 2 columns (Gene Symbol, Summary p-values). The arguments you need are: 1. A VEGAS output file containing a summary of case-control association by gene (e.g., ./VEGAS/TestData_Gene_pvalues.out) 2. An output file path (e.g., ./Output/my_file ).  Example syntax: ./BASH3_ConverterVegasToGenesPvalues.R  ./VEGAS/TestData_Gene_pvalues.out  ./Output/my_file  ")
quit()
}else{}

GenePvalueFileName<-as.character(args[1])
OutputPath<-as.character(args[2])

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

print("This is what the data originally looks like...")
head(GenePvalues)

geneweight<-GenePvalues[,c(2,8)]
colnames(geneweight)<-c("gene", "weight")

print("This is what your data looks like after conversion. It should contain only two columns now: Genes and Pvalues")
head(geneweight)

#Check if this needs header=F and whether we need to trim down the matrix in order to feed it into dmGWAS or any other program:
write.table(geneweight, OutputPath, sep="\t", row.names=FALSE, col.names=TRUE)


