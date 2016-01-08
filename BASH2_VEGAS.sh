#Converting SNP Association data to a gene-level summary using VEGAS:

#Change directory to the folder Vegas
cd VEGAS

#Using Vegas to Convert a full tab-delimited text file containing 2 columns of data: SNP names and p-values (no header! no quotes!) to a gene level summary of p-values:
./vegas ../TestData_OnlySNPs_pvalues.txt -pop hapmapCEU -out TestData_Gene_pvalues

cd ../
