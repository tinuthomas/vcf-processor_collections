#!/usr/bin/env python

"""
2013
Purpose :   Program to filter variants for Allele Balance from the VCF
            Filter criteria :   for Alt/Alt AB<0.1, for Ref/Alt 0.3<AB<0.7
Usage   :   python AlleleBalanceFilter.py in.vcf >out.vcf
"""

import sys
import re
from utils import return_file_handle

def AlleleBiasFilter():
    try:
        invcf = sys.argv[1]
    except:
        print __doc__
        sys.exit(-1)
    fin = return_file_handle(invcf)
    for data in fin:
         if data.startswith('##FORMAT'):
            data = data.split(',')
            formatname = re.search(r'^##FORMAT=<ID=(.+)',data[0])
            formatname_list.append(formatname.group(1))
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
                ln= len(samples)
                print '\t'.join(data)
        elif re.search(r'^(\d+|X|Y)|^chr(\d+|X|Y)',data):
            data = data.strip().split('\t')
            if 'AB' not in data[8].split(':'):
                print 'AB not found in ', data[0:3]
                sys.exit(-1)
            for k,x in enumerate(data[8].split(':')):   #Checks each FORMAT column of a variant for AD
                if x == 'GT':
                    GT_pos = k
                elif x == 'AB':
                    AB_pos = k
            for i  in range(0, ln) :    #Gettig AD data for each variant and appending to the list AD
                j = i + 9
                flag = 0
                if data[j] != './.' and data[j] != '.:.:.:.:.:.' and data[j] != './.:.:.:.:.:.':
                    if data[j].split(':')[GT_pos] == '0/1':
                        for AB in data[j].split(':')[AB_pos].split(','):
                            if (float(AB) <= 0.3 or float(AB) >= 0.7):
                                flag = 1
                    elif data[j].split(':')[GT_pos] == '1/1':
                        for AB in data[j].split(':')[AB_pos].split(',') :
                            if float(AB) >= 0.1 :
                                flag = 1
                if flag == 1:
                    data[j] = './.'
            print '\t'.join(data) #prints the variant information with changed data
        else:
            print '\t'.join(data)
    fin.close()

def main():
    AlleleBiasFilter()

if __name__=='__main__':
    main()
