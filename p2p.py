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
from operator import itemgetter

___author__ = 'XH, XQ'
__date__ = 'Nov 9 2013'
__version__ = '1'

# align costs
# should use enum
cost_match = 0.0
cost_insert = 2.0
cost_sub = 1.0
cost_delete = 1.5

# class for cell
class Step:
    last = (0, 0)
    val = 0.0
    action = ''
    def __init__(self):
        pass

# phonecodes
Stops = ['b', 'd', 'g', 'p', 't', 'k', 'dx', 'q']
Affricates = ['jh', 'ch']
Fricatives = ['s', 'sh', 'z', 'zh', 'f', 'th', 'v', 'dh']
Nasals = ['m', 'n', 'ng', 'em', 'en', 'eng', 'nx']
Glides = ['l', 'r', 'w', 'y', 'hh', 'hv', 'el']
Vowels = ['iy', 'ih', 'eh', 'ey',  'ae', 'aa', 'aw', 'ay', 'ah', 'ao', 'oy', 'ow', 'uh', 'uw', 'ux', 'er', 'ax', 'ix', 'axr', 'ax-h']
Others = ['pau', 'epi', 'h#']
PhoneCodes = Stops + Affricates + Fricatives + Nasals + Glides + Vowels + Others
# add closure intervals

# read p2p file for test
def read_p2p(filename):
    text = codecs.open(filename, 'r', 'utf8')
    phonemes = []
    phones = []
    linum = 0
    for line in text:
        if linum != 0:
            if linum == 1:
                phonemes = line.split()
            else:
                phones.append(line.split())
        linum += 1
    return (phonemes, phones)

# align phoneme-phone
def align(phonemes, phones):
    # remove last 'h#'
    phonemes = phonemes[0:-1]
    phones = phones[0:-1]

    table = []
    for i in range(len(phones)): # rows
        table.append([])
        for j in range(len(phonemes)): # columns
            step = Step()
            if i == 0 and j != 0:
                step.last = (i, j - 1)
                step.val = table[i][j - 1].val + cost_delete
                step.action = '-' + phonemes[j]
            elif i != 0 and j == 0:
                step.last = (i - 1, j)
                step.val = table[i - 1][j].val + cost_insert
                step.action = '+' + phones[i]
            elif i != 0 and j != 0:
                last_steps = [(table[i - 1][j - 1].val + (0.0 if phonemes[j] == phones[i] else cost_sub), (i - 1, j - 1), \
                    ('*' if phonemes[j] == phones[i] else '*' + phones[i] + '/' + phonemes[j])), \
                (table[i - 1][j].val + cost_insert, (i - 1, j), '+' + phones[i]), \
                (table[i][j - 1].val + cost_delete, (i, j - 1), '-' + phonemes[j])]
                finest = min(last_steps, key=itemgetter(0))
                step.last = finest[1]
                step.val = finest[0]
                step.action = finest[2]
            table[i].append(step)

    # best alignment sequence
    (i, j) = (len(phones) - 1, len(phonemes) - 1)
    align_seq = []
    while (i ,j) != (0, 0):
        align_seq.insert(0, table[i][j].action)
        (i ,j) = table[i][j].last

    print ' '.join(align_seq)

    



