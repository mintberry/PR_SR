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

# FST, carmel
final_state = "FINAL"
start_state = "START"
epsilon = '*e*'

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

def count_alignment(align_table, phonemes, phones, phone_class, phoneme_trees, count_changes):
    # best alignment sequence
    (i, j) = (len(phones) - 1, len(phonemes) - 1)
    last_j = j + 1
    last_j_changes = ''
    align_seq = []
    while (i ,j) != (0, 0):
        align_seq.insert(0, align_table[i][j].action)
        
        # add step and context
        last_j_changes = (align_table[i][j].action if last_j != j else (align_table[i][j].action + ' ' + last_j_changes))
        
        change = (last_j_changes, 1)
        context = (phone_class[phonemes[j - 1]], \
            phone_class[phonemes[j + 1]] if j + 1 != len(phonemes) else phone_class['h#']) # context now is a tuple of prev phone and next phoneme

        last_j = j
        count_changes(phonemes[j], change, context, phoneme_trees)
        
        (i ,j) = align_table[i][j].last

    # print ' '.join(align_seq)
    return align_seq


# align phoneme-phone, while count changes on context
def align(phonemes, phones, phone_class, phoneme_trees, count_alignment, count_changes):
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


    align_seq = count_alignment(table, phonemes, phones, phone_class, phoneme_trees, count_changes)

    return align_seq

# align all pairs in a p2p file
def align_file(filename, phoneme_trees, phone_class):
    (phonemes, phones) = read_p2p(filename);
    align_seqs = []
    for phone_seq in phones:
        align_seqs.append(align(phonemes, phone_seq, phone_class, phoneme_trees, count_alignment, count_changes))

    return align_seqs

def align_dir(p2p_dir):
    phoneme_trees = defaultdict()
    phone_class = get_phone_class()

    align_seqs = []
    files = list_files_with(p2p_dir, '.p2p')
    for f in files:
        align_seqs += align_file(p2p_dir + f, phoneme_trees, phone_class)

    # f = codecs.open(p2p_dir + 'alignments', 'w', 'utf8')

    # for align_seq in align_seqs:
    #     f.write(' '.join(align_seq) + '\n')    

    # f.close()

    return phoneme_trees

'''
with the decision tree model, generate FSTs for carmel
given conanical phonemes, produce surface with variation
train FSA separately
'''
def split_change(phoneme, union_dict):
    linear_dict = {}

    aux_dict = {}
    for change in union_dict.keys():
        change_li = change.split()
        change_counts = len(change_li)
        for idx, sub_change in enumerate(change_li):
            last_change = ''
            if 0 == idx:
                last_change = phoneme
            else:
                last_change = epsilon

            if (str(idx) + ' ' + str(change_counts) + ' ' + last_change + ' ' + sub_change) not in linear_dict.keys():
                linear_dict[str(idx) + ' ' + str(change_counts) + ' ' + last_change + ' ' + sub_change] = union_dict[change]
            else:
                linear_dict[str(idx) + ' ' + str(change_counts) + ' ' + last_change + ' ' + sub_change] += union_dict[change]

            charge_counts = change_counts if idx != 0 else idx
            if (str(idx) + ' ' + str(charge_counts) + ' ' + last_change) not in aux_dict.keys():
                aux_dict[str(idx) + ' ' + str(charge_counts) + ' ' + last_change] = union_dict[change]
            else:
                aux_dict[str(idx) + ' ' + str(charge_counts) + ' ' + last_change] += union_dict[change]

    # normalize
    for key in linear_dict.keys():
        last_change = ' '.join(key.split()[0:3])
        if last_change.split()[0] == '0':
            last_change = '0 0 ' + last_change.split()[-1]
        linear_dict[key] /= aux_dict[last_change]

    return linear_dict


def changes2emissions(phoneme, union_dict, total_changes):
    emissions = []
    # normalize union_dict
    for change in union_dict.keys():
        union_dict[change] /= total_changes
    
    linear_dict = split_change(phoneme, union_dict)

    for key in linear_dict.keys():
        state_number = int(key.split()[0])
        state_count = int(key.split()[1])
        token_in = '"' + key.split()[2] + '"'
        token_out = align_symbol = key.split()[3]
        prob = linear_dict[key]
        if align_symbol[0] == '-':
            token_out = epsilon
        elif align_symbol[0] == '_':
            token_out = '"' + phoneme + '"'
        elif align_symbol[0] == '+':
            token_out = '"' + align_symbol[1:] + '"'
        else: # replace
            token_out = '"' + align_symbol[:align_symbol.find('/')] + '"'

        cur_state = final_state if state_number == 0 else (phoneme + '_' + str(state_number) + '_' + str(state_count))
        next_state = final_state if state_number == state_count - 1 else (phoneme + '_' + str(state_number + 1) + '_' + str(state_count))

        emissions += ['(' + cur_state + ' ' + '(' + next_state + ' ' + token_in + ' ' + token_out + ' ' + str(prob) + '))']

    return emissions

def dtree2wfst(phoneme_trees, filename):
    f = codecs.open(p2p_dir + filename, 'w', 'utf8')

    f.write(final_state + '\n');
    
    for phoneme in phoneme_trees.keys():
        # here ignore the context, union all changes for this phoneme
        union_dict = {}
        total_changes = 0
        for context_dict in phoneme_trees[phoneme].root.children.values():
            for change in context_dict.keys():
                total_changes += context_dict[change]
                if change not in union_dict.keys():
                    union_dict[change] = context_dict[change]
                else:
                    union_dict[change] += context_dict[change]

        # write union_dict
        emissions = changes2emissions(phoneme, union_dict, total_changes)
        for emission in emissions:
            f.write(emission + '\n')

    f.close()




