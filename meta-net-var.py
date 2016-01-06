#!/usr/bin/env python

import argparse
import os
import tempfile
import shutil

# Constants giving names of file formats
FMT_PLINK_ASSOC = 'plink_assoc' # Treated as a list of locations to use
FMT_GENEMANIA_INTER ='genemania_interaction'
   # 3 columns tab-separated no header:
   #
   # geneid [tab] gene_id [tab] weight

FMT_HOTNET2_EDGE = 'hotnet2_edge' # 3 columns space-separated no header:
                                  # geneid geneid {}
                                  # geneid must be integer
FMT_GENE_LIST='gene_list' # newline separated list of gene ids
FMT_2_COL_GENE_NETWORK='networkx_2_col' # Tab-separated 2 column with
                                        # gene ids from a gene list.
                                        # No header.
FMT_PLINK_4_FUNSEQ='plink_4_funseq' # Tab separated 5 column
                                    # chrom start stop ref alt
                                    #
                                    # chrom is in format "chr2"
FMT_LOCATION_2_GENE_NAME='location_2_gene_name' # Tab separated 4 col No header
                                                # chromosome
                                                # start pos
                                                # end pos
                                                # gene name

FMT_HOTNET2_GENE_INDEX='hotnet2_gene_index' # 2 col space separated
                                            # gene number (used in edge file)
                                            # gene name (from gene list file)

class InputFile(object):
    """Represents a data in a specified format"""
    def __init__(self, file_format, path):
        self.file_format = file_format
        self.path = path
    def __repr__(self):
        return "InputFile('{}','{}')".format(self.file_format, self.path)

def readable_dir(prospective_dir):
    """Function for verifying that something is a readable directory. If not raises an exception, if so, returns prospective_dir

    Taken from stackoverflow question: http://stackoverflow.com/q/11415570/309334
    and not tested
    """
    if not os.path.isdir(prospective_dir):
        raise Exception("{0} is not a pre-existing readable directory path".format(prospective_dir))
    if os.access(prospective_dir, os.R_OK):
        return prospective_dir
    else:
        raise Exception("Can't read from {0}".format(prospective_dir))


def parsed_command_line():
    """Returns an object that results from parsing the command-line for this program argparse.ArgumentParser(...).parse_ags()
    """
    parser = argparse.ArgumentParser(
        description='Run multiple network snp analysis algorithms');
    parser.add_argument('--plink_assoc_in', type=argparse.FileType('r'),
                        help='Path to a plink association file https://www.cog-genomics.org/plink2/formats#assoc')
    parser.add_argument('--genemania_prot_prot_in', type=argparse.FileType('r'),
                        help='Path to a protein-protein-interaction network in 3-column genemania output format http://pages.genemania.org/data/')
    parser.add_argument('--location_2_gene_name', type=argparse.FileType('r'),
                        help='mapping of locations to gene names. Must be same names as used in network. 4 column tab separated: chromosme start end gene_name')
    parser.add_argument('--output_dir', type=readable_dir, required=True,
                        help='The output directory where everything will dump its output')
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
    if parsed_args.location_2_gene_name:
        files.append(InputFile(FMT_LOCATION_2_GENE_NAME, parsed_args.location_2_gene_name.name))
    return files

def plink_assoc_to_2_col_gene_network(input_path_in_tuple, output_path):
    """Create a new networkx formatted interaction file at output_path"""
    input_path = input_path_in_tuple[0]
    print "Converting "+input_path+" to "+FMT_2_COL_GENE_NETWORK
    pass

def genemania_inter_to_hotnet2_edge(input_path_in_tuple, output_path):
    """Create a new hotnet2_edge formatted file at output_path

    Hotnet2 expects a list of edges in the form
    id [space] id [space] {}
    with no header
    """
    input_path = input_path_in_tuple[0]
    print "Converting "+input_path+" to "+FMT_HOTNET2_EDGE
    pass

def plink_assoc_to_plink_4_funseq(input_path_in_tuple, output_path):
    """Create a new plink_4_funseq formatted file at output_path"""
    input_path = input_path_in_tuple[0]
    print "Converting "+input_path+" to "+FMT_PLINK_4_FUNSEQ
    pass

def plink_assoc_to_gene_list(input_path_in_tuple, output_path):
    """Create a new gene_list formatted file at output_path"""
    input_path = input_path_in_tuple[0]
    print "Converting "+input_path+" to "+FMT_GENE_LIST
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

def formats(files):
    return [f.file_format for f in files]

def all_inputs(starting_input_files, converters, path_for_created):
    files = starting_input_files
    old_num_formats = len(set(formats(files)))
    while True:
        for c in converters:
            if c.output_format not in formats(files):
               inputs = set(c.input_formats)
               if inputs.issubset(set(formats(files))):
                   new_path = os.path.join(path_for_created, c.output_format)
                   new_file = InputFile(c.output_format, new_path)
                   input_paths = [f.path for f in files if f.file_format
                                  in c.input_formats]
                   c.function(input_paths, new_path)
                   files.append(new_file)
        new_num_formats = len(set(formats(files)))
        if new_num_formats == old_num_formats:
            break
        else:
            old_num_formats = new_num_formats
    return files

def path_for_format(input_files, file_format):
    f = [fil for fil in input_files if fil.file_format == file_format]
    if len(f) > 1:
        raise RuntimeError("Multiple files for a given format not supported")
    elif len(f) == 0:
        return None
    else:
        return f[0].path


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
    def missing(self, available_formats):
        """Return list of missing items"""
        return set(self.requires()) - set(available_formats)

class Hotnet2(Analyzer):
    def requires(self):
        return (FMT_HOTNET2_EDGE,FMT_HOTNET2_GENE_INDEX, FMT_GENE_LIST) #TODO dummy list
    def run_with(self, input_files, output_dir):
        print "Running",self.__class__.__name__, "writing to", output_dir
        # TODO finish implementing

class Networkx(Analyzer):
    def requires(self):
        return (FMT_GENE_LIST, FMT_2_COL_GENE_NETWORK, FMT_LOCATION_2_GENE_NAME)
    def run_with(self, input_files, output_dir):
        print "Running",self.__class__.__name__, "writing to", output_dir
        # TODO finish implementing


class Funseq2(Analyzer):
    def requires(self):
        return (FMT_PLINK_4_FUNSEQ,)
    def run_with(self, input_files, output_dir):
        print "Running",self.__class__.__name__, "writing to", output_dir
        # TODO finish implementing



analyzers = {
    Hotnet2(),
    Networkx(),
    Funseq2()
}

parsed = parsed_command_line()
print ",".join([str(i) for i in input_files(parsed)])
avail = input_files(parsed)
possible = possible_inputs([a.file_format for a in avail], converters)
temp_dir_path = tempfile.mkdtemp()
print "Possible: "+",".join(sorted(list(possible)));
print "Could not run:" + ",".join(a.__class__.__name__+" is missing:"+",".join(a.missing(possible)) for a in analyzers if not a.can_run_with(possible))
print "Could run:" + ",".join(a.__class__.__name__ for a in analyzers if a.can_run_with(possible))
print "Converting inputs"
inputs = all_inputs(avail, converters, temp_dir_path)
print "Files after conversions:",",".join(f.path for f in inputs)


shutil.rmtree(temp_dir_path)
