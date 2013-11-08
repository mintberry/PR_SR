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
from random import *
from math import *
from aux import *

___author__ = 'XH, XQ'
__date__ = 'Nov 4 2013'
__version__ = '1'

# predefined paths
p2p_dir = '../timit_p2p/'
timit_dir_train = '../TIMIT/TRAIN/'
timit_dir_test = '../TIMIT/TEST/'
dict_dir = '../TIMITDIC.TXT'

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
    read_dict(dict_dir, lexicon_dict)

    write_p2p(sys.argv[1], timit_dir_train + 'dr1/fcjf0/', p2p_dir, lexicon_dict)



