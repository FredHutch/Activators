import numpy as np
import sys,os,re
import pandas as pd

#features_names = positive, negative, polar_uncharged, hydrophobic, others, aromaticity
#p  = positive
#n  = negative
#l  = polar_uncharged
#h  = hydrophobic
#o  = others
#a  = aromatic
#ha = a+h

# define dictionary of features to translate
aa =        ['R','H','K','D','E','S','T','N','Q','A','V','L','I','M','F' ,'Y', 'W', 'C','G','P']
features =  ['p','p','p','n','n','l','l','l','l','h','h','h','h','h','ha','ha','ha','o','o','o']
features_dictionary = dict(zip(aa,features))

# fx to assign the features to sequence
def assign_features_seq(seq): 
    return([features_dictionary[i] for i in seq])

# get all unique sequences
list_of_fastas = [i for i in os.listdir() if re.search('.fasta',i)]
sequences = []
for f in list_of_fastas:
    for n,i in enumerate(open(f)):
        if n%2!=0: sequences.append(i.strip())
sequences = list(set(sequences))

# select only sequences with length==30
sequences = [i for i in sequences if len(i)==30]

# get df with 1-hot encoding variables
seqs_df = pd.DataFrame([[i for i in j] for j in sequences], index=sequences)
seqs_df = pd.get_dummies(seqs_df)

# get df with 1-hot encoding for the features 
seqs_df2 = pd.get_dummies(pd.DataFrame([assign_features_seq(i) for i in sequences], index=sequences))

# merge the two along axis 1
input_data = pd.concat([seqs_df, seqs_df2], axis=1)

