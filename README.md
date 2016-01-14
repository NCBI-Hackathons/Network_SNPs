# Network_SNPs
This pipeline allows users to access multiple tools for applying network analysis to genomic datasets using one simple command-line based program. The user inputs a list of genes or single-nucleutide polymorphisms, either alone or accompanied by p-values derived from a case-control comparison or quantitative trait loci analysis. These nodes are then connected by referencing databases of molecular interactions (protein-protein interactions, protein-DNA interactions, metabolic interactions, etc.).  

This program was constructed by a group consisting of 6 members (see Abstract for the list).

#Introduction
Our work focuses on using network analysis methods to aid analysis of variant calls. Centrality measure is used as.

# Example

An example invocation of the meta-analysis package can be found in

    sample_run.sh

# Input

_todo_

# Output
##Funseq2
###Candidates.Summary
Needs description
###Error.log
Needs description
###Output.vcf
Needs description
###Recur.Summary
Needs description
##Hotnet2
###Delta_0.1
There will be one subdirectory for each delta used. At the moment delta=0.1 is hard-coded in the meta-script calling Hotnet2.
####components.txt
Needs description
####results.json
Needs description
##NetworkX
Output of our home-grown package that needs a better name
###output
3-column file with gene names, degrees and betweenness of genes.

                # From this output, it would be smart to focus on CD3EAP since it
                # has the highest centrality and degree measurement
                # Example:
                gene	degrees	btw_centrality
                CD3EAP	500	0.377719224858
                TMC1	30	0.000297257109932
                LRP8	30	0.000768086055561
                SLC30A6	26	0.000223232830101
                ZNF234	22	0.000146138740468
                MYBBP1A	20	0.000310454619974
                HHIPL2	41	0.000495219919278
                CYP2B6	41	0.000465664109724
                CLDN20	17	5.61032381821e-05
###pngs/

This folder has a figure for each input gene and its neighbor genes.

###xml_format/ 

This folder has the xml format of the subnetworks in the pngs folder.

#Running the pipeline

See the file:
```
sample_run.sh
```

#Appendices

##presentation made on day 2 of hackathon
(with additional changes on day 3)
 https://docs.google.com/presentation/d/1PzQrERWxcQQvih6TLuF4IBvmNCFe7D253Qm5UWPAWfA/edit?usp=sharing

