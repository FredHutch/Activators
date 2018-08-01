print('=' * 80,'\n',
      'Calculate scores based on mean of bins for each FACS sorting\n', \
      'bins info used in this script should be found in bins_info.py')
print('=' * 80,'\n')

import pandas as pd
#from bins_info import *
import numpy as np
import re

'''get factors to score the sequences: 
    ARG1_factor 
    ARG3_factor 
    ILV6_factor
'''
#             ARG1         ILV6       ARG3
#    bin1 =   0-200       0-200      120- 400
#    bin2 = 370-570     300-400      400- 640
#    bin3 = 580-850     410-500      640-1000
#    bin4 = 850-inf     510-inf     1010-7500

ARG1_FACS_FU  = [[0, 200], [370, 570], [580, 850], [850, None]]
ARG1_FACS_RFU = [1.0, 4.7, 7.15, 9.85]

ILV6_FACS_FU  = [[0, 200], [300, 400], [410, 500], [510, None]]
ILV6_FACS_RFU = [1.0, 3.5, 4.55, 5.55]

ARG3_FACS_FU  = [[120, 400], [400, 640], [640, 1000], [1010, None]]
ARG3_FACS_RFU = [1.0, 2.0, 3.154, 4.577]



ARG1_bins = [[0, 200], [370, 570], [580, 850], [850, 1200]]
ILV6_bins = [[0, 200], [300, 400], [410, 500], [510, 650]]
ARG3_bins = [[120, 400], [400, 640], [640, 1000], [1010, 1600]]

# <promoter>_factor variables handy to use
for i in ['ARG1','ARG3','ILV6']:
    bins = i+'_bins'
    factor = i+'_factor' 
    vars()[factor] = np.mean(  np.vstack(eval(bins)), axis=1  )


def join_bins(promoter):
    promoter = promoter.upper()
    filenames = [promoter+"_bin"+str(i)+".counter" for i in range(1,5)] + [promoter+'_pre_sorting.counter']
    dfs = [pd.read_csv(i, header=None, names=['seq',i[5:9]]).set_index('seq') for i in filenames]
    df = pd.concat(dfs, axis=1, sort=True).fillna(0)
    return df

def join_cenntroids(promoter):
    promoter = promoter.upper()
    filenames = [promoter+"_bin"+str(i)+"_centroids.csv" for i in range(1,5)] + [promoter+'_pre_sorting.counter']
    dfs = [pd.read_csv(i, header=None, names=['seq',i[5:9]]).set_index('seq') for i in filenames]
    df = pd.concat(dfs, axis=1, sort=True).fillna(0)
    return df

# fx to calculate the score of the sequence based on its reads in background and bins 
def assign_score(promoter, df):
    factor_matrix = eval(promoter+'_factor')
    bins = [i for i in df.columns if re.search('bin',i)]
    df.loc[:,'scores'] = np.sum(df[bins] * factor_matrix, axis=1)
    # First attempt of normalization is dividing the scores by the total number of reads.
    df.loc[:,'norm_scores'] = df['scores'] / df.drop('scores', axis=1).sum(axis=1)
    df.loc[:,'norm2bg'] = df['scores'] / (df['pres']+1)
    df.loc[:,'new_scores'] = np.sum( [i/(j+1) for i,j in zip(df[['bin1','bin2','bin3','bin4']].values, df['pres'].values)] * factor_matrix, axis=1 )
    return df
