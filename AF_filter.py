#!/usr/bin/env python
"""
ProgramName :   AF_filter.py 
Author      :   Tinu Thomas
Date        :   10/25/2013
Purpose     :   Given a VCF file, filters and gives a VCF with variants greater or lesser than specified AF value by the user
Usage       :   python AF_filter.py option VCF AF_value >OutputVCF
                Option      -   1 or 2
                    1) Filter variants with AF greater than AF specified by the user
                    2) Filter variants with AF value less than AF specified by the user
                AF_value    -   To be specified by the user(anything between 0 and 1)
                VCF         -   Input VCF file
"""

import sys
import re
from utils import return_file_handle

try:
    option = float(sys.argv[1])
    inVCF = sys.argv[2]
    af_check = float(sys.argv[3])
except:
    print __doc__
    sys.exit(-1)

if type(option) is not float or type(af_check) is not float:
    print "Option and AF must be numbers\nOption      -   1 or 2\n1) Filter variants with AF greater than AF specified by the user\n2) Filter variants with AF value less than AF specified by the user\nAF_value    -   To be specified by the user(anything between 0 and 1)\n"
    sys.exit(-1)
elif af_check < 0 or af_check > 1:
    print 'AF values should be only anything from 0 to 1'
    sys.exit(-1)
if float(option) == 1:
    fin = return_file_handle(inVCF)
    for line in fin:
        line = line.strip('\n\r').split('\t')
        if re.search(r'^(\d+|X|Y)|^chr(\d+|X|Y)', line[0]):
            flag = 0
            for val in line[7].split(';'):
                if '=' in val and val.split('=')[0] == 'AF' and ',' not in val.split('=')[1]  :
                    if float(val.split('=')[1]) > af_check:
                        flag = 1
                        break
                elif '=' in val and val.split('=')[0] == 'AF' and ',' in val.split('=')[1]:
                    for af_val in val.split('=')[1].split(','):
                        if float(af_val) > af_check:
                            flag = 1
                            break
            if flag == 1 :
                print '\t'.join(line)
        else:
                print '\t'.join(line)
    fin.close()
elif float(option) == 2:
    fin = return_file_handle(inVCF)
    for line in fin:
        line = line.strip('\n\r').split('\t')
        if re.search(r'^(\d+|X|Y)|^chr(\d+|X|Y)', line[0]):
            flag = 0
            for val in line[7].split(';'):
                if '=' in val and val.split('=')[0] == 'AF' and ',' not in val.split('=')[1]  :
                    if float(val.split('=')[1]) < af_check:
                        flag = 1
                        break
                elif '=' in val and val.split('=')[0] == 'AF' and ',' in val.split('=')[1]:
                    for af_val in val.split('=')[1].split(','):
                        if float(af_val) < af_check:
                            flag = 1
                            break
            if flag == 1 :
                print '\t'.join(line)
        else:
                print '\t'.join(line)
    fin.close()
else:
    print "Please give the correct option 1 or 2\nOption      -   1 or 2\n1) Filter variants with AF greater than AF specified by the user\n2) Filter variants with AF value less than AF specified by the user\nAF_value    -   To be specified by the user\nVCF         -   Input VCF file"
    sys.exit(-1)
