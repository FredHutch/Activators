#!/usr/bin/python

__author__ = "Lukasz Pawel Kozlowski"
__email__  = "lukaszkozlowski.lpk@gmail.com"
__copyrights__ = "Lukasz Pawel Kozlowski & Max Planck Institute for Biophysical Chemistry"

import os
import sys
import csv
from scipy.stats.stats import pearsonr
from scipy import stats
import matplotlib
import matplotlib.pyplot as plt
    

def fasta_reader(inputFile):
    '''reads fasta file and return table [ [head1, seq1], [head2, seq2], ...]
    it is endure for all stupid errors like: multiple line for sequence, white spaces etc.'''
    fastaTab = open(inputFile).read().split('>')[1:]
    fastaDict = {}
    for n in range(0, len(fastaTab)):
        tmp = fastaTab[n].split(os.linesep)
        head = tmp[0]
        seq = ''.join(tmp[1:]).replace('*', '')
        fastaDict[head]=seq
    return fastaDict


if __name__ == '__main__':
    fastas = fasta_reader('titz.9aatad.fasta')
    heads = fastas.keys()
    #print heads
    model1_results = {}
    model2_results = {}
    model3_results = {}
    model4_results = {}    
    for head in heads:
        uid = head.split('|')[0]
        score = float(head.split()[-1])
        if 'model1' in head: model1_results[uid]=score
        elif 'model2' in head: model2_results[uid]=score
        elif 'model3' in head: model3_results[uid]=score  
        elif 'model4' in head: model4_results[uid]=score     
        
    titz_data = {}
    titz_data2 = {}
    with open('cleaned_TA.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            orf_name = row['ORF'].strip()
            LTH = row['LTH (3-AT)'].strip()
            
            if '>200' in LTH: LTH = 250.0
            else: LTH = float(LTH)
            
            bGAL = row['bGAL (+/- SEM)'].strip()
            
            if 'NA' in bGAL: bGAL = 0.0
            else: 
                bGAL = float(bGAL.split('+')[0])
            
            #print(orf_name, str(LTH))
            titz_data[orf_name]=LTH
            titz_data2[orf_name]=bGAL
            
    print (len(titz_data))
    #print model1_results
    titz_tab = []
    titz_tab2 = []
    model1_tab = []
    model2_tab = []
    model3_tab = []
    model4_tab = []
    for head, score in titz_data.items():
        titz_tab.append(score)
        titz_tab2.append(titz_data2[head])
        model1_tab.append(model1_results[head])
        model2_tab.append(model2_results[head])
        model3_tab.append(model3_results[head])
        model4_tab.append(model4_results[head])        
        
    r2 =  pearsonr(titz_tab, model1_tab)[0]
    print('model1 r^2 ' + str(round(r2,4)))
    r2 =  pearsonr(titz_tab, model2_tab)[0]
    print('model2 r^2 ' + str(round(r2,4)))
    r2 =  pearsonr(titz_tab, model3_tab)[0]
    print('model3 r^2 ' + str(round(r2,4)))
    r2 =  pearsonr(titz_tab, model4_tab)[0]
    print('model4 r^2 ' + str(round(r2,4)))

    r2 =  pearsonr(titz_tab, titz_tab2)[0]
    print('Titz2 r^2 ' + str(round(r2,4)))
    
    #plt.scatter(titz_tab, model1_tab, alpha=0.5)
    #plt.show()
    #plt.scatter(titz_tab, model2_tab, alpha=0.5)
    #plt.show()
    #plt.scatter(titz_tab, model3_tab, alpha=0.5)
    #plt.show()
    plt.scatter(titz_tab, titz_tab2, alpha=0.5)
    plt.show() 
    #plt.scatter(model2_tab, model1_tab, alpha=0.5)
    #plt.show()
    x = titz_tab
    x.sort()
    print(len(x))
    #plt.hist(titz_tab, alpha=0.5)
    plt.show()