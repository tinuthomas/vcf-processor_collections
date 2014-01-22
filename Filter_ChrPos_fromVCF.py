#!/usr/bin/env python
"""
Purpose	:	Given 2 VCF files, spits out variants in second VCF found in first.
"""
import sys
import re 
from utils import return_file_handle

def Filter_ChrPos_FromVCF(vcffile, PosvcfFile):
    """
    Purpose	:	Given 2 VCF files, spits out variants in second VCF found in first.
    Usage   :   python Filter_ChrPos_FromVCF.py Master.vcf Variant.vcf >Output.vcf
    """
    fpos = return_file_handle(PosvcfFile)
    pos = {}
    pos_ct =0 
    for line in fpos:
        line = line.strip().split('\t')
        if re.search(r'^(\d+|X|Y|M)|^chr(\d+|X|Y|M)',line[0]):
            line[0] = line[0].replace("chr","")
            pos[":".join(line[0:2])] = 1			#Getting Gene names and storing them in the dictinary named 'pos'
    fpos.close()
    fin = return_file_handle(vcffile) #Opening vcf Family Distribution text file
    for data in fin:
        data = data.strip().split('\t')
        if data[0] == '#CHROM':
            print '\t'.join(data)
        elif re.search(r'^(\d+|X|Y|M)|^chr(\d+|X|Y|M)',data[0]):	
            data[0] = data[0].replace('chr','')
            if ':'.join(data[0:2]) in pos:
                print '\t'.join(data)
        else:
            print '\t'.join(data)
    fin.close()

def main():
	try:
		vcffile = sys.argv[1]
		PosvcfFile = sys.argv[2]	
	except:
		print Filter_ChrPos_FromVCF.__doc__
        sys.exit(-1)
	Filter_ChrPos_FromVCF(vcffile, PosvcfFile)

if __name__== '__main__':
	main()

