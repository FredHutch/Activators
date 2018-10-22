#!/usr/bin/python

__author__ = "Lukasz Pawel Kozlowski"
__email__  = "lukaszkozlowski.lpk@gmail.com"
__copyrights__ = "Lukasz Pawel Kozlowski & Max Planck Institute for Biophysical Chemistry"

import os
import sys
import math
from multiprocessing import Pool
import multiprocessing
                
def author_information():
    '''add information about author'''
    print( '==============================================================================================\n' )
    print( '\t\t\t%s - SCRIPT FOR RUNNING NetSurfP ON MULTIPLE CPUs\n'%sys.argv[0] )
    print( 'AUTHOR: \t%s, %s'%(__author__, __email__))
    print( 'COPYRIGHTS: \t%s\n'%__copyrights__)
    print( '\t\t\t\t\tFebruary 2016' )
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

def slice_list(input_list, size):
    input_size = len(input_list)
    slice_size = int(input_size / size)
    remain = input_size % size
    result = []
    iterator = iter(input_list)
    for i in range(size):
        result.append([])
        for j in range(slice_size):
            result[i].append(next(iterator))
        if remain:
            result[i].append(next(iterator))
            remain -= 1
    return result

def runner(fasta_subfile_path):
    '''runs ronn_runner_mpi.py'''
    cmd = 'python netsurfp_runner_mpi.py %s'%fasta_subfile_path
    print(cmd)
    os.system(cmd)
    
if __name__ == '__main__': 
    #author_information()
    try: 
        FASTA_FILE = sys.argv[1].strip()
    except: 
        error_information()
        
    #get information about nuber of cpus in your system
    cpu = multiprocessing.cpu_count()
    
    #adjust cpu number according current load in your machine
    if cpu>1:
        system_load = int(math.ceil(os.getloadavg()[2]))
        cpu = cpu-system_load
        if cpu<1: cpu = 1
    cpu = 10    #hard coding cpu
    print('According system usage and CPU number script will be run on %s CPUs\n'%cpu)
 
    fasta_subfiles_names = []
    for c in range(int(cpu)):
        part_number = str(c+1)
        fasta_subfiles_name = FASTA_FILE.split('.fasta')[0] + '.part_' + part_number + '.fasta'
        fasta_subfiles_names.append(fasta_subfiles_name)

    fasta_out_tab = [] 
    fasta_tab = fasta_reader(FASTA_FILE)

    print('%s file (%s sequences) will be divided into %s subfiles:'%(FASTA_FILE, str(len(fasta_tab)), cpu))        
    parts = slice_list(fasta_tab, int(cpu))
    
    pattern = FASTA_FILE.split('.fasta')[0] + 'part*netsurfp_ss_acc.fasta'
    cmd = 'rm '+ pattern
    print(cmd)
    os.system(cmd)
    
    # creating subfiles
    sum_sublist = 0
    for n in range(0, len(parts)):
        #single file
        fasta_string_tmp = ''
        print('\tWriting: '+ fasta_subfiles_names[n])
        sum_sublist += len(parts[n])
        for query in parts[n]:
            tmp_sequence = query[0]
            tmp_header = query[1]
            fasta_string_tmp += tmp_header + os.linesep + tmp_sequence + os.linesep
            
        f = open(fasta_subfiles_names[n], 'w')
        f.write(fasta_string_tmp)
        f.close()
    print(sum_sublist)
    print('\n')
    
    #finally we have everything what is needed to run it in parallel 
    #e.g. python ronn_runner_mpi.py ./Samples_O1/test.part_4.fasta
    
    #################### PARALLELIZATION START #################### 
    pool = Pool(processes=cpu)               # start N worker processes on N CPUs
    vectorsTab2 = pool.map(runner, fasta_subfiles_names) # print out 
    ####################  PARALLELIZATION END  #################### 
    
    #glue all files
    FASTA_FILE_OUT = FASTA_FILE.split('.fasta')[0] + '.netsurfp_ss_acc.fasta'
    print('Merging subfiles into final file: '+FASTA_FILE_OUT) 
    
    pattern = FASTA_FILE.split('.fasta')[0] + '.part_*.netsurfp_ss_acc.fasta'
    cmd = 'cat %s > %s' % (pattern, FASTA_FILE_OUT)
    print(cmd)
    os.system(cmd)