#!/usr/bin/python

__author__ = "Lukasz Pawel Kozlowski"
__email__  = "lukaszkozlowski.lpk@gmail.com"
__copyrights__ = "Lukasz Pawel Kozlowski & Max Planck Institute for Biophysical Chemistry"

import os
import sys
                
def author_information():
    '''add information about author'''
    print( '==============================================================================================\n' )
    print( '\t\t\t%s - SCRIPT FOR RUNNING RONN ON MULTIPLE FASTA\n'%sys.argv[0] )
    print( 'AUTHOR: \t%s, %s'%(__author__, __email__))
    print( 'COPYRIGHTS: \t%s\n'%__copyrights__)
    print( '\t\t\t\t\tJanuary 2016' )
    print( '==============================================================================================\n' )    
    
def error_information():
    '''information how to run IPC script'''  
    print( "Usage:  python %s <fasta_file>\n"%sys.argv[0] )
    info_string = '''<fasta_file>    multiple fasta file'''             
    print(info_string)    
    sys.exit(1) 
    
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


def ronn_runner(seq, fasta_header = 'None'):
    '''runs RONN - protein disorder predictor based on ANN'''
    
    ronn_bin_path = '/home/lukaskoz/bin/RONNv3_1/'
    old_dir = os.getcwd()
    os.chdir(ronn_bin_path)

    #extend our peptides
    #highly project specific
    fasta_string = fasta_header + os.linesep + seq
    
    f = open('tmp.fasta', 'w')
    f.write(fasta_string)
    f.close()
    
    cmd = './RONN tmp.fasta 1'
    os.system(cmd)
    
    f = open('disorder.prb','r')
    ronnTab = f.readlines()
    
    disText = ''
    probTab = []
    for n in range(0, len(ronnTab)):
        score = float(ronnTab[n].split('\t')[1])
        
        #offset 40 in ASCII table for better visibility 
        probTab.append(str(chr(int(round(score*100, 0))+40) ) )

        if score >= 0.5: disText += 'D'
        else: disText += '-'
    probabilities = ''.join(probTab)
    
    #remove what was added
    #print(fasta_header)
    #print(sequence[3:33])
    #print(disorder_string)
    #print(disorder_quality)
    #print(len(probTab))
    os.chdir(old_dir)
    return disText, probabilities
    
if __name__ == '__main__': 
    #author_information()
    try: 
        FASTA_FILE = sys.argv[1].strip()
    except: 
        error_information()
    
    fasta_out_tab = [] 
    fasta_tab = fasta_reader(FASTA_FILE)
    print(len(fasta_tab))
    counter = 0
    

    FASTA_FILE_OUT = FASTA_FILE.split('.fasta')[0]+'.RONN_disorder.fasta'
    print('Writing result to:  '+FASTA_FILE_OUT)
    
    #write to fasta format (additional line for quality)
    for query in fasta_tab:
        sequence, fasta_header = query
        print(fasta_header, len(sequence))
        disorder_string, disorder_quality = ronn_runner(sequence, fasta_header)
        query_fasta_string = fasta_header + os.linesep + sequence + os.linesep + disorder_string + os.linesep + disorder_quality + os.linesep
        fasta_out_tab.append(query_fasta_string)
        #counter+=1
        #if counter%10==0: print(counter, fasta_header)
        #print(query_fasta_string)

    fasta_string = ''.join(fasta_out_tab)
    f = open(FASTA_FILE_OUT, 'w')
    f.write(fasta_string)
    f.close()

    

    