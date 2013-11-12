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
from aux import *

___author__ = 'XH, XQ'
__date__ = 'Nov 9 2013'
__version__ = '1'

# align costs
# should use enum
cost_match = 0.0
cost_insert = 2.0
cost_sub = 1.0
cost_delete = 1.5

# class for alignment step
class Step:
    last = (0, 0)
    val = 0.0
    action = ''
    def __init__(self):
        pass

# class for decision tree node
class Node:
    children = None
    def __init__(self):
        self.children = defaultdict()
        pass    

# class of phoneme, including the decision tree
class Phoneme:
    pid = None
    root = None
    def __init__(self, id):
        self.pid = id
        self.root = Node()
        pass

    def add_change(self, change, context): # change(change_content, count)
        if context not in self.root.children.keys():
            self.root.children[context] = defaultdict()

        if change[0] not in self.root.children[context].keys():
            self.root.children[context][change[0]] = change[1]
        else:
            self.root.children[context][change[0]] += change[1]



# phonecodes
Stops = ['b', 'd', 'g', 'p', 't', 'k', 'dx', 'q', 6]
Affricates = ['jh', 'ch', 5]
Fricatives = ['s', 'sh', 'z', 'zh', 'f', 'th', 'v', 'dh', 4]
Nasals = ['m', 'n', 'ng', 'em', 'en', 'eng', 'nx', 3]
Glides = ['l', 'r', 'w', 'y', 'hh', 'hv', 'el', 2]
Vowels = ['iy', 'ih', 'eh', 'ey',  'ae', 'aa', 'aw', 'ay', 'ah', 'ao', 'oy', 'ow', 'uh', 'uw', 'ux', 'er', 'ax', 'ix', 'axr', 'ax-h', 1]
Others = ['pau', 'epi', 'h#', 0]
# add closure intervals

# init phone codes
def get_phone_class():
    PhoneCodes = []
    PhoneCodes.append(Stops)
    PhoneCodes.append(Affricates)
    PhoneCodes.append(Fricatives)
    PhoneCodes.append(Nasals)
    PhoneCodes.append(Glides)
    PhoneCodes.append(Vowels)
    PhoneCodes.append(Others)

    phone_class = defaultdict()
    for li in PhoneCodes:
        for phoneme in li[:-1]:
            phone_class[phoneme] = li[-1]

    return phone_class

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


def count_changes(pid, change, context, phoneme_trees):
    if pid not in phoneme_trees.keys():
        phoneme_trees[pid] = Phoneme(pid)

    phoneme_trees[pid].add_change(change, context)


# align phoneme-phone, while count changes on context
def align(phonemes, phones, phone_class, phoneme_trees, count_changes):
    # remove last 'h#' or keep it?
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
                    ('_' if phonemes[j] == phones[i] else phones[i] + '/' + phonemes[j])), \
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
        # add step and context
        change = (table[i][j].action, 1)
        context = (phone_class[phonemes[j - 1]], \
        phone_class[phonemes[j + 1]] if j + 1 != len(phonemes) else phone_class['h#']) # context now is a tuple of prev phone and next phoneme
        count_changes(phonemes[j], change, context, phoneme_trees)

        align_seq.insert(0, table[i][j].action)
        (i ,j) = table[i][j].last

    # print ' '.join(align_seq)

# align all pairs in a p2p file
def align_file(filename, phoneme_trees, phone_class):
    (phonemes, phones) = read_p2p(filename);
    for phone_seq in phones:
        align(phonemes, phone_seq, phone_class, phoneme_trees, count_changes)

def align_dir(p2p_dir):
    phoneme_trees = defaultdict()
    phone_class = get_phone_class()

    files = list_files_with(p2p_dir, '.p2p')
    for f in files:
        align_file(p2p_dir + f, phoneme_trees, phone_class)

    return phoneme_trees



