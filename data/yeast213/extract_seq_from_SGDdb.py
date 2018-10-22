#!/usr/bin/python

__author__ = "Lukasz Pawel Kozlowski, Johannes Soding"
__email__  = "lukaszkozlowski.lpk@gmail.com, soeding@mpibpc.mpg.de"
__copyrights__ = "Max Planck Institute for Biophysical Chemistry"

import os, sys

def fasta_reader(inputFile):
    '''reads fasta file and return table [ [head1, seq1], [head2, seq2], ...]
    it is endure for all stupid errors like: multiple line for sequence, white spaces etc.'''
    fastaTab = open(inputFile).read().split('>')[1:]
    fastaDict = {}
    for n in range(0, len(fastaTab)):
        tmp = fastaTab[n].split(os.linesep)
        head = '>'+tmp[0]
        seq = ''.join(tmp[1:]).replace('*', '')
        #print(head, seq)
        if 'SGDID:' in head: 
            SGD_id = head.split('SGDID:')[1].split(',')[0]
            fastaDict[SGD_id] = [head, seq]

    return fastaDict

if __name__ == '__main__':
    
    try: SGD_fasta_file = sys.argv[1] 
    except: 
        print('Error with input file: '+sys.argv[1])
        sys.exit(1)

    try: SGD_id_file = sys.argv[2] 
    except: 
        print('Error with input file: '+sys.argv[2])
        sys.exit(1)

    fastas = fasta_reader(SGD_fasta_file)
    SGD_ids = [n.strip() for n in open(SGD_id_file).readlines()]

    print(len(fastas))
    print(SGD_ids[:5])

    #filter only those on list
    SGD_sequences = ''
    for uid in SGD_ids:
        query = fastas[uid]
        SGD_sequences += query[0]+os.linesep+query[1]+os.linesep

    OUTPUT_FASTA_FILE = SGD_id_file.split('.')[0]+'.fas'
    print(len(SGD_ids))
    print('\n\nWritting to: '+OUTPUT_FASTA_FILE)
    f = open(OUTPUT_FASTA_FILE, 'w')
    f.write(SGD_sequences[:-1])
    f.close()
