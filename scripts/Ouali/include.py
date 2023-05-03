'''
Created on 12 déc. 2019

@author: Abdelkader Ouali

Interpreter: Python 3
'''

import os
import sys
import datetime
import math
import random
import argparse
import re
import csv
import operator
import collections
import itertools
import time
import subprocess
#import numpy as np
import multiprocessing as mp
from multiprocessing import Process
import operator as op
from functools import reduce


# some basic function
def is_int(n):
    try:
        float_n = float(n)
        int_n = int(float_n)
    except ValueError:
        return False
    else:
        return float_n == int_n


def is_float(n):
    try:
        float_n = float(n)
    except ValueError:
        return False
    else:
        return True


def ncr(n, r):
    r = min(r, n - r)
    numer = reduce(op.mul, range(n, n - r, -1), 1)
    denom = reduce(op.mul, range(1, r + 1), 1)
    return numer / denom


def flatten(l):
    for el in l:
        if isinstance(el, collections.Iterable) and not isinstance(el, (str, bytes)):
            yield from flatten(el)
        else:
            yield el


def nestedCombLoop(cur_list, max_list):
    '''
    cur_list = [0, 2, 4], max_list = [1, 5, 7] --> [[0, 2, 4], [0, 2, 5], ..., [0, 4, 6]
    '''
    assert len(max_list) == len(cur_list) and len(max_list) > 0, "Wrong parameters to create nested combinations"
    tmp = range(cur_list[0], max_list[0])
    if len(max_list) == 1:
        return tmp
    for i in range(1, len(max_list)):
        l = []
        for p in itertools.product(tmp, range(cur_list[i], max_list[i])):
            l.append(p)
        tmp = l
    for t in tmp:
        ft = []
        for e in  flatten(t):
            ft.append(e)
        yield ft


# Print iterations progress
def printProgressBar (iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end=printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()


# set the root directory
cwd = os.path.dirname(os.path.realpath(__file__))
project_dir = os.path.abspath(os.path.join(cwd, os.pardir, os.pardir))

# preparing  project directories directories
project_bin_closed_diversity_new_file = os.path.abspath(os.path.join(project_dir, "target", "ClosedDiversityNew-choco4-0-3-jar-with-dependencies.jar"))
project_bin_closed_diversity_file = os.path.abspath(os.path.join(project_dir, "target", "ClosedDiversity-choco4-0-3-jar-with-dependencies.jar"))
project_bin_closed_diversity_onlylb_file = os.path.abspath(os.path.join(project_dir, "target", "ClosedDiversityOnlyLB-choco4-0-3-jar-with-dependencies.jar"))
project_bin_closed_diversity_topk_file = os.path.abspath(os.path.join(project_dir, "target", "ClosedDiversityTopK-choco4-0-3-jar-with-dependencies.jar"))
project_bin_closed_file = os.path.abspath(os.path.join(project_dir, "target", "ClosedPattern-choco4-0-3-jar-with-dependencies.jar")) 
project_bin_closed_diversity_falsepositive_file = os.path.abspath(os.path.join(project_dir, "target", "ClosedDiversityFalsePositive-choco4-0-3-jar-with-dependencies.jar"))
project_bin_closed_pattern_topk_file = os.path.abspath(os.path.join(project_dir, "target", "ClosedPatternTopK-choco4-0-3-jar-with-dependencies.jar"))
project_psm_lp_bin = os.path.abspath(os.path.join(project_dir, "bin", "pattern-set-mining"))
project_data_dir = os.path.abspath(os.path.join(project_dir, "data"))
project_res_dir = os.path.abspath(os.path.join(project_dir, "results"))

