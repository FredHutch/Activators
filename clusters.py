import sys, os, re 
import pandas as pd
import numpy as np
from assign_scores import *

HELP = 'python clusters.py <promoter> <bin> --> e.g. python clusters.py ARG3 bin1 (bin3, pre_sorting, ...)'

if len(sys.argv) < 2:
    print(HELP)
    print('\n\n')
    sys.exit(1)


promoter = sys.argv[1].upper()
binn = sys.argv[2]
output = '_'.join([promoter, binn, 'centroids']) + '.csv'

def main():
    df = pd.read_csv('_'.join([promoter, binn]) + '.counter', header=None, index_col=0, names=['counts'])
    # get df of promoter's sequences (from all bins, probably redundant)
    # In some clusters, there might be more than one sequence (centroid) to keep! Keep them im ALL_centroids
    ALL_centroids = []
    # It's not possible to buffer all files of clusters at once, therefore I do it sequentially
    #for i in range(len(_centroids)):
    cluster_names = os.scandir('./clusters/' + binn)
    while True:
        try:
            cluster_name = next(cluster_names).name
            clusters = open_cluster('./clusters/' + binn +'/' + cluster_name)

            ''' find the sequence with the highest number of reads 
                if there are several sequences with number of reads above 
                a threashold, include all of them and distribute all other 
                resudual reads between them '''
        
            # get all sequences with enough reads
            c = df.loc[clusters] #, ['bin1','bin2','bin3','bin4','pres']]
            cGood = c.sort_values('counts', ascending=False).index[0]
            ALL_centroids.append(cGood)
        except StopIteration: 
            break

    # finally, save the updated df
    #ALL_centroids = list(np.concatenate(ALL_centroids))
    df.loc[ALL_centroids].to_csv(output, header=False)



def open_cluster(filename):
    n, c = 0, []
    for i in open(filename):
        if n%2: c.append(i.strip())         
        n+=1
    return(c)


if __name__=='__main__': main()
