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

    # file_list = os.listdir(timit_dir_train + 'dr1/')
    # first_row = True
    # for subdir in file_list:
    #     if subdir[0] != '.':
    #         filepath = timit_dir_train + 'dr1/' + subdir + '/' + sys.argv[1] + '.phn'
    #         if os.path.isfile(filepath):
    #             if first_row:
    #                 write_phone_dict(sys.argv[1], timit_dir_train + 'dr1/' + subdir + '/', p2p_dir, lexicon_dict)
    #                 first_row = False 
    #             write_phone_obs(sys.argv[1], timit_dir_train + 'dr1/' + subdir + '/', p2p_dir, lexicon_dict)        

    (phonemes, phones) = read_p2p(p2p_dir + sys.argv[1] + '.p2p');
    align(phonemes, phones[0]) 






