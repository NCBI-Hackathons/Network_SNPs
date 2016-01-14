#!/bin/bash

# A simple example of running the meta-net-var.py application that
# serves as a quick command for smoke-testing.
cd "$(dirname "$0")"


# Ensure the existence of and clean up output directory
mkdir -p ~/trial/outdir
for i in ~/trial/outdir/*; do 
    rm -rf $i
done

# Run with our sample input files
./meta-net-var.py --plink_assoc_in ~/testdata/phs000182.pha002890.txt --location_2_gene_name ~/Data/geneMania.network --gene_p_value /home/ubuntu/ffrancis/snp_output_file_pval.txt  --output_dir ~/trial/outdir
