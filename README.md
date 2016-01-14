# Network_SNPs: "MetaNetVars"
MetaNetVars is a pipeline for applying network analysis tools for genomic variants analysis

This program was constructed by: Vijayaraj Nagarajan PhD, Vojtech Huser MD PhD, Eric Moyer MS, Felix Francis MS, Oscar Rodriguez, Matthew Lesko, Megan Hagenauer PhD, Ben Busby PhD.

#Introduction
This pipeline allows users to access multiple tools for applying network analysis to human genomic datasets using one simple command-line based program. The user inputs a list of genes, single-nucleutide polymorphisms, or variant loci, either alone or accompanied by p-values derived from a case-control comparison or quantitative trait loci analysis. These nodes are then connected by referencing databases of molecular interactions (protein-protein interactions, protein-DNA interactions, metabolic interactions, etc.). 

# Example

An example invocation of the meta-analysis package can be found in

    sample_run.sh

# Input

MetaNetVars can accept multiple forms of input.

## PLINK-formatted association files:  (http://pngu.mgh.harvard.edu/~purcell/plink/)
            # NCBI dbGaP analysis accession:	pha002890
            # Name:	 Genome Wide Association Study in Age-related Macular Degeneration (AMD)
            # Description:	 Genome-wide genotyping data were produced using the Illumina HumanCNV370v1_C array platform and filtered             using the following criteria: 1) per sample call rate &#8805; 99%, 2) SNP minor allele frequency &#8805; 1%, 3) SNP call              rate &#8805; 95%, 4) SNP HWE p-value &#8805; 1x10 -6 , 5) removing unexpected relatives, resulting in a set of 324067                 autosomal SNPs across 3307 unrelated samples (2157 cases and 1150 controls).  
            # Method:	We performed a genome-wide association study on 2157 Age-Related Macular Degeneration patients and 1150                   controls. The primary statistical analyses for association were carried out using chi-square tests for allelic                        association. Option assoc was used in the program PLINK. To further adjust for the  potential population stratification,              we performed association analyses using a logistic regression with first two principal components obtained from                       EIGENSTRAT. Options " --covar " and " --logistic " were used in the program PLINK. Genotype counts, P-values and allelic              odds ratios with 95% CI are reported. For further information see   Chen et al.  Proc Natl Acad Sci USA.  107:7401-7406,              2010 .
            # Human genome build:	37
            # dbSNP build:	132

            # SNP ID:	Marker accession
            # P-value:	testing p-value
            # Chr ID:	chromosome
            # Chr Position:	chromosome position
            # ss2rs:	ss to rs orientation.  +: same; -: opposite strand.
            # rs2genome:	Orientation of rs flanking sequence to reference genome.  +: same orientation, -: opposite.
            # Allele1:	genomic allele 1
            # Allele2:	genomic allele 2
            # pHWE (case):	p-value from HWE testing in cases
            # pHWE (control):	p-value from HWE testing in controls
            # Call rate (case):	Call rate for cases
            # Call rate (control):	Call rate for controls
            # CI low:	the lower limit of 95% confidence interval
            # CI high:	the higher limit of 95% confidence interval


            SNP ID	P-value	Chr ID	Chr Position	Submitted SNP ID	ss2rs	rs2genome	Allele1	Allele2	pHWE (case)	pHWE (control)	            Call rate (case)	Call rate (control)	Odds ratio	CI low	CI high
            rs6753288	0.8531	2	128169898	ss122610328	+	+	A	G	0.187	0.2064	0.999072786277237	1	1.01	0.9114	1.119
            rs2069916	0.3409	2	128178414	ss121907566	+	+	C	T	0.4805	0.1822	1	1	0.9498	0.8542	1.056
            rs1568277	0.6219	2	128190054	ss121757155	+	+	T	C	0.7399	0.196	1	1	1.037	0.8979	1.197
            rs6754999	0.5926	2	128195386	ss122610674	+	+	G	A	0.9627	0.1115	0.999536393138618	1	0.9713	0.8731	1.081
            rs12994586	0.7279	2	128218363	ss121614165	+	+	C	T	0.1031	0.8797	0.999536393138618	1	1.029	0.8765	1.208
            rs7590705	0.001365	2	128225227	ss122786983	+	+	G	A	0.1431	1	1	1	1.184	1.068	1.312
            rs334160	0.06624	2	128243334	ss123087097	+	+	C	T	0.6101	0.5117	1	0.999130434782609	1.136	0.9915	1.302
            rs2288655	0.196	2	128246983	ss121987517	+	+	G	A	0.5284	0.02692	0.999536393138618	1	1.099	0.9525	1.268


##Bed Formatted association file:
A tab-delimited text file with 5 required fields:
chrom	chromStart	chromEnd	Reference.allele	Alterative.allele	[optional]sample.name
* chrom - The name of the chromosome (e.g. chr3, chrY). 
* chromStart - The starting position of the feature in the chromosome. The first base in a chromosome is numbered 0.
* chromEnd - The ending position of the feature in the chromosome. The chromEnd base is not included in the display of the feature. 
For example, the first 100 bases of a chromosome are defined as chromStart=0, chromEnd=100, and span the bases numbered 0-99.
* Reference.allele - The reference allele of SNVs
* Alternative.allele - The alternative allele of SNVs.

            chr1  213941196  213941197	G	T	PR2832
            chr1  213942363  213942364	A	C	PR2832
            chr1  213943530  213943531	T	A	PR1783

##Tab-delimited SNP association p-value .txt files:
            SNP ID	P-value
            rs6753288	0.8531
            rs2069916	0.3409
            rs1568277	0.6219
            rs6754999	0.5926
            rs12994586	0.7279
            rs7590705	0.001365
            rs334160	0.06624
            rs2288655	0.196

## VEGAS output providing aggregate association p-values for each gene: (http://gump.qimr.edu.au/VEGAS/)
        This is a plain-text file with the columns: Chromosome, Gene, Number of SNPs, Number of simulations, Start position, Stop             position, Gene-based test statistic, P-value.

##Tab-delimited gene & aggregate association p-value .txt files: 
            Gene	Pvalue
            GPR1	0.09762
            CD3EAP	0.148
            DNASE1	0.18
            COL18A1	0.222
            TIE1	0.255
            BMP4	0.282
            SPINK1	0.399
            PSG11	0.462

##Tab-delimited .txt file denoting genetic location and gene symbol:
            4 columns of data, no header: chromosome, start position, end position, gene name (official gene symbol)

##A simple line-separated list of gene symbols (length>5):
            GPR1
            TNFRSF1A
            CD3EAP
            DNASE1
            COL18A1
            TIE1
            BMP4
            SPINK1
            PSG11


# Output
##Funseq2
Citation for FunSeq2: [PMID: 24092746, http://funseq2.gersteinlab.org/] 

###Candidates.Summary
Needs description
###Error.log
Needs description
###Output.vcf
Needs description
###Recur.Summary
Needs description

##Hotnet2
Citation for HotNet2: [PMID: 21385051, http://compbio.cs.brown.edu/projects/hotnet/] 

###Delta_0.1
There will be one subdirectory for each delta used. At the moment delta=0.1 is hard-coded in the meta-script calling Hotnet2.
####components.txt
Needs description
####results.json
Needs description

##NetworkX
Citation for NetworkX: [https://networkx.github.io/] 
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

##dmGWAS:
Citation for dmGWAS_3.0: [PMID: 21045073, http://bioinfo.mc.vanderbilt.edu/dmGWAS/]


#Running the pipeline

See the file:
```
sample_run.sh
```

#Appendices

##presentation made on day 2 of hackathon
(with additional changes on day 3)
 https://docs.google.com/presentation/d/1PzQrERWxcQQvih6TLuF4IBvmNCFe7D253Qm5UWPAWfA/edit?usp=sharing

