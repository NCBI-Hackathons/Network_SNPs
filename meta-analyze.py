#!/usr/bin/env python 

import argparse


def parsed_command_line():
    """Returns an object that results from parsing the command-line for this program argparse.ArgumentParser(...).parse_ags() 
    """
    parser = argparse.ArgumentParser(
        description='Run multiple network snp analysis algorithms');
    parser.add_argument('--plink_in', type=argparse.FileType('r'),
                        help='Path to a plink association file https://www.cog-genomics.org/plink2/formats#assoc')
    
    return parser.parse_args()

def input_files(parsed_args):
    """Returns a list of input files that were passed on the command line

    parsed_args: the result of parsing the command-line arguments
    """
    if parsed_args.plink_in:
        print "Plink input: "+str(parsed_args.plink_in.name);

parsed = parsed_command_line()
input_files(parsed)
