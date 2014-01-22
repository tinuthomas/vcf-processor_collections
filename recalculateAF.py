#!/usr/bin/env python
"""
Purpose :   Recalculates AF for ACAN run file and replaces old AF value with the new value. Else if AF is not found in the INFO field, calculates and adds it to the INFO field
Usage   :   python /CommonDATA/Python_Scripts/recalculateAF.py  In.vcf  >Out.vcf
"""
import sys
import re
from utils import return_file_handle

try:
    inVCF = sys.argv[1]
except:
    print __doc__
    sys.exit(-1)
info = {}
fin = return_file_handle(inVCF)
info_fields = {}
for line in fin:
    line = line.strip('\n\r')
    if line.startswith('##INFO'):
        print line
        line = line.split(',')
        infoname = re.search(r'^##INFO=<ID=(.+)',line[0])
        infotype = re.search(r'^Type=(.*)',line[2])
        info_fields[infoname.group(1)] = infotype.group(1)        
    elif re.search(r'^chr(\d+|X|Y)|^(\d+|X|Y)',line):
        if 'AC' in info_fields and 'AN' in info_fields:
            line = line.split('\t')
            ALT = []
            AC = []
            AF = []
            if not re.search(r'AC=', line[7]):
                line[7] = line[7] + ';AC=0'
            info_data = line[7].split(';')
            for k in info.keys():
                info[k] = 'None'
            for val in info_data:
                if val.split('=')[0] == 'AC' or val.split('=')[0] == 'AN':
                    info[val.split('=')[0]] = val.split('=')[1]
                    info[val.split('=')[0]] = val.split('=')[1]
                    info[val.split('=')[0]] = val.split('=')[1]

            #Checking for multiple alternate alleles in the vcf file and storing their names in the list named 'ALT'
            #Correspondingly storing multiple values of 'AC' in the list named AC
            if ',' in line[4]:
                ALT = line[4].split(',')
                AC = info['AC'].split(',')
            else:
                ALT.append(line[4])
                AC.append(info['AC'])
            flag = 0
    
            ln_ALT = len(ALT)
            #Calculating the AF values and storing them in the list AF
            for alt_ct in range(0,ln_ALT):
                if float(info['AN']) == 0:
                    AF_value = 0
                else:
                    AF_value = round(float(AC[alt_ct])/float(info['AN']) ,4)
                AF.append(AF_value)
            AF_str = ','.join(str(e) for e in AF)
            #if 'AF' in info_fields:
            line[7] = re.sub(r'AF=.*?;','AF='+AF_str+';',line[7])
            #elif 'AF' not in info_fields and 'AC' in info:
            #    line[7] = line[7] + ';AF='+AF_str
            print '\t'.join(line)
        else:
            print 'AC, AN or AF not present in the INFO field of the VCF'
            sys.exit(-1)
    elif line.startswith('#CHROM'):
        line = line.split('\t')
        print '\t'.join(line)
    else:
        line = line.split('\t')
        print '\t'.join(line)
fin.close()
