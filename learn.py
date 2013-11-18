#!/usr/bin/env python

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
from random import *
from math import *
from aux import *
from p2p import *

___author__ = 'XH, XQ'
__date__ = 'Nov 4 2013'
__version__ = '1'

# threshold

# class for a table entry
class Cell:
    p_forward = 0.0
    p_backward = 0.0
    def __init__(self):
        pass

# language model
lexicon_dict = defaultdict()


if __name__=='__main__':   #main function
    # read_dict(dict_dir, lexicon_dict) 
    # generate_p2p('dr1/', lexicon_dict)        

    phoneme_trees = align_dir(p2p_dir)
    dtree2wfst(phoneme_trees, p2p_dir + 'wfst_p2p.fst')
    # transition_fsa(get_phone_class(), p2p_dir + 'fsa_p2p.fsa')

    wfsa_reformat(p2p_dir + 'wfsa_p2p.fsa', p2p_dir + 'wfsa_p2p_n.fsa')
    






