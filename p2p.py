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
__date__ = 'Nov 9 2013'
__version__ = '1'

# phonecodes
Stops = ['b', 'd', 'g', 'p', 't', 'k', 'dx', 'q']
Affricates = ['jh', 'ch']
Fricatives = ['s', 'sh', 'z', 'zh', 'f', 'th', 'v', 'dh']
Nasals = ['m', 'n', 'ng', 'em', 'en', 'eng', 'nx']
Glides = ['l', 'r', 'w', 'y', 'hh', 'hv', 'el']
Vowels = ['iy', 'ih', 'eh', 'ey',  'ae', 'aa', 'aw', 'ay', 'ah', 'ao', 'oy', 'ow', 'uh', 'uw', 'ux', 'er', 'ax', 'ix', 'axr', 'ax-h']
Others = ['pau', 'epi', 'h#']
PhoneCodes = Stops + Affricates + Fricatives + Nasals + Glides + Vowels + Others




