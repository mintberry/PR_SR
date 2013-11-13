"""
COMPUTATIONAL LINGUISTICS

project: pronunciation recognition & sentence reconstruction

This module counts the corpus to get the language model.
"""

from __future__ import division          #integer division
from collections import defaultdict
import random
import codecs          #to read and write unicode
import sys        #for command-line args
import string
import operator

___author__ = 'XH, XQ'
__date__ = 'Nov 11 2013'
__version__ = '1'

# predefined paths
phonemes_file = './prompts_phonemes.txt'
unigram_model_file = './unigram_model_file.txt'
bigram_model_file = './bigram_model_file.txt'


def count_words(filename, uni_count_dict, pair_count_dict):
	'''Read in the prompts phonemes and count the frequency of each "word" and pair'''
	with codecs.open(filename, 'r', 'utf8') as f:
		for line in f:
			line = line.replace('\n', '')
			line = line.split('#')
			line_length = len(line)
			for i in range(0, line_length):
				uni_count_dict[line[i]] += 1
				if i <= line_length-2:
					pair_count_dict[line[i]+'&'+line[i+1]] += 1

def write_dict_to_file(filename, dict_to_write):
	'''Write the dict to file for future use'''
	with codecs.open(filename, 'w', 'utf8') as f:
		for key in dict_to_write:
			f.write(key + ' ' + str(dict_to_write[key]) + '\n')

if __name__ == '__main__':
	uni_count_dict = defaultdict(int)
	pair_count_dict = defaultdict(int)
	unigram_model = defaultdict(float)
	bigram_model = defaultdict(float)

	count_words(phonemes_file, uni_count_dict, pair_count_dict)

	# print uni_count_dict
	# print pair_count_dict

	# add dummy word <UNK>, has a great impact, must be very very small
	uni_count_dict['<UNK>'] = 1e-12

	#c ompute unigram probabilities
	word_tokens = sum(uni_count_dict.values())
	for phone_word in uni_count_dict:
		unigram_model[phone_word] = uni_count_dict[phone_word] / word_tokens

	# compute bigram probabilities and do linear interpolation
	unigram_weight = 0.05
	for pair in pair_count_dict:
		previous, current = pair.split('&')
		key = current + '|' + previous
		bigram_model[key] = pair_count_dict[pair] / uni_count_dict[previous]
		bigram_model[key] = (1-unigram_weight) * bigram_model[key] + unigram_weight * unigram_model[current]

	# wirte the computed LM to file
	write_dict_to_file(unigram_model_file, unigram_model)
	write_dict_to_file(bigram_model_file, bigram_model)

	