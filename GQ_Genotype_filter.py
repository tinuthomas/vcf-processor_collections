#!/usr/bin/env python
"""
Purpose :   Checks whether the GQ in FORMAT field is less than the specified GQ_value by the user. IF yes, replaces the Genotype column with './.' for samples            less than the specified GQ
            Very Important to recalculate AC, AN and AF in INFO field after running this script
Usage   :   python /CommonDATA/Python_Scripts/GQ_Genotype_filter.py  In.vcf  GQ_value  >Out.vcf 
Example :   python /CommonDATA/Python_Scripts/GQ_Genotype_filter.py  QUAL_recalibrated_snpEff.vcf  10  > GQ_filtered.vcf
"""

import sys
import re
from utils import return_file_handle

try:
    inVCF = sys.argv[1]
    GQ_value = sys.argv[2]
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
    elif re.search(r'^chr(\d+|X|Y)|^(\d+|X|Y)',line):
        line = line.split('\t')
        GQ_pos = -9
        for k,x in enumerate(line[8].split(':')):
            if x == 'GQ':
                GQ_pos = k
        if GQ_pos != -9:
            ln = len(sample_names) - 1
            for i in range(0, ln):
                j = i + 9
                if line[j] != '.' and line[j] != './.' and len(line[j].split(':')) >= GQ_pos + 1:
                    temp_GQ = line[j].split(':')[GQ_pos]
                    if temp_GQ != '.' and float(temp_GQ) < float(GQ_value):
                        line[j] = './.'
                else:
                    line[j] = './.'
            print '\t'.join(line)
        else:
            print "\n",'GQ not present in the variant ', line[0:2],"\n"
            sys.exit(-1)
    elif line.startswith('#CHROM'):
        line = line.split('\t') 
        if len(line) <= 8:
            print "\n",'FORMAT names and Samples not present in the VCF',"\n"
            sys.exit(-1)
        elif 'GQ' not in formatname_list:
            print "\n",'GQ not present in the FORMAT field of the VCF',"\n"
            sys.exit(-1)
        else:
            sample_names = line[9:]
            print '\t'.join(line)
    else:
        line = line.split('\t')
        print '\t'.join(line)
fin.close()
