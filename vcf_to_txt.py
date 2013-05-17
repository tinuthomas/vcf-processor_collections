#!/usr/bin/env python 
"""
Program to convert VCF files to TEXT format

Usage: python vcf_to_txt.py in.vcf > out.txt 
"""

import sys 
import re
from utils import return_file_handle

def vcf_parser(input_vcf):
    """
    VCF main parsing program
    """
    fin = return_file_handle(input_vcf)
    info_ct = format_ct = variant_ct = 0
    info_fields = {}
    info_header = []
    for line in fin:
        line = line.strip('\n\r')
        if line.startswith('##INFO'):
            line = line.split(',')
            infoname = re.search(r'^##INFO=<ID=(.+)',line[0])
            infotype = re.search(r'^Type=(.*)',line[2])
            info_fields[infoname.group(1)] = infotype.group(1)
        elif line.startswith('#CHROM'):
            line = line.split('\t')
            sample_names = line[9:] 
            for head in info_fields.keys():
                info_header.append(head)
            print '\t'.join(line[0:7] + info_header + line[9:])
        elif re.search(r'^(\d+|X|Y)|^chr(\d+|X|Y)',line):
            line = line.split('\t')
            if line[0].startswith('chr'):
                line[0] = line[0].replace('chr','')
            info_values = info_parser(info_header,info_fields,line[7])
            GT = GT_parser(line[8], line[9:])
            print '\t'.join(line[0:7] + info_values + GT ) 
    fin.close()


def info_parser(info_header, info_fields,info_col):
    """
    Function to parse INFO column
    This function will receive the list of INFO column names from the VCF header, info_fields dictionary with key as INFO column name value as TYPE,
    INFO column for a particular variant from the VCF
    """
    info = {}
    info_values = []
    for inf in info_fields.keys():  #Initializing the dict values to None
        info[inf] = 'None'
    for col in info_col.split(';'):
        if info_fields[col.split('=')[0]] != 'Flag' :
            info[col.split('=')[0]] = col.split('=')[1]
        else: 
            info[col.split('=')[0]] = col.split('=')[0]
    for val in info_header:         #Getting the info column values in the same order as of info_header list in the list info_values 
        if val in info:
            info_values.append(info[val])
        else:
            print "Val Not Present"
    return info_values

def GT_parser(format, Genotype_data):
    """
    Gets the GT data for each variant and returns the GT as list
    """
    GT = []
    for k,x in enumerate(format.split(':')):
        if x == 'GT':
            GT_pos = k
    for col in Genotype_data:
        GT.append(col.split(':')[GT_pos])
    return GT

def main():

    try:
        input_vcf = sys.argv[1]	
    except:
        print __doc__
        sys.exit(-1) 
    vcf_parser(input_vcf)

if __name__=='__main__':
	main()
