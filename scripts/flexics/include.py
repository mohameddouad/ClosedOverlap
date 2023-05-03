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
import subprocess
import numpy as np
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

def ncr(n, r):
    r = min(r, n-r)
    numer = reduce(op.mul, range(n, n-r, -1), 1)
    denom = reduce(op.mul, range(1, r+1), 1)
    return numer / denom

# set the root directory
cwd = os.path.dirname(os.path.realpath(__file__))
project_dir = os.path.abspath(os.path.join(cwd, os.pardir, os.pardir))

# preparing  project directories directories
project_data_dir = os.path.abspath(os.path.join(project_dir, "data"))

project_flexics_data_dir = os.path.abspath(os.path.join(project_dir, "datasets"))
project_res_dir = os.path.abspath(os.path.join(project_dir, "results"))

project_flexics_script_file = os.path.abspath(os.path.join(project_dir, "scripts", "flexics", "flexics-experiments"))
project_flexics_postprocess_file = os.path.abspath(os.path.join(project_dir, "scripts", "flexics", "postProcessingFlexics.py"))

project_bin_closed_diversity_new_file = os.path.abspath(os.path.join(project_dir, "target", "ClosedDiversityNew-choco4-0-3-jar-with-dependencies.jar"))

