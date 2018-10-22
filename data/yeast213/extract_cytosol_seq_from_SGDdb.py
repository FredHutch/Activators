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
        tmp_uid = tmp[0].split()[0]
        fastaDict[tmp_uid] = [seq]

    return fastaDict

if __name__ == '__main__':
    
    try: cytosol_file = sys.argv[1] 
    except: 
        print('Error with input file: '+sys.argv[1])
        sys.exit(1)

    cytosol_protein_lines = open(cytosol_file).readlines()[1:]
    print(len(cytosol_protein_lines))
    cytosol_uids = []
    for line in cytosol_protein_lines:
        foo = line.split(',')
        uid = foo[1].replace('"', '').replace("'", "")
        fraction = foo[2].replace('"', '').replace("'", "")
        #print(uid, fraction)
        if fraction=='cytosol': cytosol_uids.append(uid)
    print(len(cytosol_uids))
    print(cytosol_uids[:10])    
    fastas = fasta_reader("orf_trans_all.fasta")
    print(len(fastas))
    print(fastas.values()[:10])
    SGD_ids = cytosol_uids

    print(len(fastas))
    print(SGD_ids[:5])

    #filter only those on list
    SGD_sequences = ''
    missing =0
    counter = 0
    too_many_threshold = 211
    for uid in SGD_ids:
        try: 
            query = fastas[uid]
            SGD_sequences += '>'+uid+os.linesep+query[0]+os.linesep
            counter += 1
            if counter>too_many_threshold: break
        except: 
            missing+=1

    OUTPUT_FASTA_FILE = cytosol_file.split('.')[0]+'.fas'
    print(counter)
    print('\n\nWritting to: '+OUTPUT_FASTA_FILE)
    f = open(OUTPUT_FASTA_FILE, 'w')
    f.write(SGD_sequences[:-1])
    f.close()
    print(missing)
