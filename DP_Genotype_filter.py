#!/usr/bin/env python

"""
Purpose :   Checks whether the DP in FORMAT field is lees than the specified DP_value by the user. IF yes, replaces the Genotype column with './.' for samples            less than the specified DP
            Very Important to recalculate AC, AN and AF in INFO field after running this script
Usage   :   python /CommonDATA/Python_Scripts/DP_Genotype_filter.py  In.vcf  DP_value  >Out.vcf 
Example :   python /CommonDATA/Python_Scripts/DP_Genotype_filter.py  QUAL_recalibrated_snpEff.vcf  10  > DP_filtered.vcf
"""
import sys
import re
from utils import return_file_handle

try:
    inVCF = sys.argv[1]
    DP_value = sys.argv[2]
except:
    print __doc__
    sys.exit(-1)
formatname_list = []
fin = return_file_handle(inVCF)
for line in fin:
    line = line.strip('\n\r')
    if line.startswith('##FORMAT'):
        data = line
        line = line.split(',')
        formatname = re.search(r'^##FORMAT=<ID=(.+)',line[0])
        formatname_list.append(formatname.group(1))
        print '\t'.join(data.split('\t'))
    elif re.search(r'^(\d+|X|Y)|^chr(\d+|X|Y)', line):
        line = line.split('\t')
        DP_pos = -9 
        if len(line) <= 8:
            print "\n",'FORMAT field and Samples not found in the VCF ', line[0:2],"\n"
            sys.exit(-1)
        else:
            for k,x in enumerate(line[8].split(':')):
                if x == 'DP':
                    DP_pos = k
        if DP_pos == -9:
            print "\n",'DP not found in FORMAT field of the variant ',line[0:2],"\n"
            sys.exit(-1)
        else:
            ln = len(sample_names) - 1
            for i in range(0, ln):
                j = i + 9
                if line[j] != '.' and line[j] != './.' and len(line[j].split(':')) >= DP_pos + 1:
                    temp_DP = line[j].split(':')[DP_pos]
                    if temp_DP != '.' and float(temp_DP) < float(DP_value):
                        line[j] = './.'
                else:
                    line[j] = './.'
            print '\t'.join(line)
    elif line.startswith('#CHROM'):
        if 'DP' not in formatname_list:
            print "\n", 'DP not present in FORMAT field', "\n"
            sys.exit(-1)
        else:
            line = line.split('\t')
            sample_names = line[9:]
            print '\t'.join(line)
    else:
        line = line.split('\t')
        print '\t'.join(line)
fin.close()
