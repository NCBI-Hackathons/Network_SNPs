#!/bin/bash

# A simple example of running the meta-net-var.py application that
# serves as a quick command for smoke-testing.
cd "$(dirname "$0")"


# Ensure the existence of and clean up output directory
mkdir -p ~/trial/outdir
for i in ~/trial/outdir/*; do 
    rm -rf $i
done

# Keep vegas from running by supplying dummy output (the output of the
# next stage is also supplied on the command-line so this dummy file
# will never be used)
DUMMY_VEGAS_OUTPUT=~/trial/outdir/dummy_vegas_output
touch $DUMMY_VEGAS_OUTPUT

# Run with our sample input files
./meta-net-var.py --plink_assoc_in ~/testdata/phs000182.pha002890.txt --location_2_gene_name ~/Data/geneMania.network --tabbed_gene_list /home/ubuntu/ffrancis/snp_output_file_pval.txt --vegas_gene_assoc $DUMMY_VEGAS_OUTPUT --gene_pvalue /home/ubuntu/TestData_OnlyGeneNames_pvalues-2000.txt --genemania_prot_prot_in /home/ubuntu/graphanalytics/genemania/COMBINED.DEFAULT_NETWORKS.BP_COMBINING_MAPPED.txt  --output_dir ~/trial/outdir
