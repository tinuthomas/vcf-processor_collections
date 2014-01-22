#!/usr/bin/env python
"""
Date		:	02/11/2013
Purpose		:	Given two VCF files, merges the INFO fields for common variants and creates a new VCF file with the merged INFO column.
				Give the file with lesser variants as first file
Usage		:	python MergeINFO.py VCFfile1 VCFfile2 MergedVCFfile
"""

import sys
import re
from utils import return_file_handle

def MergeINFO(VCFfile1,VCFfile2):
	variant = {}
	fin1 = return_file_handle(VCFfile1)
	for line in fin1:
		line = line.strip().split('\t')
		if line[0] == '#CHROM':
			header = line
		elif re.search(r'^(\d+|X|Y)|^chr(\d+|X|Y)',line[0]):
			#line[0] = line[0].replace('chr','')  #optional
			ID = ':'.join(line[0:2]+line[3:5])
			variant[ID]	=	[line[2]] + line[5:] #stores the first VCF content in the dictionary named 'variant' with ID as 'Chr:Pos:Ref:Alt' as key and rest of the data as values			
	fin1.close()
	fin2 = return_file_handle(VCFfile2)
	for data in fin2:
		data = data.strip().split('\t')
		if data[0] == '#CHROM' :
			print'\t'.join(header)
		elif re.search(r'^(\d+|X|Y)|^chr(\d+|X|Y)',data[0]):
			temp_ID = ':'.join(data[0:2]+data[3:5]) #checks if each variant is present in the dictionary, then joins the info column and prints the output 
			if temp_ID in variant:		
				info_field = ';'.join([variant[temp_ID][3]] + [data[7]])
				print '\t'.join(data[0:7] + [info_field] + data[8:])

	fin2.close()
	
def main():
	try:
		VCFfile1 = sys.argv[1]
		VCFfile2 = sys.argv[2]
	except:
		print __doc__
	MergeINFO(VCFfile1,VCFfile2)
	
if __name__=='__main__':
	main()