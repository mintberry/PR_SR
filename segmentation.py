"""
COMPUTATIONAL LINGUISTICS

project: pronunciation recognition & sentence reconstruction

This module get the segmentation that maximizes the probability.
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
__date__ = 'Nov 10 2013'
__version__ = '1'

# predefined paths
dict_dir = '../TIMITDIC.TXT'


if __name__ == '__main__':
