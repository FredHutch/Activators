import sys, os, re 
import pandas as pd
import numpy as np
from assign_scores import *

promoter = sys.argv[1].upper()

def main():
	# get df of promoter's sequences (from all bins, probably redundant)
	df = join_bins(promoter)
	_centroids = centroids(promoter)
	# In some clusters, there might be more than one sequence (centroid) to keep! Keep them im ALL_centroids
	ALL_centroids = []
	# It's not possible to buffer all files of clusters at once, therefore I do it sequentially
	for i in range(len(_centroids)):
		clusters = open_cluster(promoter, i)

		''' find the sequence with the highest number of reads 
			if there are several sequences with number of reads above 
			a threashold, include all of them and distribute all other 
			resudual reads between them '''
		
		# get all sequences with enough reads
		c = df.loc[clusters, ['bin1','bin2','bin3','bin4','pres']]
		cGood = c[c.sum(axis=1)>=10].index # This value is based on having ~5 times more sequences than the number of centroids ***
										   # *** Anyway, the script checks the number of reads of each seq, to avoid redundancies.
		cBad = c.loc[list(set(c.index)-set(cGood))].sum(axis=0) / len(cGood) 
		# sum cBad to each of the cGood sequences
		c = c.loc[cGood] + cBad
		df.loc[c.index].iloc[:,:5] = c
		ALL_centroids.append(c.index)
	# finally, save the updated df
	ALL_centroids = list(np.concatenate(ALL_centroids))
	df.loc[ALL_centroids].to_csv(promoter.lower()+'_ALLcentroids_reads.csv')
	#df.loc[_centroids].to_csv(promoter.lower()+'_centroids_reads.csv')	

def centroids(promoter):
	n, c = 0, []
	for i in open(promoter.lower()+'_centroids.fasta'):
		if n%2:
			c.append(i.strip())
		n+=1
	return(c)


def open_cluster(promoter, number):
	filename = './clusters/'+promoter.lower()+'/'+str(number)
	n, c = 0, []
	for i in open(filename):
		if n%2: c.append(i.strip())			
		n+=1
	return(c)


if __name__=='__main__': main()
