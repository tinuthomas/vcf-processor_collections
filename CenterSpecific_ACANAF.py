
#!/usr/bin/env python
"""
	This script would take AC, AN, AF fields from INFO column and adds center sepcific AC,AN, AF fields while 
	keeping original AC,AF, AN text intact. This would be useful when you want to merge VCFs with samples from different centers.
	
	Usage 	: python CenterSpecific_ACANAF.py VCF CenterName
	example : python CenterSpecific_ACANAF.py  Center_SimplexoSubset_GGA_VA_gatk2.6.4_Part2_07152013.vcf.gz Mayo
"""

import sys
import re
from utils import return_file_handle

def CenterSpecific_ACANAF():
    """
    This script would take AC, AN, AF fields from INFO column and adds center sepcific AC,AN, AF fields while 
	keeping original AC,AF, AN text intact
	
	Usage 	: python CenterSpecific_ACANAF.py VCF CenterName
	example : python CenterSpecific_ACANAF.py  Center_SimplexoSubset_GGA_VA_gatk2.6.4_Part2_07152013.vcf.gz Mayo
    """
    try:
        inVCF = sys.argv[1]
        CenterName = sys.argv[2]
    except:
        print CenterSpecific_ACANAF.__doc__
        sys.exit(-1)
    fin = return_file_handle(inVCF)
    for line in fin:
        line = line.strip().split('\t')
        if re.search(r'^(\d+|X|Y)|^chr(\d+|X|Y)', line[0]):
            flag_AF = 0
            flag_AC = 0
            flag_AN = 0
            for val in line[7].split(';'):
                if val.split('=')[0] == 'AF':
                    cname_AF = CenterName + '_AF=' + val.split('=')[1] + ';'
                    flag_AF = 1
                elif val.split('=')[0] == 'AC':
                    cname_AC = CenterName + '_AC=' + val.split('=')[1] + ';'
                    flag_AC = 1
                elif val.split('=')[0] == 'AN':
                    cname_AN = CenterName + '_AN=' + val.split('=')[1] + ';'
                    flag_AN = 1
            if flag_AF == 1 and flag_AC == 1 and flag_AN == 1:
                line[7] = cname_AC + cname_AF + cname_AN + line[7]
                print '\t'.join(line)
            else:
                print "Missing AC, AN or AF values for the variant",'\t'.join(line[0:6])
                sys.exit(-1)
        elif re.search(r'^#CHROM',line[0]):
            print '##INFO=<ID=' + CenterName + '_AC,Number=A,Type=Integer,Description="Center specific Allele count in genotypes, for each ALT allele, in the same order as listed">'
            print '##INFO=<ID=' + CenterName +'_AF,Number=A,Type=Float,Description="Center specific Allele Frequency, for each ALT allele, in the same order as listed">'
            print '##INFO=<ID=' + CenterName + '_AN,Number=1,Type=Integer,Description="Center specific Total number of alleles in called genotypes">'
            print '\t'.join(line)
        else:
            print '\t'.join(line)			
    fin.close()

def main():
    CenterSpecific_ACANAF()

if __name__ =='__main__':
    main()
