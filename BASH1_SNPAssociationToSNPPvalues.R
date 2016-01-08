#!/usr/bin/env R

#Converting SNP Association data into the right format for VEGAS.

args<-commandArgs(trailingOnly=TRUE)

if(args[1]=="-h"){
print("This script converts SNP Association data into the right format for VEGAS.
The arguments you need are:
1. The file name for the SNP association file
2. The column number containing the SNP names (rs…)
3. The column number containing the SNP case-control association p-value
4. An output directory")
}else{}

SNPAssociationFileName<-args[1]
ColumnNumberSNPNames<-args[2]
ColumnNumberSNPpvalues<-args[3]
OutputPath<-args[4]

#Reading in our SNP association data, extracting the correct columns, and outputting it into a new file.

SNPAssociationFile<-read.table(SNPAssociationFileName, sep="\t", header=T)

print("This is the format of your SNP Association File")
head(SNPAssociationFile)

print("These are the columns that you have indicated include the SNP names and pvalues")
head(SNPAssociationFile[,c(ColumnNumberSNPNames,ColumnNumberSNPpvalues)])

#Note: We need to extract out only the columns of data including the SNP names and p-values, no header:
write.table(SNPAssociationFile[,c(ColumnNumberSNPNames,ColumnNumberSNPpvalues)], paste(OutputPath, "TestData_OnlySNPs_pvalues.txt", sep=""), quote=F, sep="\t",  col.names=F, row.names=F)

q()
