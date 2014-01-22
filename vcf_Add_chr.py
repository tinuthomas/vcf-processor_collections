#!/usr/bin/env python
import sys
import re
from utils import return_file_handle


def vcf_Add_chr(input_vcf):
    fin = return_file_handle(input_vcf)
    for line in fin:
        line = line.strip('\n\r').split('\t')
        if re.search(r'^(\d+)|X|Y', line[0]):
            line[0] = 'chr' + line[0]
            print '\t'.join(line)
        else:
            print '\t'.join(line)
    fin.close()

input_vcf = sys.argv[1]

vcf_Add_chr(input_vcf)

