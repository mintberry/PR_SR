"""
COMPUTATIONAL LINGUISTICS

project: pronunciation recognition & sentence reconstruction

This module use DP to get the phonemes segmentation that maximizes the probability.
"""

from __future__ import division          #integer division
from collections import defaultdict
import random
import codecs          #to read and write unicode
import sys        #for command-line args
import string
import operator
from random import *
from math import *

___author__ = 'XH, XQ'
__date__ = 'Nov 10 2013'
__version__ = '1'

# predefined paths
unigram_model_file = './unigram_model_file.txt'
bigram_model_file = './bigram_model_file.txt'
observation_file = './observation1.txt'
seg_result_file = './seg_result.txt'

def read_model(filename, model_dict):
	'''Read in the LM from file'''
	with codecs.open(filename, 'r', 'utf8') as f:
		for line in f:
			key, val = line.split()
			model_dict[key] = float(val)

def read_observatoin(filename):
	'''Read in the observations from file'''
	observations = []
	with codecs.open(filename, 'r', 'utf8') as f:
		for line in f:
			line = line.replace('\n', '')
			observations.append(line)

	return observations

if __name__ == '__main__':
	unigram_model = defaultdict(float)
	bigram_model = defaultdict(float)

	read_model(unigram_model_file, unigram_model)
	read_model(bigram_model_file, bigram_model)

	# print bigram_model

	observations = read_observatoin(observation_file)
	# print observations

	# DP to get the segmentation that maximizes the probabilities
	unigram_weight = 0.05
	each_seg = defaultdict(list)  # dict that holds segmentation for each position in DP
	each_seg[0] = ['#']
	with codecs.open(seg_result_file, 'w', 'utf8') as f:
		for line in observations:
			line = '#' + line
			L = [0] * len(line)
			for i in range(1, len(line)):
				max_prob = -999999
				for j in range(0, i):
					current = line[j+1 : i+1]
					previous = each_seg[j][-1]
					bigram_key = current + '|' + previous
					if bigram_key in bigram_model:
						new_prob = L[j] + log(bigram_model[bigram_key], 2)
						# print bigram_key, new_prob, max_prob
					elif current in unigram_model:
						new_prob = L[j] + log(unigram_weight * unigram_model[current], 2)
					else:
						new_prob = L[j] + log(unigram_model['<UNK>'], 2)

					if new_prob > max_prob:
						max_prob = new_prob
						argmax_j = j
				
				L[i] = max_prob
				each_seg[i] = list(each_seg[argmax_j])
				# print argmax_j
				each_seg[i].append(line[argmax_j+1 : i+1])

			f.write('#'.join(each_seg[i][1:]) + '\n')