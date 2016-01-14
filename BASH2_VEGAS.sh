#!/bin/bash

#Converting SNP Association data to a gene-level summary using VEGAS:
if [ $# -lt 2 ]; then
echo "Usage: $0 names_and_pvalues output_filename"
fi

#Using Vegas to Convert a full tab-delimited text file containing 2 columns of data: SNP names and p-values (no header! no quotes!) to a gene level summary of p-values:
#Please note: The location of the input file must be specified, but the output filename must be written without an associated directory.
#Example syntax: ./BASH2_VEGAS.sh ./Output/TestData_OnlySNPs_pvalues.txt TestData_GeneNames_pvalues
/home/ubuntu/VEGAS/vegas $1 -pop hapmapCEU -out $2
