#!/usr/bin/env python

import argparse
import os
import tempfile
import shutil
import subprocess
import sys

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

FMT_GENE_PVALUE='gene_pvalue_file' # 2 column tab separated
                                   # gene_name
                                   # aggregate_p_value as a float in decimal

FMT_HOTNET2_INFLUENCE_MAT='hotnet_influence_mat'

FMT_HEAT_SCORE_JSON='hotnet_heat_score_json'

FMT_SNP_PVALUE='snp_pvalue_file' # 2 column tab-separated no header
                                 # snp id e.g. rs268
                                 # pvalue asd float in decimal
                                 # Used as input to vegas

FMT_VEGAS_GENE_ASSOC='vegas_gene_association' # Output of vegas app
                                              # 10 column space-separated 
                                              # with header. Strings surrounded
                                              # by double quotes
                                              # Columns:
                                              # Chr - string
                                              # Gene - string
                                              # nSNPs - integer
                                              # nSims - integer
                                              # Start - integer
                                              # Stop - integer
                                              # Test - double precision
                                              # Pvalue - 3-digit float
                                              # Best-SNP - string
                                              # SNP-pvalue - double precision

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
    parser.add_argument('--gene_p_value', type=argparse.FileType('r'),
                        help='2 column tab separated no header: gene_name [tab] aggregate_p_value')
    parser.add_argument('--output_dir', type=readable_dir, required=True,
                        help='The output directory where everything will dump its output')
    parser.add_argument('--dry_run', action='store_true',
                        help='Do everything but execute the analyzers '+
                        'and converters')
    parser.add_argument('--exclude_analyzer', type=str, action='append',
                        help='Exclude a given analyzer from running even if '+
                        'its prerequisites are satisfied. If a non-existent '+
                        'analyzer like "this-is-not-an-analyzer" is given, '+
                        'prints a list of the available analyzers')
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
    if parsed_args.gene_p_value:
        files.append(InputFile(FMT_GENE_PVALUE, parsed_args.gene_p_value.name))
    return files

def path_for_format(input_files, file_format):
    f = [fil for fil in input_files if fil.file_format == file_format]
    if len(f) > 1:
        raise RuntimeError("Multiple files for a given format not supported")
    elif len(f) == 0:
        return None
    else:
        return f[0].path

is_dry_run = False
def run_command(command_list):
    """Run command_list using subprocess.call after printing it to stdout"""
    print "Command:"," ".join(command_list)
    if is_dry_run:
        print "Skipped command because this is a dry run"
    else:
        subprocess.call(command_list)


def genemania_inter_to_hotnet2_edge(input_file_in_tuple, output_path):
    """Create a new hotnet2_edge formatted file at output_path

    Hotnet2 expects a list of edges in the form
    id [space] id [space] {}
    with no header
    """
    input_path = input_file_in_tuple[0].path
    print "Converting "+input_path+" to "+FMT_HOTNET2_EDGE
    pass

def plink_assoc_to_plink_4_funseq(input_file_in_tuple, output_path):
    """Create a new plink_4_funseq formatted file at output_path"""
    input_path = input_file_in_tuple[0].path
    print "Converting "+input_path+" to "+FMT_PLINK_4_FUNSEQ
    command_list=['bash','dbvartofunseq.sh', input_path, output_path]
    run_command(command_list)

def plink_4_funseq_and_location_2_gene_name_to_gene_list(input_files, output_path):
    """Create a new gene_list formatted file at output_path"""
    print "Converting "+",".join(str(f) for f in input_files)+" to "+FMT_GENE_LIST
    snp_positions=path_for_format(input_files, FMT_PLINK_4_FUNSEQ)
    loc_to_gene=path_for_format(input_files, FMT_LOCATION_2_GENE_NAME)
    command_list=['bash','scripts/gene_name.sh', snp_positions, loc_to_gene, output_path]
    run_command(command_list)

def gene_pvalue_to_heat_score_json(input_file_in_tuple, output_path):
    """Create a new heat_score_json formatted file at output_path"""
    input_path = input_file_in_tuple[0].path
    print "Converting "+input_path+" to "+FMT_HEAT_SCORE_JSON
    command_list=['python', '/home/ubuntu/ffrancis/hotnet2/hotnet2/generateHeat.py',
                    'mutation', '--snv_file', input_path, '--output_file',
                     output_path]
    run_command(command_list)

def plink_assoc_to_snp_pvalue(input_file_in_tuple, output_path):
    """Create a new snp_pvalue formatted file at output_path"""
    input_path = input_file_in_tuple[0].path
    print "Converting "+input_path+" to "+FMT_SNP_PVALUE
    run_command(['scripts/BASH1_SNPAssociationToSNPPvalues.R', input_path,
                 '1','2', output_path])

def snp_pvalue_to_vegas_gene_assoc(input_file_in_tuple, output_path):
    """Create a new vegas_gene_assoc formatted file at output_path """
    input_path = input_file_in_tuple[0].path
    print "Converting "+input_path+" to "+FMT_VEGAS_GENE_ASSOC
    run_command(['scripts/BASH2_VEGAS.sh', input_path, output_path])
    
#FMT_SNP_PVALUE='snp_pvalue_file' # 2 column tab-separated no header
#FMT_VEGAS_GENE_ASSOC='vegas_gene_association' # Output of vegas app

class Conversion(object):
    def __init__(self, input_formats, output_format, function):
        self.input_formats = input_formats
        self.output_format = output_format
        self.function = function


converters = (
    Conversion((FMT_PLINK_4_FUNSEQ, FMT_LOCATION_2_GENE_NAME),
               FMT_GENE_LIST,
               plink_4_funseq_and_location_2_gene_name_to_gene_list),
#    Conversion((FMT_GENEMANIA_INTER,),
#               FMT_HOTNET2_EDGE,genemania_inter_to_hotnet2_edge),
    Conversion((FMT_PLINK_ASSOC,),
               FMT_PLINK_4_FUNSEQ, plink_assoc_to_plink_4_funseq),
#    Conversion((FMT_PLINK_ASSOC,),
#               FMT_SNP_PVALUE, plink_assoc_to_snp_pvalue),
    Conversion((FMT_SNP_PVALUE,),
               FMT_VEGAS_GENE_ASSOC, snp_pvalue_to_vegas_gene_assoc),
    Conversion((FMT_GENE_PVALUE,),
               FMT_HEAT_SCORE_JSON, gene_pvalue_to_heat_score_json),
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
                   input_files = [f for f in files if f.file_format
                                  in c.input_formats]
                   c.function(input_files, new_path)
                   files.append(new_file)
        new_num_formats = len(set(formats(files)))
        if new_num_formats == old_num_formats:
            break
        else:
            old_num_formats = new_num_formats
    return files



class Analyzer(object):
    def  __init__(self):
       pass
    def requires(self):
        """Return an iterable of the file formats required to do the
        analysis"""
        raise NotImplementedError()
    def run_with(self, input_files, output_dir):
        """Run the analysis with the given input files
        input_files iterable list of InputFile objects
        output_dir string pathname to output directory
        """
        raise NotImplementedError()
    def can_run_with(self, available_formats):
        """Return true if self.requires() is a subset of available_formats"""
        return set(self.requires()).issubset(set(available_formats))
    def missing(self, available_formats):
        """Return list of missing items"""
        return set(self.requires()) - set(available_formats)

class Hotnet2(Analyzer):
    def requires(self):
        return (FMT_HEAT_SCORE_JSON,FMT_HOTNET2_INFLUENCE_MAT, FMT_HOTNET2_GENE_INDEX) #TODO dummy list
    def run_with(self, input_files, output_dir):
        print "Running",self.__class__.__name__, "writing to", output_dir
        heat_score=path_for_format(input_files,FMT_HEAT_SCORE_JSON)
        influence=path_for_format(input_files,FMT_HOTNET2_INFLUENCE_MAT)
        g_index=path_for_format(input_files,FMT_HOTNET2_GENE_INDEX)
        command_list = ['python','/home/ubuntu/ffrancis/hotnet2/hotnet2/bin/findComponents.py',
                        '--infmat_file',influence,'--infmat_index_file',g_index,
                        '--heat_file',heat_score,'--deltas','0.1',
                         '--min_cc_size','1','--output_directory',output_dir, 'none']
        run_command(command_list)

class Networkx(Analyzer):
    def requires(self):
        return (FMT_GENE_LIST, FMT_2_COL_GENE_NETWORK)
    def run_with(self, input_files, output_dir):
        print "Running",self.__class__.__name__, "writing to", output_dir
        gene_list = path_for_format(input_files, FMT_GENE_LIST)
        gene_net_2_col = path_for_format(input_files, FMT_2_COL_GENE_NETWORK)
        command_list = ["python","scripts/network_snps.py","--input",gene_list,
                         "--network",gene_net_2_col, "--out", output_dir]
        run_command(command_list)


class Funseq2(Analyzer):
    def requires(self):
        return (FMT_PLINK_4_FUNSEQ,)
    def run_with(self, input_files, output_dir):
        print "Running",self.__class__.__name__, "writing to", output_dir
        input_file = path_for_format(input_files, FMT_PLINK_4_FUNSEQ)
        command_list=['/home/ubuntu/graphanalytics/funseq2/funseq2-1.2/funseq2',
                      '-f',os.path.abspath(input_file),
                      '-inf','bed','-o',os.path.abspath(output_dir)]
        run_command(command_list)



analyzers = {
    Hotnet2(),
    Networkx(),
    Funseq2()
}

parsed = parsed_command_line()
is_dry_run = parsed.dry_run
excluded_analyzers = set(parsed.exclude_analyzer)

# Check that all excluded analyzers all are legal names
analyzer_names = set(a.__class__.__name__ for a in analyzers)
illegal_excluded_names = excluded_analyzers - analyzer_names
if illegal_excluded_names:
    analyzer_noun = "analyzers" if len(illegal_excluded_names) > 1 \
                    else "analyzer"
    print "Cannot exclude the non-existent "+analyzer_noun+":",",".join(
        illegal_excluded_names)
    print "Legal analyzers are:",", ".join(analyzer_names)
    sys.exit(-1)

print "Available input files: "
print ",".join([str(i) for i in input_files(parsed)])
avail = input_files(parsed)

# Add Hard-coded paths
avail.append(InputFile(FMT_HOTNET2_INFLUENCE_MAT,'/home/ubuntu/ffrancis/hotnet2/hotnet2/manuscript_files/hint+hi2012_influence_matrix_0.40.mat'))
avail.append(InputFile(FMT_HOTNET2_GENE_INDEX,'/home/ubuntu/ffrancis/hotnet2/hotnet2/manuscript_files/hint+hi2012_index_file.txt'))
avail.append(InputFile(FMT_2_COL_GENE_NETWORK,'/home/ubuntu/Data/geneMania.network'))
avail.append(InputFile(FMT_GENE_LIST,'/home/ubuntu/oscarlr/Network_SNPs/Network_SNPs/test/gene_names'))

possible = possible_inputs([a.file_format for a in avail], converters)
temp_dir_path = tempfile.mkdtemp(prefix='meta-net-var')
print "Available inputs after conversion: "
print ",".join(sorted(list(possible)))

print "Analyzers that can run with inputs after conversion:"
print ",".join(a.__class__.__name__ for a in analyzers if a.can_run_with(possible))

print "\nConverting inputs\n"
inputs = all_inputs(avail, converters, temp_dir_path)
print "Files after conversions:",",".join(f.path for f in inputs)
for analyzer in analyzers:
    if analyzer.can_run_with(formats(inputs)):
        a_name = analyzer.__class__.__name__
        if a_name in excluded_analyzers:
            print "Skipping excluded analyzer:", a_name
            continue
        print "Running", a_name
        a_path = os.path.join(parsed.output_dir, a_name)
        try:
            os.makedirs(a_path)
            analyzer.run_with(inputs, a_path)
        except OSError:
            print "Could not run", a_name, "because", a_path, " was already in existence"

analyzers_without_prereq = [a for a in analyzers if not
                            a.can_run_with(possible)]
if analyzers_without_prereq:
    print "Some analyzers could not run because they were "
    print "missing prerequisites:", \
        ",".join(a.__class__.__name__+" is missing:" + 
        ",".join(a.missing(possible)) for a in analyzers_without_prereq)
print "Finished running analyzers"

#print 'Not removing temp directory for debugging:'
#print 'Tempdir is:'
#print temp_dir_path
shutil.rmtree(temp_dir_path)
