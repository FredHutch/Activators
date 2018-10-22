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

def netsurfp_runner(seq, fasta_header = '>test', cpu_number = '13'):
    '''runs NetSurfP - protein secondary structure and solvent accessibility predictor based on ANN'''
    
    netsurfp_bin_path = '/home/lukaskoz/bin/netsurfp-1.0_%s/'%cpu_number
    old_dir = os.getcwd()
    os.chdir(netsurfp_bin_path)

    #extend our peptides
    #highly project specific
    fasta_string = fasta_header + os.linesep + seq
    
    f = open('tmp.fasta', 'w')
    f.write(fasta_string)
    f.close()
    
    cmd = './netsurfp -i tmp.fasta -a -o tmp_%s.out > /tmp/log_netsurfp_runner.txt 2>&1 '%cpu_number
    os.system(cmd)
    
    f = open('tmp_%s.out'%cpu_number,'r')
    netsurfp_lines = f.readlines()
    # Column 1: Class assignment - B for buried or E for Exposed - Threshold: 25% exposure, based on 1.st layer networks and not based on RSA
    # Column 2: Amino acid
    # Column 3: Sequence name
    # Column 4: Amino acid number
    # Column 5: Relative Surface Accessibility - RSA
    # Column 6: Absolute Surface Accessibility
    # Column 7: Z-fit score
    # Column 8: Probability for Alpha-Helix
    # Column 9: Probability for Beta-strand
    # Column 10: Probability for Coil
    
    # remove comments
    netsurfp_lines = [a for a in netsurfp_lines if not a.startswith('#')]
    #print(netsurfp_lines)
    rsaText = ''
    rsa_tab = []
    ssText = ''
    ss_prob_tab = []
    
    for lines in netsurfp_lines:
        tmp = lines.split()
        #print(tmp)
        acc = tmp[0]
        if acc=='E': acc='-'
        rsaText += acc
        
        # Relative Surface Accessibility
        rsa = float(tmp[4])
        # offset 40 in ASCII table for better visibility 
        rsa = str(chr(int(round(rsa*100, 0))+40) ) 
        rsa_tab.append(rsa)
        
        #secondary structure
        probH = float(tmp[-3])
        probE = float(tmp[-2])
        probC = float(tmp[-1])
        
        if probH > probE and probH > probC: 
            ssText+='H'
            prob = probH
        elif probE > probH and probE > probC: 
            ssText+='E'
            prob = probE
        else: 
            ssText+='-'
            prob = probC
        # offset 40 in ASCII table for better visibility 
        prob_ascii = str(chr(int(round(prob*100, 0))+40) ) 
        ss_prob_tab.append(prob_ascii)     
        
    rsa_probabilities = ''.join(rsa_tab)    
    ss_probabilities = ''.join(ss_prob_tab)
    
    
    # remove what was added
    rsa_string = rsaText
    rsa_probabilities_string = rsa_probabilities
    
    ssText_string = ssText
    ss_probabilities_string = ss_probabilities
    
    os.chdir(old_dir)
    return rsa_string, rsa_probabilities_string, ssText_string, ss_probabilities_string
    
if __name__ == '__main__': 
    #author_information()
    try: 
        FASTA_FILE = sys.argv[1].strip()
    except: 
        error_information()
    
    fasta_out_tab = [] 
    fasta_tab = fasta_reader(FASTA_FILE)
    
    FASTA_FILE_OUT = FASTA_FILE.split('.fasta')[0]+'.netsurfp_ss_acc.fasta'
    print('Writing result to:  '+FASTA_FILE_OUT)
    #print(fasta_tab)
    
    
    #write to fasta format (additional line for quality) 
    counter = 0
    for query in fasta_tab:
        counter += 1
            
        sequence, fasta_header = query
        if counter%5==0:
            print(fasta_header + ' ' + str(counter))
            
        rsa_string, rsa_probabilities, ssText_string, ss_probabilities_string = netsurfp_runner(sequence, fasta_header)
        query_fasta_string = fasta_header + os.linesep + sequence + os.linesep + rsa_string + os.linesep + rsa_probabilities + os.linesep + ssText_string + os.linesep + ss_probabilities_string + os.linesep
        #query_fasta_string = fasta_header + os.linesep + sequence + os.linesep + rsa_string + os.linesep + ssText_string + os.linesep

        fasta_out_tab.append(query_fasta_string)
        
    fasta_string = ''.join(fasta_out_tab)    
    f = open(FASTA_FILE_OUT, 'w')
    f.write(fasta_string)
    f.close()
    