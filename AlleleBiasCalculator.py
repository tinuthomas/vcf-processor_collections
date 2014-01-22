#!/usr/bin/env python
"""
Program to calculate Allele Balance(AB) from Allele Depth(AD) in the FORMAT field of the VCF

Usage: python AlleleBiasCalculator.py in.vcf >out.vcf
"""

import sys
import re
from utils import return_file_handle

def AlleleBiasCalculator():
    try:
        inVCF = sys.argv[1]
    except:
        print __doc__
        sys.exit(-1)
    formatname_list = []
    fin = return_file_handle(inVCF)
    for data in fin:
        if data.startswith('##FORMAT'):
            data = data.split(',')
            formatname = re.search(r'^##FORMAT=<ID=(.+)',data[0])
            formatname_list.append(formatname.group(1)) #stores format field name from the VCF header
        elif data.startswith('#CHROM'):
            data = data.strip().split('\t')
            if len(data) <= 8:
                print "\n",'VCF doesnot contain FORMAT field....FORMAT field with Allele Depth(AD) is required for Allelic Bias(AB) calculation',"\n"
                sys.exit(-1)
            elif 'AD' not in formatname_list:
                print "\n",data[0:6],'Variants missing Allelic Depth(AD) in genotype columns. AD required for AlleleBias calculation...',"\n"
                sys.exit(-1)
            else:
                sample_names = data[9:]
                print '\t'.join(data)
        elif re.search(r'^(\d+|X|Y)|^chr(\d+|X|Y)',data):
            data = data.strip().split('\t')
            AD_pos = -9
            if 'AB' in data[8].split(':'):
                print "\n",'AB present in the VCF',"\n"
                sys.exit(-1)                
            for k,x in enumerate(data[8].split(':')):
                if x == 'AD':
                    AD_pos = k
            if AD_pos != -9:
                data[8] = data[8] + ':AB'
                ln = len(sample_names)
                for i in range(0, ln):  #Getting AD dta for each sample and appending to the list AD
                    j = i + 9
                    if data[j] != './.':
                        if data[j].split(':')[AD_pos] != '.' and float(data[j].split(':')[AD_pos].split(',')[0]) != 0:
                            AB_value = []
                            for v in range(0, len(data[j].split(':')[AD_pos].split(',')) - 1):
                                AB_v = float(data[j].split(':')[AD_pos].split(',')[0])/(float(data[j].split(':')[AD_pos].split(',')[0]) + float(data[j].split(':')[AD_pos].split(',')[int(v)+1]))
                                AB_value.append(round(AB_v,5))
                            AB_value = [str(e) for e in AB_value]
                            data[j] = data[j] + ':' + ','.join(AB_value)
                        elif data[j].split(':')[AD_pos] == '.':
                            data[j] = data[j] + ':.'
                        elif float(data[j].split(':')[AD_pos].split(',')[0]) == 0:
                            data[j] = data[j] + ':0' 
                print '\t'.join(data) #prints the variant information with changed data
            elif AD_pos == -9:
                print 'AD not present in FORMAT field !!'
                sys.exit(-1)
        else:
            data = data.strip().split('\t')
            print '\t'.join(data)
    fin.close()

def main():
    AlleleBiasCalculator()

if __name__=='__main__':
    main()
