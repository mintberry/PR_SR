"""
COMPUTATIONAL LINGUISTICS

project: pronunciation recognition & sentence reconstruction
"""

from __future__ import division          #integer division
from collections import defaultdict
import random
import codecs          #to read and write unicode
import sys        #for command-line args
import string
import operator
import os
import re
import aux
from random import *
from math import *

___author__ = 'XH, XQ'
__date__ = 'Nov 24 2013'
__version__ = '1'

# predefined paths
p2p_dir = '../timit_p2p/'
timit_dir_train = '../TIMIT/TRAIN/'
timit_dir_test = '../TIMIT/TEST/'
dict_dir = '../TIMITDIC.TXT'

# FST, carmel
final_state = "FINAL"
start_state = "START"
epsilon = '*e*'

# lexicons from a dict
def read_dict_keys(filename, lexicon_dict):
    aux.read_dict(filename, lexicon_dict)

    return list(lexicon_dict.keys())


# generate an fsa of words for carmel to train
def lex_trans_fsa(dict_keys, filename):
    f = codecs.open(p2p_dir + filename, 'w', 'utf8')

    f.write(final_state + '\n')

    transitions = []
    emissions = []

    for next_word in dict_keys:
        transitions += ['(' + start_state + ' ' + '(' + next_word.upper() + ' *e* *e*))']

    print len(dict_keys)

    for word in dict_keys:
        self_state = word.upper()
        emit_state = self_state + '_e'
        # emit itself
        emissions += ['(' + self_state + ' ' + '(' + emit_state + ' *e* "' + word + '"))']

        # transition with final if "H#"
        # since the start and end state is h# now
        # if phoneme == 'h#':
        #     transitions += ['(' + final_state + ' ' + '(' + self_state + ' *e* *e*))']
        #     transitions += ['(' + emit_state + ' ' + '(' + final_state + ' *e* *e*))']

        for next_word in dict_keys:
            transitions += ['(' + emit_state + ' ' + '(' + next_word.upper() + ' *e* *e*))']

    for transition in transitions:
        f.write(transition + '\n')

    f.write('\n')

    for emission in emissions:
        f.write(emission + '\n')

    f.close()


# generate a emission wfst, based on the dictionary
def lex_emit_wfst(lexicon_dict, filename):
    f = codecs.open(p2p_dir + filename, 'w', 'utf8')

    f.write(final_state + '\n')

    for key in lexicon_dict.keys():

        emission = '(' + final_state + ' ' + '(' + final_state + ' ' + key + ' "' + ' '.join(lexicon_dict[key][0]) + '" ' + '1.0' + '))'
        f.write(emission + '\n')

    f.close()






