#!/usr/bin/env python
"""
Purpose	:	Given a file with gene names, and parsed vcf text file, will filter variants from VCF file which has genes in the Gene file
Usage   :   python /CommonDATA/Python_Scripts/FilterGenesFromVCFtxt.py vcf_txt_file GenesFile
"""
import sys
import re 
from utils import return_file_handle

def Filter_Genes_FromVCFtxt(vcf_txt_file, GenesFile):
	fgenes = return_file_handle(GenesFile)
	genes = {}
	gene_ct =0 
	for line in fgenes:
		line = line.strip().split('\t')
		genes[line[0]] = 1			#Getting Gene names and storing them in the dictinary named 'genes'
	fgenes.close()
	fin = return_file_handle(vcf_txt_file) #Opening vcf Family Distribution text file
	for data in fin:
		data = data.strip().split('\t')
		if data[0] == '#CHROM':
			print '\t'.join(data)
			for k,x in enumerate(data[0:]):
				if x == 'SNPEFF_GENE_NAME':
					pos = k
			continue
		elif re.search(r'^(\d+|X|Y|M)',data[1]):	
			if data[pos] in genes:
				gene_ct = gene_ct + 1
				print '\t'.join(data)
	fin.close()

def main():
	try:
		vcf_txt_file = sys.argv[1]
		GenesFile = sys.argv[2]	
	except:
		print __doc__
	Filter_Genes_FromVCFtxt(vcf_txt_file, GenesFile)

if __name__== '__main__':
	main()
