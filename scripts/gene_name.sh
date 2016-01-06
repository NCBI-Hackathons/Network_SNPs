#!/bin/bash
#
# ./gene_name.sh <snp_positions_fn> <gene_names_fn> <outdir>
# Input: 1. dbGAP file (snp_positions_fn)
#        2. 4-column file with chr, start, end, gene (gene_names_fn)
#        3. directory to output files (outdir)
#
# Output: 1. 1-column file with a list of genes

snp_positions_fn=$1
gene_names_fn=$2
out_gene_list=$3

temp_dir=`mktemp -d`
sort -k1,1 -k2,2n ${snp_positions_fn} > ${temp_dir}/${snp_positions_fn}.sorted
sort -k1,1 -k2,2n ${gene_names_fn} > ${temp_dir}/${gene_names_fn}.sorted

bedtools intersect -wb -a ${temp_dir}/${snp_positions_fn}.sorted -b ${temp_dir}/${gene_names_fn}.sorted | cut -f3 > ${out_gene_list}
rm -fr ${temp_dir}
