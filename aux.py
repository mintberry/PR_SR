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
__date__ = 'Nov 7 2013'
__version__ = '1'

# read dict, key is a word, val is a list of phones
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
    text.close()

def read_phone(filename):
    text = codecs.open(filename, 'r', 'utf8')
    phones = []
    for line in text:
        phones.append(line.split()[-1])

    text.close()
    return phones

def sentence2phone(filename, lexicon_dict):
    text = codecs.open(filename, 'r', 'utf8')
    phones = ["h#"]
    sentence = []
    for line in text:
        phone = lexicon_dict[line.split()[-1]][0]
        phones = phones + phone
        sentence.append(line.split()[-1])

    text.close()
    phones.append("h#")
    return (phones, sentence)

def write_phone_dict(sid, input_dir, output_dir, lexicon_dict):
    f = codecs.open(output_dir + sid + '.p2p', 'w', 'utf8')

    (phones_dict, sentence) = sentence2phone(input_dir + sid + '.wrd', lexicon_dict);

    f.write(' '.join(sentence) + '\n')
    f.write(' '.join(phones_dict) + '\n')
    f.close()

def write_phone_obs(sid, input_dir, output_dir, lexicon_dict):
    f = codecs.open(output_dir + sid + '.p2p', 'a', 'utf8')

    phones_obs = read_phone(input_dir + sid + '.phn')

    f.write(' '.join(phones_obs) + '\n')

    f.close()


