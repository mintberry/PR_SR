"""
COMPUTATIONAL LINGUISTICS

project: pronunciation recognition & sentence reconstruction

This module builds the word to phonemes wfst.
"""

from __future__ import division          #integer division
from collections import defaultdict
import random
import codecs          #to read and write unicode
import sys        #for command-line args
import string
import operator
import re
from aux import *

___author__ = 'XH, XQ'
__date__ = 'Nov 22 2013'
__version__ = '1'

# predefined paths
dict_dir = '../TIMITDIC.TXT'
word2phonemes_file = './wfst_w2p.fst'

#FST, carmel
final_state = "FINAL"
epsilon = '*e*'
big_prob = '1.0'


def get_word2phonemes_wfst(filename, lexicon_dict):
	with codecs.open(filename, 'w', 'utf8') as f:
		f.write(final_state + '\n')
		f.write('(FINAL (FINAL "start#" *e* 1.0))\n')
		f.write('(FINAL (FINAL "end#" *e* 1.0))\n')
		for key in lexicon_dict:
			phonemes = lexicon_dict[key][0]
			phonemes_len = len(phonemes)
			if phonemes_len == 1:
				f.write('(' + final_state + ' (' + final_state + ' "' + key + '" ' + ' "' + phonemes[0] + '" ' + big_prob + '))\n')
			else:
				for i in range(0, phonemes_len):
					if i == 0:
						f.write('(' + final_state + ' (' + key + '_' + str(i+1) + ' "' + key + '" ' + ' "' + phonemes[i] + '" ' + big_prob + '))\n')
					elif i != phonemes_len-1:
						f.write('(' + key + '_' + str(i) + ' (' + key + '_' + str(i+1) + ' ' + epsilon + ' "' + phonemes[i] + '" ' + big_prob + '))\n')
					else:
						f.write('(' + key + '_' + str(i) + ' (' + final_state + ' ' + epsilon + ' "' + phonemes[i] + '" ' + big_prob + '))\n')



if __name__ == '__main__':
	#read in the lexicon
	lexicon_dict = defaultdict(list)
	read_dict(dict_dir, lexicon_dict)

	print lexicon_dict['she']

	get_word2phonemes_wfst(word2phonemes_file, lexicon_dict)