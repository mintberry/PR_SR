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
from random import *
from math import *

___author__ = 'XH, XQ'
__date__ = 'Nov 7 2013'
__version__ = '1'

# predefined paths
p2p_dir = '../timit_p2p/'
timit_dir_train = '../TIMIT/TRAIN/'
timit_dir_test = '../TIMIT/TEST/'
dict_dir = '../TIMITDIC.TXT'

# read dict, key is a word, val is a list of phones
def read_dict(filename, lexicon_dict):
    text = codecs.open(filename, 'r', 'utf8')
    for line in text:
        if line[0] != ';':
            key = line.split()[0]
            pronunciation = line[line.find('/') + 1:line.rfind('/')].split()
            # remove stress marker
            for idx, phone in enumerate(pronunciation):
                if phone[-1] == '1' or phone[-1] == '2':
                    pronunciation[idx] = phone[:-1]
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
        key = line.split()[-1]
        # irregular word in sentence, half workaround
        if key not in lexicon_dict.keys():
            if key == 'semi':
                key += '-'
            elif key == 'read':
                key += ('~v_past' if randint(0, 10) > 5 else '~v_pres')
            else:
                key += ('~n' if randint(0, 10) > 5 else '~v')
            if key == 'present~n' or key == 'separate~n':
                key += '~adj' 
            if key == 'close~n' or key == 'live~n':
                key = 'close~adj'
                
        phone = lexicon_dict[key][0]
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

def list_files_with(files_dir, suffix):
    return [f for f in os.listdir(files_dir) if f.find(suffix) != -1]


# generate p2p files for all sentences in a dialect region
def generate_p2p(dialect_region, lexicon_dict): # e.g. dr1/
    file_list = os.listdir(timit_dir_train + dialect_region)
    sid_dict = defaultdict()
    for subdir in file_list:
        if subdir[0] != '.':
            # find all sentences said by this person
            files = [f for f in os.listdir(timit_dir_train + dialect_region + subdir + '/') if f.find('.phn') != -1]
            for f in files:
                sid = f[:f.find('.phn')]
                if sid not in sid_dict.keys():
                    sid_dict[sid] = True
                filepath = timit_dir_train + dialect_region + subdir + '/' + sid + '.phn'  
                if os.path.isfile(filepath):
                    if sid_dict[sid]:
                        write_phone_dict(sid, timit_dir_train + dialect_region + subdir + '/', p2p_dir, lexicon_dict)
                        sid_dict[sid] = False 
                    write_phone_obs(sid, timit_dir_train + dialect_region + subdir + '/', p2p_dir, lexicon_dict)



