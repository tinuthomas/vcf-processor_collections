#!/usr/bin/env python

import sys
import re
import argparse
parser = argparse.ArgumentParser()
from utils import return_file_handle
"""
class Filters:
    def AF_filter(self,invcf):
        print 'hello'
        print invcf
        #Modify to accept Allele Frequency values from the user
        #try:
        #    x = int(raw_input())
        #except ValueError:
        #    print 'Invalid Num lueer'
        fin = return_file_handle(invcf)
        for line in fin:
            line = line.strip('\n\r').split('\t')
            if re.search(r'^(\d+|X|Y)\t|^chr(\d+|X|Y)\t',line[0]):
                flag = 0
                if ',' in line[4]:
                    for val in line[7].split(';'):
                        if val.split('=')[0] == 'AF':
                            AF_values = val.split('=')[1].split(',')
                            break
                    for af in AF_values:
                        if float(af) < 0.05:
                            flag = 1
                    #if flag:
                        #print '\t'.join(line)
                else: 
                    for val in line[7].split(';'):
                        if val.split('=')[0]=='AF' and float(val.split('=')[1]) < 0.05:
                            flag = 1
                #if flag:
                  # print '\t'.join(line)
            #else:
                #print '\t'.join(line)
        fin.close()
x= Filters()
invcf = sys.argv[1]
x.AF_filter(invcf)
print x.AF_filter.__doc__
"""
