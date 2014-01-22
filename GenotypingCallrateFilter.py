"""
Purpose : From the VCF calculates the callrate of variant per center and extracts only variants with call rate greater than user specified  genotyping call rate

Usage   :   python GenotypingCallRateFilter.py  In.vcf  CallrateLimit  >Out.vcf
"""

import sys
import re
from utils import return_file_handle

def CallRateFilter():
    try:
        inVCF = sys.argv[1]
        cr_limit = sys.argv[2]
    except:
        print __doc__
        sys.exit(-1)
    fin = return_file_handle(inVCF)
    for line in fin:
        line = line.strip().split('\t')
        msk_an = msk_cr = 0
        if re.search(r'^chr(\d+|X|Y)|^(\d+|X|Y)',line[0]):
            samples = len(line[9:])
            for val in line[7].split(';'):
                if val.split('=')[0] == 'AN':
                    msk_an = float(val.split('=')[1])/2
                    msk_cr = msk_an/float(samples)
            if (msk_cr > float(cr_limit)):
                print '\t'.join(line)
        else:
            print '\t'.join(line)
    fin.close()


def main():
    CallRateFilter()
    
if __name__=='__main__':
    main()

