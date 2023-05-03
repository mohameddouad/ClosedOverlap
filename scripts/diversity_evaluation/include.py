'''
Created on 12 déc. 2019

@author: Abdelkader Ouali
Last Update : Arnold (11/05/2020)

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
project_res_dir = os.path.abspath(os.path.join(project_dir, "results"))

project_bin_closed_file = os.path.abspath(os.path.join(project_dir, "target", "ClosedPattern-choco4-0-3-jar-with-dependencies.jar")) 
project_bin_closed_pattern_topk_file = os.path.abspath(os.path.join(project_dir, "target", "ClosedPatternTopK-choco4-0-3-jar-with-dependencies.jar"))

project_bin_closed_diversity_1_file = os.path.abspath(os.path.join(project_dir, "target", "ClosedDiversity_1-choco4-0-3-jar-with-dependencies.jar"))
project_bin_closed_diversity_1_estFreq_file = os.path.abspath(os.path.join(project_dir, "target", "ClosedDiversity_1_estFreq-choco4-0-3-jar-with-dependencies.jar"))
project_bin_closed_diversity_2_file = os.path.abspath(os.path.join(project_dir, "target", "ClosedDiversity_2-choco4-0-3-jar-with-dependencies.jar"))
project_bin_closed_diversity_2_estFreq_file = os.path.abspath(os.path.join(project_dir, "target", "ClosedDiversity_2_estFreq-choco4-0-3-jar-with-dependencies.jar"))
project_bin_closed_diversity_3_file = os.path.abspath(os.path.join(project_dir, "target", "ClosedDiversity_3-choco4-0-3-jar-with-dependencies.jar"))
project_bin_closed_diversity_3_estFreq_file = os.path.abspath(os.path.join(project_dir, "target", "ClosedDiversity_3_estFreq-choco4-0-3-jar-with-dependencies.jar"))

project_bin_closed_diversity_onlylb_file = os.path.abspath(os.path.join(project_dir, "target", "ClosedDiversityOnlyLB-choco4-0-3-jar-with-dependencies.jar"))
project_bin_closed_diversity_onlyub_file = os.path.abspath(os.path.join(project_dir, "target", "ClosedDiversityOnlyUB-choco4-0-3-jar-with-dependencies.jar"))
# project_bin_closed_diversity_falsepositive_file = os.path.abspath(os.path.join(project_dir, "target", "ClosedDiversityFalsePositive-choco4-0-3-jar-with-dependencies.jar"))

project_bin_closed_diversity_topk_file = os.path.abspath(os.path.join(project_dir, "target", "ClosedDiversityTopK-choco4-0-3-jar-with-dependencies.jar"))

project_bin_closed_diversity_checker_file = os.path.abspath(os.path.join(project_dir, "target", "ClosedDiversityChecker-choco4-0-3-jar-with-dependencies.jar"))

# project_flexics_script_file = os.path.abspath(os.path.join(project_dir, "scripts", "flexics", "flexics-experiments"))
# project_flexics_postprocess_file = os.path.abspath(os.path.join(project_dir, "scripts", "flexics", "postProcessingFlexics.py"))
project_flexics_data_dir = os.path.abspath(os.path.join(project_dir, "datasets"))

