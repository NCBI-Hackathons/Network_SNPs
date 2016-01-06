#!/usr/bin/env python

import argparse

# Constants giving names of file formats
FMT_PLINK_ASSOC = 'plink_assoc'
FMT_GENEMANIA_INTER ='genemania_interaction'
   # 3 columns tab-separated no header:
   #
   # geneid [tab] gene_id [tab] weight

FMT_HOTNET2_EDGE = 'hotnet2_edge' # 3 columns space-separated no header:
                                  # geneid geneid {}
FMT_GENE_LIST='gene_list' # newline separated list of gene ids
FMT_2_COL_GENE_NETWORK='networkx_2_col' # Tab-separated 2 column with
                                        # gene ids from a gene list.
                                        # No header.
FMT_PLINK_4_FUNSEQ='plink_4_funseq' # Tab separated 5 column
                                    # chrom start stop ref alt
                                    #
                                    # chrom is in format "chr2"

class InputFile(object):
    """Represents a data in a specified format"""
    def __init__(self, file_format, path):
        self.file_format = file_format
        self.path = path
    def __repr__(self):
        return "InputFile('{}','{}')".format(self.file_format, self.path)

def parsed_command_line():
    """Returns an object that results from parsing the command-line for this program argparse.ArgumentParser(...).parse_ags()
    """
    parser = argparse.ArgumentParser(
        description='Run multiple network snp analysis algorithms');
    parser.add_argument('--plink_assoc_in', type=argparse.FileType('r'),
                        help='Path to a plink association file https://www.cog-genomics.org/plink2/formats#assoc')
    parser.add_argument('--genemania_prot_prot_in', type=argparse.FileType('r'),
                        help='Path to a protein-protein-interaction network in 3-column genemania output format http://pages.genemania.org/data/')

    return parser.parse_args()

def input_files(parsed_args):
    """Returns a list of input files that were passed on the command line

    parsed_args: the result of parsing the command-line arguments
    """
    files=[]
    if parsed_args.plink_assoc_in:
        files.append(InputFile(FMT_PLINK_ASSOC, parsed_args.plink_assoc_in.name))
    if parsed_args.genemania_prot_prot_in:
        files.append(InputFile(FMT_GENEMANIA_INTER, parsed_args.genemania_prot_prot_in.name))
    return files

def plink_assoc_to_2_col_gene_network(input_path_in_tuple, output_path):
    """Create a new networkx formatted interaction file at output_path"""
    input_path = input_path_in_tuple[0]
    pass

def genemania_inter_to_hotnet2_edge(input_path_in_tuple, output_path):
    """Create a new hotnet2_edge formatted file at output_path

    Hotnet2 expects a list of edges in the form
    id [space] id [space] {}
    with no header
    """
    input_path = input_path_in_tuple[0]
    pass

def plink_assoc_to_plink_4_funseq(input_path_in_tuple, output_path):
    """Create a new plink_4_funseq formatted file at output_path"""
    input_path = input_path_in_tuple[0]
    pass

def plink_assoc_to_gene_list(input_path_in_tuple, output_path):
    """Create a new gene_list formatted file at output_path"""
    input_path = input_path_in_tuple[0]
    pass

class Conversion(object):
    def __init__(self, input_formats, output_format, function):
        self.input_formats = input_formats
        self.output_format = output_format
        self.function = function


converters = (
    Conversion((FMT_PLINK_ASSOC,),
               FMT_2_COL_GENE_NETWORK,
               plink_assoc_to_2_col_gene_network),
    Conversion((FMT_PLINK_ASSOC,),
               FMT_GENE_LIST,
               plink_assoc_to_gene_list),
    Conversion((FMT_GENEMANIA_INTER,),
               FMT_HOTNET2_EDGE,genemania_inter_to_hotnet2_edge),
    Conversion((FMT_PLINK_ASSOC,),
               FMT_PLINK_4_FUNSEQ, plink_assoc_to_plink_4_funseq)
)

def possible_inputs(starting_input_formats, converters):
    possible = set(starting_input_formats)
    old_size = len(possible)
    while True:
        for c in converters:
            inputs = set(c.input_formats)
            if inputs.issubset(possible):
                possible.add(c.output_format)
        if len(possible) == old_size:
            break
        else:
            old_size = len(possible)
    return possible

class Analyzer(object):
    def  __init__(self):
       pass
    def requires(self):
        """Return an iterable of the file formats required to do the
        analysis"""
        raise NotImplementedError()
    def run_with(self, input_files, output_dir):
        """Run the analysis with the given input files"""
        raise NotImplementedError()
    def can_run_with(self, available_formats):
        """Return true if self.requires() is a subset of available_formats"""
        return set(self.requires()).issubset(set(available_formats))

class Hotnet2(Analyzer):
    def requires(self):
        return (FMT_HOTNET2_EDGE,) #TODO dummy list

class Networkx(Analyzer):
    def requires(self):
        return (FMT_GENE_LIST, FMT_2_COL_GENE_NETWORK)

class Funseq2(Analyzer):
    def requires(self):
        return (FMT_PLINK_4_FUNSEQ,)

analyzers = {
    Hotnet2(),
    Networkx(),
    Funseq2()
}

parsed = parsed_command_line()
print ",".join([str(i) for i in input_files(parsed)])
avail = input_files(parsed)
possible = possible_inputs([a.file_format for a in avail], converters)
print "Possible: "+",".join(sorted(list(possible)));
print "Could not run:" + ",".join(a.__class__.__name__ for a in analyzers if not a.can_run_with(possible))
print "Could run:" + ",".join(a.__class__.__name__ for a in analyzers if a.can_run_with(possible))
for a in analyzers:
    print a.__class__.__name__, " requires: ", ",".join(a.requires())
