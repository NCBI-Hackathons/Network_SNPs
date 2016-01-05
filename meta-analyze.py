#!/usr/bin/env python 

import argparse

class InputFile:
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
    
    return parser.parse_args()

def input_files(parsed_args):
    """Returns a list of input files that were passed on the command line

    parsed_args: the result of parsing the command-line arguments
    """
    files=[]
    if parsed_args.plink_assoc_in:
        files.append(InputFile("plink_assoc", parsed_args.plink_assoc_in.name))
    return files

def plink_assoc_to_networkx(input_path, output_path):
    """Create a new networkx formatted file at output_path"""
    pass

converters = {('plink_assoc','networkx'):plink_assoc_to_networkx} 
parsed = parsed_command_line()
print ",".join([str(i) for i in input_files(parsed)])

