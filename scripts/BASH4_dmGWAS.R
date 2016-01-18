#!/usr/bin/env Rscript


#Overlaying our Gene-level summary p-values onto a pre-created PPI network:

args<-commandArgs(trailingOnly=TRUE)

if(as.character(args[1])=="-h"){
print("This script overlays gene-level summary p-values onto a pre-created PPI network. The arguments you need are: 1. A tab-delimited text file containing a simple matrix with 2 columns (Gene Symbol, Summary p-values) containing the gene-level summary data for an entire GWAS study (in this case, the file TestData_OnlyGeneNames_pvalues.txt created by VEGAS and then converted to the appropriate format by the script ConverterVegasToGenesPvalues). (e.g., ./Output/TestData_OnlyGeneNames_pvalues.txt), 2. The name of a file containing the network of interest. Our default is the network produced by GeneMania (File: COMBINED.DEFAULT_NETWORKS.BP_COMBINING_MAPPED.txt) (e.g., ./COMBINED.DEFAULT_NETWORKS.BP_COMBINING_MAPPED.txt), 3. An output file directory (e.g., ./Output/), Example syntax: ./BASH4_dmGWAS.R ./Output/TestData_OnlyGeneNames_pvalues.txt ./COMBINED.DEFAULT_NETWORKS.BP_COMBINING_MAPPED.txt ./Output/ ")
quit()
}else{}


GenePvalueFileName<-as.character(args[1])
NetworkFileName<-as.character(args[2])
OutputPath<-as.character(args[3])

###########################


#Reading in Genes and Associated p-values:

print("Reading in genes and associated p-values...")

geneweight<-read.table(GenePvalueFileName, sep="\t", header=TRUE)

#dmGWAS chokes with p==0 and p==1), so we have to replace them
geneweight[geneweight[,2]==1,2]<-0.999
geneweight[geneweight[,2]==0,2]<-1e-06

print("The data should take the format of a matrix with 2 columns: Gene Symbols and P-values")
head(geneweight)

print("Reading in the network of interest...")

network<-read.table(NetworkFileName, sep="\t", header=F)

#Getting the network data in the correct format:
head(network)

network<-network[,c(1,2)]
colnames(network)<-c("interactorA", "interactorB")

library(plyr)

print("Initiating parallel computing for network analysis: Depending on computing power, this may take hours or days.")

#Indicate to R that it should search for the fixed version of dmGWAS in a different folder: This code is the same thing as running in BASH: env R_LIBS=$HOME/RLIB R
.libPaths("/home/ubuntu/RLIB") 
library(BiocParallel)
library(dmGWAS)

#Note: this is just using the recommended settings. Tweaking r can change the strictness of the p-values for what is included in the network formation. Making R larger can reduce network size and computing time:
res.list<-dms(network, geneweight, expr1=NULL, expr2=NULL, d=1, r=0.1)

save(res.list,file=paste(OutputPath, "ResList.RData", sep=""))
print("Initial network construction complete: Full network and related output saved under the name ResList.RData")

######################################################################

#Dense module search: Pulling out subnetwork information for each top gene and creating useful output

print("Pulling out subnetwork information for each top gene and creating navigable output...")

#Calculating percentage rank:

#The output that is overviewed in the dmGWAS manual is not what we see!
# Instead, I think this is what we want:
SeedGeneModuleScorePercentileRank<-(length(res.list$zi.ordered[,3])-rank(res.list$zi.ordered[,3])+1)/length(res.list$zi.ordered[,3])

temp<-data.frame(res.list$zi.ordered[,c(1,3)], SeedGeneModuleScorePercentileRank)
colnames(temp)<-c("gene", "Zn_NormalizedModuleScore", "Percentile Rank")

SummaryByGene<-join(temp, geneweight, by="gene")
colnames(SummaryByGene)[4]<-"OriginalAssociationPvalue"

write.table(SummaryByGene, paste(OutputPath,"ModuleStrengthSummaryByGene.txt", sep=""), sep="\t")
print("Basic output finished: The tab-delimited file ModuleStrengthSummaryByGene.txt contains a list of the following subnetwork properties associated with each gene
1. the normalized module score, with higher scores indicating a greater enrichment of the gene's subnetwork for significant p-values
2. The percentile rank for the normalized module score
3. The original case-control association p-values")

print("Pulling out a list of subnetwork nodes for the genes with the most enriched subnetworks")

#The top genes with their normalized module scores and percentile rank:
Top1000ModuleScores<-SummaryByGene[c(1:1000),]

head(Top1000ModuleScores)

SubgraphGeneSets<-vector("list", length=length(Top1000ModuleScores[,1]))

for(i in 1:length(Top1000ModuleScores$gene)){

temp<-((names(res.list$genesets.clear)) %in% (as.character(Top1000ModuleScores$gene[[i]])))

SubgraphForGene<-res.list$genesets.clear[temp==T]

names(SubgraphGeneSets)[i]<-names(SubgraphForGene) 

SubgraphGeneSets[[i]]<-SubgraphForGene[[1]]

}


SubgraphGeneSets2<-vector("character", length=1000)

for(i in c(1:1000)){
SubgraphGeneSets2[i]<-paste(SubgraphGeneSets[[i]], sep="\t", collapse=", ")
}

Top1000ModuleScores$SubgraphGeneSets<-SubgraphGeneSets2

write.table(Top1000ModuleScores, paste(OutputPath,"Top1000ModuleScores.txt", sep=""), sep="\t", row.names=F, col.names=T)

print("The subnetwork nodes for the top 1000 genes with the most enriched subnetworks have been outputted to the tab-delimited file Top1000ModuleScores.txt") 

q()
