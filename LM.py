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
import re
from random import *
from math import *
from aux import *

___author__ = 'XH, XQ'
__date__ = 'Nov 10 2013'
__version__ = '1'

# predefined paths
dict_dir = '../TIMITDIC.TXT'
prompts_dir = '../PROMPTS.TXT'
trimmed_prompts_file = '../trimmed_prompts.txt'
phonemes_file = '../prompts_phonemes.txt'

def read_prompts(filename):
	with codecs.open(filename, 'r', 'utf8') as f:
		prompts = []
		for line in f:
			if line[0] != ';':
				line = line.split('(')[0]
				line = re.sub(r'([,.!?])', r' ', line)
				prompts.append(line)

	return prompts

def write_trimmed_prompts(filename, prompts):
	with codecs.open(filename, 'w', 'utf8') as f:
		for line in prompts:
			f.write(line + '\n')

def trimmed_prompts_to_phonemes(filename, prompts, lexicon_dict):
	with codecs.open(filename, 'w', 'utf8') as f:
		for line in prompts:
			line = line.split()
			phonemes = ['h#']
			for word in line:
				word = word.lower()
				if word in lexicon_dict:
					phoneme = lexicon_dict[word][0]
				else:
					phoneme = ['XXX']
				phonemes = phonemes + phoneme
			phonemes.append('h#')
			f.write(' '.join(phonemes) + '\n')

if __name__ == '__main__':
	#read in the lexicon
	lexicon_dict = defaultdict(str)
	read_dict(dict_dir, lexicon_dict)

	#read in the prompts
	trimmed_prompts = read_prompts(prompts_dir)

	#write the trimmed prompts to file
	write_trimmed_prompts(trimmed_prompts_file, trimmed_prompts)

	#write the phonemes of each prompt sentence to file
	trimmed_prompts_to_phonemes(phonemes_file, trimmed_prompts, lexicon_dict)