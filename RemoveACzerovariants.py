#!/usr/bin/env python

"""
Purpose :   Given a VCF file would remove variants with AC = 0
Usage   :   python /CommonDATA/Python_Scripts/RemoveACzerovariants.py Input.vcf >Output.vcf
"""
import sys
import re
from utils import return_file_handle

try:
    inVCF = sys.argv[1]
except:
    print __doc__
    sys.exit(-1)
formatname_list = []
fin = return_file_handle(inVCF)
for line in fin:
    line = line.strip('\n\r').split('\t')
    if re.search(r'^(\d+|X|Y)|^chr(\d+|X|Y)', line[0]):
        flag = 0
        for val in line[7].split(';'):
            if '=' in val and val.split('=')[0] == 'AC' and ',' not in val.split('=')[1]  :
                if float(val.split('=')[1]) != 0:
                    flag = 1
                    break
            elif '=' in val and val.split('=')[0] == 'AC' and ',' in val.split('=')[1] :
                AC_values = list(set(val.split('=')[1].split(',')))
                if AC_values != ['0']:
                    flag = 1
        if flag == 1 :
            print '\t'.join(line)
    else:
        print '\t'.join(line)
fin.close()


