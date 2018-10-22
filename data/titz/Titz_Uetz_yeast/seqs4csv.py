#!/usr/bin/python

__author__ = "Lukasz Pawel Kozlowski"
__email__  = "lukaszkozlowski.lpk@gmail.com"
__copyrights__ = "Lukasz Pawel Kozlowski & Max Planck Institute for Biophysical Chemistry"

import os
import sys
import csv

def fasta_reader(inputFile):
    '''reads fasta file and return table [ [head1, seq1], [head2, seq2], ...]
    it is endure for all stupid errors like: multiple line for sequence, white spaces etc.'''
    fastaTab = open(inputFile).read().split('>')[1:]
    fastaDict = {}
    for n in range(0, len(fastaTab)):
        tmp = fastaTab[n].split(os.linesep)
        head = tmp[0].split()[0]
        seq = ''.join(tmp[1:]).replace('*', '')
        fastaDict[head]=seq
    return fastaDict

fastas = fasta_reader('yeast_orf_trans_all.fasta')

titz_data_tab = []
fasta_string = ''
with open('cleaned_TA.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        orf_name = row['ORF'].strip()
        LTH = row['LTH (3-AT)'].strip()
        if '>200' in LTH: LTH = 250
        else: LTH = float(LTH)
        
        #filter sequence
        seq = fastas[orf_name]
        fasta_string += '>' + orf_name + '\n' + seq + '\n'
        
        print(orf_name, str(LTH), len(seq))
        titz_data_tab.append( (orf_name, LTH, seq) )
    
print (len(titz_data_tab))

f = open('titz.fasta', 'w')
f.write(fasta_string)
f.close()

