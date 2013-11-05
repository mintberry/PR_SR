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

___author__ = 'XH, XQ'
__date__ = 'Nov 4 2013'
__version__ = '1'

# threshold
likelihood = 0.0001


# class for a table entry
class Cell:
    p_forward = 0.0
    p_backward = 0.0
    def __init__(self):
        pass

# language model
lexicon_dict = defaultdict()

# read model from file and random init
def read_dict(filename, lexicon_dict):
    text = codecs.open(filename, 'r', 'utf8')
    for line in text:
        if line[0] != ';':
            key = line.split()[0]
            pronunciation = line[line.find('/') + 1:line.rfind('/')].split()
            if key not in lexicon_dict.keys():
                lexicon_dict[key] = [pronunciation]
            else:
                lexicon_dict[key].append(pronunciation)

def read_observation(filename):
    f = codecs.open(filename, 'r', 'utf8')
    # text = f.read()
    lines = []
    for line in f:
        tokens = line.split()
        lines.append(tokens)
    return lines

if __name__=='__main__':   #main function

    read_dict(sys.argv[1], lexicon_dict)







    











