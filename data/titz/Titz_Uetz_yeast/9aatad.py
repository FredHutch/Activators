#!/usr/bin/python

__author__ = "Lukasz Pawel Kozlowski"
__email__  = "lukaszkozlowski.lpk@gmail.com"
__copyrights__ = "Lukasz Pawel Kozlowski & Max Planck Institute for Biophysical Chemistry"

import os
import sys
import time
import sys, traceback, copy
import urllib
import urllib2
import pickle
import fcntl
import socket
import re
import random

def fasta_reader(inputFile):
    '''reads fasta file and return table [ [head1, seq1], [head2, seq2], ...]
    it is endure for all stupid errors like: multiple line for sequence, white spaces etc.'''
    fastaTab = open(inputFile).read().split('>')[1:]
    fastaList = []
    for n in range(0, len(fastaTab)):
        tmp = fastaTab[n].split(os.linesep)
        head = '>'+tmp[0]
        seq = ''.join(tmp[1:])
        fastaList.append([seq, head])
    return fastaList


def predict_9aatad(seq, flavour=1):
    ''' send data to Piskacek et al. 2007 9aaTAD server'''
    
    matches = []
    
    piskacek_flavours = [#"[MDENQSTYG]{KRHCGP}[ILVFWM]{KRHCGP}{CGP}{CGP}[ILVFWM]{CGP}{CGP}",
                         #"[MDENQSTYG]{KRHCGP}[ILVFWM]{KRHCGP}{CGP}{KRHCGP}[ILVFWM][ILVFWMAY]{KRHC}",
                         #"[MDENQSTYCPGA]X[ILVFWMAY]{KRHCGP}{CGP}{CGP}[ILVFWMAY]XX",
                         #"XX[ILVFWMAY]{GP}{GP}[ILVFWMAY]{GP}XX",
                         "XX[W]XX[L][F]XX",
                         ]
    #print flavour, piskacek_flavours[flavour]
    #parameters of php form
    parms = [('sequence', seq),
             ('pattern', piskacek_flavours[flavour]),
             ('submit', 'Start Analysis'),
             ('rc[]', 1),('rc[]', 2),('rc[]', 3),
             ('rc[]', 4),('rc[]', 5),('rc[]', 6),
             ('rc[]', 7),('rc[]', 8),('rc[]', 9),
             ('rc[]', 10),('rc[]', 11),('rc[]', 12),
             ]
        
    php_url = 'http://www.med.muni.cz/9aaTAD/analysis.php#matches'
    timeout = 90
    socket.setdefaulttimeout(timeout)
    
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = {'User-Agent' : user_agent}
    data = urllib.urlencode(parms)
    req = urllib2.Request(php_url, data, headers)
    
    
    
    f = urllib2.urlopen(req)
    #print(req, php_url, f,data)
    d = copy.deepcopy(f.read(500))
    #f = urllib2.urlopen(php_url, urllib.urlencode(parms))
    
    try: 
        htmlPage = d
        htmlPage += f.read()
    except: 
            #print 'failed to open whole, maybe partial'
            htmlPage = d
            
    if '<h4>No match.</h4>' in htmlPage: return matches
    
    htmlPage = htmlPage.split('<a name="matches"')[1].split('</table>')[0].replace(' class="bold"', '')
    matches_html = htmlPage.split('<tr><td>')[1:]
    
    for match_html in matches_html:
        seq9aa = match_html.split('</td')[0]
        start = int(match_html.split('</td><td>')[1].split('<')[0])
        end = int(match_html.split('</td><td>')[2].split('<')[0])
        percent_match = match_html.split(' match')[0].split('>')[-1]
        if '%' in percent_match: percent_match=float(percent_match[:-1])
        elif 'Perfect' in percent_match: percent_match=100.0
        #print seq9aa, start, end, percent_match
        matches.append((seq9aa, start, end, percent_match))
    f.close()
    tab = htmlPage.split('<td>')
    
    return matches

if __name__ == '__main__': 
    FASTA_FILE = sys.argv[1].strip()
    
    fasta_out_tab = [] 
    fasta_tab = fasta_reader(FASTA_FILE)
    #print(len(fasta_tab))
    counter = 0

    FASTA_FILE_OUT = FASTA_FILE.split('.fasta')[0]+'XXWXXLFXX.9aatad_.fasta'
    #print('Writing result to:  '+FASTA_FILE_OUT)
    fasta_string = ''
    
    #write to fasta format (additional line for quality)
    for query in fasta_tab:
        seq, fasta_header = query
        print(fasta_header, len(seq))
        for counter in range(1):
            first  = predict_9aatad(seq, counter)
            if len(first)==0: first_score = 0
            else: first_score = sum([n[-1] for n in first])
            fasta_string += fasta_header+'|model'+str(counter+1)+' '+str(round(first_score,2)) +'\n'+seq+'\n'
            fasta_string += '\n'.join([n[0]+' '+str(n[1])+' '+str(n[2])+' '+str(n[3]) for n in first])+'\n'
    
    f = open(FASTA_FILE_OUT, 'w')
    f.write(fasta_string)
    f.close()    