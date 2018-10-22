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
    fastaTab = open(inputFile).read().split('>@')[1:]
    fastaList = []
    for n in range(0, len(fastaTab)):
        tmp = fastaTab[n].split(os.linesep)
        head = '>@'+tmp[0]
        seq = ''.join(tmp[1:])
        if len(seq)==30: fastaList.append([seq, head])
    return fastaList


def fasta_reader2(inputFile):
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


def psipred_runner(seq, fasta_header = 'None', cpu_number = '0'):
    '''runs psipred - protein secondary structure predictor'''
    
    psipred_bin_path = '/home/lukaskoz/bin/psipred2_%s/'%cpu_number
    old_dir = os.getcwd()
    os.chdir(psipred_bin_path)

    # extend our peptides
    # highly project specific
    # we run 79 aa long protein fragments to void problems with prediction on ends e.g. 21 sliding window (C-terminus)
    #seq = 'MSA' + seq.strip() + 'GDNDIPAGTDDVSLADKAIESTEEVSLVPSNLEVSTTSFLPTPVLE'
    seq = seq.strip()
    fasta_string = fasta_header + os.linesep + seq
    
    f = open('tmp.fasta', 'w')
    f.write(fasta_string)
    f.close()
    
    #run it
    cmd = './runpsipred tmp.fasta > tmp.log'
    os.system(cmd)
    
    #parse it
    f = open('tmp.horiz','r')
    ssTab = f.readlines()
    
    #we take information from horizontal view, quality only in 10 step resolution
    confLines = []
    predLines = []
    for line in ssTab:
        if line.startswith('Conf: '):
            try: 
                conf = line.split()[1]
                confLines.append(conf)
            except: confLines.append('')
            
        elif line.startswith('Pred: '):
            try: prediction = line.split()[1].replace('C', '-')      # '-' is easer to see than 'C'
            except: prediction = ''           
            predLines.append(prediction)
    probabilities = ''.join(confLines)
    ssText = ''.join(predLines)   
    #print(seq)
    #print(ssText)
    #print(probabilities)
    #remove what was added
    ss_string = ssText
    ss_quality = probabilities  
    #print()
    #print(ss_string)
    #print(ss_quality)
    os.chdir(old_dir)
    return ss_string, ss_quality
    
if __name__ == '__main__': 
    #author_information()
    try: 
        FASTA_FILE = sys.argv[1].strip()
        cpu_number = FASTA_FILE.split('part_')[1].split('.')[0]
        #cpu_number = sys.argv[2].strip()
    except: 
        error_information()
    
    fasta_out_tab = [] 
    fasta_tab = fasta_reader2(FASTA_FILE)
    print(str(len(fasta_tab)))
    FASTA_FILE_OUT = FASTA_FILE.split('.fasta')[0]+'.PSIPRED_ss.fasta'
    print('Writing result to:  '+FASTA_FILE_OUT)
        
    #write to fasta format (additional line for quality) 
    counter = 0
    for query in fasta_tab:
        counter += 1
        if counter%50==0:
            print(FASTA_FILE + ' '+ str(cpu_number) + ' ' + str(counter))
            
        sequence, fasta_header = query
        ss_string, ss_quality = psipred_runner(sequence, fasta_header, cpu_number)
        #except: print(sequence, fasta_header)
        query_fasta_string = fasta_header + os.linesep + sequence + os.linesep + ss_string + os.linesep + ss_quality + os.linesep
        fasta_out_tab.append(query_fasta_string)
        
    fasta_string = ''.join(fasta_out_tab)    
    f = open(FASTA_FILE_OUT, 'w')
    f.write(fasta_string)
    f.close()
    
