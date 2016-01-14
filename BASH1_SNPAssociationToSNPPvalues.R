#!/usr/bin/env Rscript

#Converting SNP Association data into the right format for VEGAS.

args<-commandArgs(trailingOnly=TRUE)

if(as.character(args[1])=="-h"){
print("This script converts SNP Association data into the right format for VEGAS. The arguments you need are: 1. The file name for the SNP association file (e.g., ./BASH1_SNPAssociationToSNPPvalues.R phs000182.pha002890.txt), 2. The column number containing the SNP names (rs…) (e.g., 1), 3. The column number containing the SNP case-control association p-value (e.g., 2), 4. An output directory (e.g., ./Output/). Example syntax:  ./BASH1_SNPAssociationToSNPPvalues.R phs000182.pha002890.txt 1 2 ./Output/")
quit()
}else{}

SNPAssociationFileName<-as.character(args[1])
ColumnNumberSNPNames<-as.numeric(args[2])
ColumnNumberSNPpvalues<-as.numeric(args[3])
OutputPath<-as.character(args[4])

#Reading in our SNP association data, extracting the correct columns, and outputting it into a new file.

SNPAssociationFile<-read.table(SNPAssociationFileName, sep="\t", header=T)

print("This is the format of your SNP Association File")
head(SNPAssociationFile)

print("These are the columns that you have indicated include the SNP names and pvalues")
head(SNPAssociationFile[,c(ColumnNumberSNPNames,ColumnNumberSNPpvalues)])

#Note: We need to extract out only the columns of data including the SNP names and p-values, no header:
write.table(SNPAssociationFile[,c(ColumnNumberSNPNames,ColumnNumberSNPpvalues)], paste(OutputPath, "TestData_OnlySNPs_pvalues.txt", sep=""), quote=F, sep="\t",  col.names=F, row.names=F)

q()
