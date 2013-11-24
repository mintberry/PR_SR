"""
COMPUTATIONAL LINGUISTICS

project: pronunciation recognition & sentence reconstruction

This module translates all the prompts to their phonemes.
"""

from __future__ import division          #integer division
from collections import defaultdict
import random
import codecs          #to read and write unicode
import sys        #for command-line args
import string
import operator
import re
from random import *
from math import *
from aux import *

___author__ = 'XH, XQ'
__date__ = 'Nov 10 2013'
__version__ = '1'

# predefined paths
dict_dir = '../TIMITDIC.TXT'
prompts_dir = '../writable_prompts.txt'
trimmed_prompts_file = '../trimmed_prompts.txt'
hand_trimmed_prompts_file = '../hand_trimmed_prompts.txt'
phonemes_file = './prompts_phonemes.txt'

hashtag_added_prompts_file = '../hashtag_added_prompts.txt'

def read_prompts(filename):
	'''Read in the prompts'''
	with codecs.open(filename, 'r', 'utf8') as f:
		prompts = []
		for line in f:
			if line[0] != ';':
				line = line.split('(')[0]
				line = re.sub(r'([,.!?;:"])', r' ', line)
				line = re.sub(r'--', r' ', line)
				prompts.append(line)

	return prompts

def read_trimmed_prompts(filename):
	'''Read in the trimmed prompts'''
	with codecs.open(filename, 'r', 'utf8') as f:
		trimmed_prompts = []
		for line in f:
			if line[0] != ';':
				trimmed_prompts.append(line)

	return trimmed_prompts

def write_trimmed_prompts(filename, prompts):
	with codecs.open(filename, 'w', 'utf8') as f:
		for line in prompts:
			f.write(line + '\n')

def trimmed_prompts_to_phonemes(filename, prompts, lexicon_dict):
	'''Look up each word in the lexicon and translate prompts to phonemes'''
	with codecs.open(filename, 'w', 'utf8') as f:
		for line in prompts:
			line = line.split()
			phonemes = []
			for word in line:
				word = word.lower()
				if word in lexicon_dict:
					phoneme = ''.join(lexicon_dict[word][0])
				else:
					phoneme = 'XXX'
				phonemes.append(phoneme)
			f.write('#'.join(phonemes) + '\n')

def add_hashtag_to_trimmed_prompts(filename, prompts):
	'''For each line of prompts, add h# to both head and tail of the sentence'''
	with codecs.open(filename, 'w', 'utf8') as f:
		for line in prompts:
			f.write('start# ' + line[:-2] + 'end#\n')

if __name__ == '__main__':
	#read in the lexicon
	lexicon_dict = defaultdict(list)
	read_dict(dict_dir, lexicon_dict)

	# read in the prompts
	# trimmed_prompts = read_prompts(prompts_dir)
	# write the trimmed prompts to file
	# write_trimmed_prompts(trimmed_prompts_file, trimmed_prompts)

	# after hand modification, read in the trimmed prompts
	trimmed_prompts = read_trimmed_prompts(hand_trimmed_prompts_file)

	# write the phonemes of each prompt sentence to file
	# trimmed_prompts_to_phonemes(phonemes_file, trimmed_prompts, lexicon_dict)

	# add h# to prompts
	add_hashtag_to_trimmed_prompts(hashtag_added_prompts_file, trimmed_prompts)