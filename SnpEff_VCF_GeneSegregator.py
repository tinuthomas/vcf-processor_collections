#!/usr/bin/env python
"""
Purpose     :   Given a VCF file or VCF file in text format with SnpEff, gives per gene count of total variants, nonsense, missense, silent, high impact, moderate impact
ProgramName :   SnpEff_VCF_GeneSegregator.py 
Author      :   Tinu Thomas
Date        :   10/25/2013
Purpose     :   Given a VCF
Usage       :   python SnpEff_VCF_GeneSegregator.py Option VCF >Output.vcf
                Option  -   1 or 2
                    1) SnpEff annotated VCF
                    2) SnpEff annotated VCF text file
                VCF -   Input VCF file
"""
import sys
import re
from utils import return_file_handle

def Snpeff_VCFtxt(inVCF):
    genes = {}
    fin = return_file_handle(inVCF)
    for line in fin:
        line = line.strip('\n\r').split('\t')
        if re.search(r'^#CHROM', line[0]):
            #nonsense_ct = missense_ct = silent_ct = frame_shift = high_impact = mod_impact = 0
            #function_callrank = avg_cons_scr = sum_D_C = ''
            genename_pos = func_class_pos = effect_pos = impact_pos = -9
            for pos,header in enumerate(line):
                if header == 'SNPEFF_GENE_NAME' :
                    genename_pos = pos
                elif header == 'SNPEFF_FUNCTIONAL_CLASS':
                    func_class_pos = pos
                elif header == 'SNPEFF_EFFECT' :
                    effect_pos = pos
                elif header == 'SNPEFF_IMPACT' :
                    impact_pos = pos
            if genename_pos == -9 or func_class_pos == -9 or effect_pos == -9 or impact_pos == -9:
                print 'SNPEFF annotation not found in this file ! '
                sys.exit(-1)
        elif re.search(r'^(\d+|X|Y)|^chr(\d+|X|Y)', line[0]):
            nonsense_ct = missense_ct = silent_ct = frame_shift = high_impact = mod_impact = nonsyn_cod = codchng_coddel = codchng_codins = stop_gain = splice_accep = splice_donor = cod_ins = cod_del = start_lost = stop_lost = 0
            genename = line[genename_pos]
            genename_ct = 1
            if line[func_class_pos] == 'MISSENSE' :
                missense_ct = 1     #Counter counting number of missense variants per gene
            elif line[func_class_pos] == 'NONSENSE' :
                nonsense_ct = 1     #Counter counting number of nonsense variants per gen
            elif line[func_class_pos] == 'SILENT' :
                silent_ct = 1       #Counter counting number of silent variants per gene
            
            if line[effect_pos] == 'FRAME_SHIFT' :
                frame_shift =1
            elif line[effect_pos] == 'NON_SYNONYMOUS_CODING' :
                nonsyn_cod =1
            elif line[effect_pos] == 'CODON_CHANGE_PLUS_CODON_DELETION' :
                codchng_coddel =1
            elif line[effect_pos] == 'CODON_CHANGE_PLUS_CODON_INSERTION' :
                codchng_codins =1
            elif line[effect_pos] == 'STOP_GAINED' :
                stop_gain =1
            elif line[effect_pos] == 'SPLICE_SITE_ACCEPTOR' :
                splice_accep =1
            elif line[effect_pos] == 'CODON_INSERTION' :
                cod_ins =1
            elif line[effect_pos] == 'CODON_DELETION' :
                cod_del =1
            elif line[effect_pos] == 'SPLICE_SITE_DONOR' :
                splice_donor =1
            elif line[effect_pos] == 'START_LOST' :
                start_lost =1
            elif line[effect_pos] == 'STOP_LOST' :
                stop_lost =1

            if line[impact_pos] == 'HIGH' or line[impact_pos] == 'Prob_high':
                high_impact =1 
            elif line[impact_pos] == 'MODERATE' :
                mod_impact =1 
            function_callrank = float(line[141])
            function_call_noData = float(line[142])
            if line[146] == 'None':
                 total_cons_scr = 0
            else:
                total_cons_scr = float(line[146])
            cons_noData = float(line[147])
            if genename not in genes:
                genes[genename] = [genename_ct, nonsense_ct, missense_ct, silent_ct, frame_shift, nonsyn_cod, codchng_coddel, codchng_codins, stop_gain, splice_accep, splice_donor, cod_ins, cod_del, start_lost, stop_lost, high_impact, mod_impact, function_callrank, total_cons_scr, function_call_noData, cons_noData]
            else:
                genes[genename][0] = genes[genename][0] + genename_ct
                genes[genename][1] = genes[genename][1] + nonsense_ct
                genes[genename][2] = genes[genename][2] + missense_ct
                genes[genename][3] = genes[genename][3] + silent_ct
                genes[genename][4] = genes[genename][4] + frame_shift
                genes[genename][5] = genes[genename][5] + nonsyn_cod
                genes[genename][6] = genes[genename][6] + codchng_coddel
                genes[genename][7] =  genes[genename][7] + codchng_codins
                genes[genename][8] =  genes[genename][8] + stop_gain
                genes[genename][9] = genes[genename][9] + splice_accep
                genes[genename][10] = genes[genename][10] + splice_donor
                genes[genename][11] = genes[genename][11] + cod_ins
                genes[genename][12] = genes[genename][12] + cod_del
                genes[genename][13] = genes[genename][13] + start_lost
                genes[genename][14] = genes[genename][14] + stop_lost
                genes[genename][15] = genes[genename][15] + high_impact
                genes[genename][16] = genes[genename][16] + mod_impact
                genes[genename][17] = genes[genename][17] + float(function_callrank)
                genes[genename][18] = genes[genename][18] + total_cons_scr
                genes[genename][19] = genes[genename][19] + function_call_noData
                genes[genename][20] = genes[genename][20] + cons_noData

    fin.close()
    print '\t'.join(['Gene', '#Variants', '#Nonsense', '#Missense', '#Silent', '#Frame_shift','#NonSyn_Coding','#Codonchange_plus_CodonDel','#Codonchange_plus_CodIns','#Stop_Gain','#Splice_Accep','#Splice_Donor','Cod_Ins','Cod_Del','#Start_Lost','#Stop_Lost','#High_Impact', '#Moderate_Impact', 'PerGene_FunctionalCallScr(#D)','PerGene_AvgConsScr','#MISSING_FUNCTIONALCALL_TRACKS','#MISSING_CONSERVATION_TRACKS'])
    for gname,values in genes.items():
        values[18] = values[18]/float(values[0])
        values = [ str(e) for e in values]
        print '\t'.join([gname] + values)

def Snpeff_VCF(inVCF):
    genes = {}
    fin = return_file_handle(inVCF)
    for line in fin:
        line = line.strip('\n\r').split('\t')
        if re.search(r'^(\d+|X|Y)|^chr(\d+|X|Y)', line[0]):
            if re.search(r'UBE2Q1',line[7]):
                print '\t'.join(line)
    """
            nonsense_ct = missense_ct = silent_ct = frame_shift = high_impact = mod_impact = 0
            for val in line[7].split(';'):
                if '=' in val and val.split('=')[0] == 'SNPEFF_GENE_NAME' :
                    genename = val.split('=')[1]
                    genename_ct = 1
                elif val.split('=')[0] == 'SNPEFF_FUNCTIONAL_CLASS' and val.split('=')[1] == 'MISSENSE' :
                    missense_ct = 1     #Counter counting number of missense variants per gene
                elif val.split('=')[0] == 'SNPEFF_FUNCTIONAL_CLASS' and val.split('=')[1] == 'NONSENSE':
                    nonsense_ct = 1     #Counter counting number of nonsense variants per gene
                elif val.split('=')[0] == 'SNPEFF_FUNCTIONAL_CLASS' and val.split('=')[1] == 'SILENT':
                    silent_ct = 1       #Counter counting number of silent variants per gene
                elif val.split('=')[0] == 'SNPEFF_EFFECT' and val.split('=')[1] == 'FRAME_SHIFT':
                    frame_shift =1
                elif val.split('=')[0] == 'SNPEFF_IMPACT' and val.split('=')[1] == 'HIGH':
                    high_impact =1 
                elif val.split('=')[0] == 'SNPEFF_IMPACT' and val.split('=')[1] == 'MODERATE':
                    mod_impact =1 
            if genename not in genes:
                genes[genename] = [genename_ct, nonsense_ct, missense_ct, silent_ct, frame_shift, high_impact, mod_impact ]
            else:
                genes[genename][0] = genes[genename][0] + genename_ct
                genes[genename][1] = genes[genename][1] + nonsense_ct
                genes[genename][2] = genes[genename][2] + missense_ct
                genes[genename][3] = genes[genename][3] + silent_ct
                genes[genename][4] = genes[genename][4] + frame_shift
                genes[genename][5] = genes[genename][5] + high_impact
                genes[genename][6] = genes[genename][6] + mod_impact
    fin.close()
    print '\t'.join(['Gene', '#Variants', '#Nonsense', '#Missense', '#Silent', '#Frame_shift', '#High_Impact', '#Moderate_Impact'])
    for gname,values in genes.items():
        values = [ str(e) for e in values]
        print '\t'.join([gname] + values)
    """

def main():
    try:
        option = float(sys.argv[1])
        inVCF = sys.argv[2]
    except:
        print __doc__
        sys.exit(-1)
    if type(option) is not float :
        print "Option must be numbers\nOption      -   1 or 2 or 3 \n1) SnpEff Gene annotation \n2) ANNOVAR refGene \n3)ANNOVAR ensGene\n"
        sys.exit(-1)
    elif option == 0 or option > 2 :
        print 'Option should be 1 or 2 or 3\n'
        sys.exit(-1)
    elif float(option) == 1 :
        Snpeff_VCF(inVCF)
    elif float(option) == 2:
        Snpeff_VCFtxt(inVCF)

if __name__=='__main__':
    main()






















