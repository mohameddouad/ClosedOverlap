#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 08:17:57 2020

@author: hien
"""

import matplotlib.pyplot as plt
import numpy as np
from include import *

fthresholds = {
#               "BMS1.dat" : ["0.0016", "0.0015", "0.0014", "0.0012"],
#               "connect.dat" : ["0.3"],
#               "german-credit.dat" : ["0.1", "0.01", "0.001", "0.025"],
               "hepatitis.dat" : ["0.2"]
#               "mushroom.dat" : ["0.05"],
#               "pumsb.dat" : ["0.4"],
#               "retail.dat" : ["0.05"],
#               "T10I4D100K.dat" : [ "0.05"],
#               "vote.dat" : ["0.1", "0.01", "0"],
#               "chess.dat" : ["0.2"],
#               "heart-cleveland.dat" : [ "0.3", "0.2", "0.1", "0.05"],
#               "kr-vs-kp.dat" : ["0.3"]
#               "primary-tumor.dat" : [ "0.1", "0.01", "0"],
#               "splice1.dat" : [ "0.1", "0.05", "0.01" ],
#               "T40I10D100K.dat" : [ "0.1", "0.01", "0.005" ],
#               'ijcai16.dat': ["0.3", "0.2", "0.1"]
               }

jmaxThresholds = {
#               "BMS1.dat" : ["0.0016", "0.0015", "0.0014", "0.0012"],
#               "connect.dat" : ["0.1", "0.2", "0.25", "0.3", "0.35", "0.4", "0.45", "0.5", "0.6", "0.7"],
#               "german-credit.dat" : ["0.1", "0.01", "0.001", "0.025"],
               "hepatitis.dat" : ["0.1", "0.2", "0.25", "0.3", "0.35", "0.4", "0.45", "0.5", "0.6", "0.7"],
#               "mushroom.dat" : ["0.1", "0.2", "0.25", "0.3", "0.35", "0.4", "0.45", "0.5", "0.6", "0.7"],
#               "pumsb.dat" : ["0.1", "0.2", "0.25", "0.3", "0.35", "0.4", "0.45", "0.5", "0.6", "0.7"],
#               "retail.dat" : ["0.1", "0.2", "0.25", "0.3", "0.35", "0.4", "0.45", "0.5", "0.6", "0.7"],
#               "T10I4D100K.dat" : ["0.1", "0.2", "0.25", "0.3", "0.35", "0.4", "0.45", "0.5", "0.6", "0.7"],
#               "vote.dat" : ["0.1", "0.01", "0"],
#               "chess.dat" : ["0.1", "0.2", "0.25", "0.3", "0.35", "0.4", "0.45", "0.5", "0.6", "0.7"],
#               "heart-cleveland.dat" : [ "0.3", "0.2", "0.1", "0.05"],
#               "kr-vs-kp.dat" : ["0.1", "0.2", "0.25", "0.3", "0.35", "0.4", "0.45", "0.5", "0.6", "0.7"]
#               "primary-tumor.dat" : [ "0.1", "0.01", "0"],
#               "splice1.dat" : [ "0.1", "0.05", "0.01" ],
#               "T40I10D100K.dat" : [ "0.1", "0.01", "0.005" ],
#               'ijcai16.dat': ["0.3", "0.2", "0.1"]
               }

# dataset = "connect.dat"
# dataset = "BMS1.dat"
aggreg = "MAX" # the aggregation function
timeout = "91800s"
npr = 10

searchstrategies = ["MINCOV", "FIRSTWITCOV"]

# this function should be changed based on solver logs 
def readResultClosed(absolute_dataset_res_file, absolute_dataset_ana_file, absolute_dataset_log_file):
    cputime = "100000"
    nbr_pattern = "*"
    nbr_nodes = "*"
    # extract
    if (os.path.exists(absolute_dataset_log_file)):
        with open(absolute_dataset_log_file, 'r') as logfile:
            for line in logfile:
                line_parse = re.findall(r'Exit status:[\s]+(\d+)', line)
                if line_parse:
                    if line_parse[0] == '0':
                        with open(absolute_dataset_ana_file, 'r') as anafile:
                            first_line = anafile.readline()
                            resval = first_line.split(';')
                            cputime = '{0:.2f}'.format(float(resval[-3]))
                            nbr_pattern = resval[-2]
                            nbr_nodes = resval[-1]  
                    elif line_parse[0] == '124':
                        cputime = "100000"
                        nbr_pattern = "*"
                        nbr_nodes = "*"
    return cputime, nbr_pattern, nbr_nodes

def readResultClosedDiversity(absolute_dataset_res_file, absolute_dataset_ana_file, absolute_dataset_log_file):
    cputime = "100000"
    nbr_pattern = "*"
    nbr_nodes = "*"
    nbr_pattern_witness = "*"
    nbr_var_filtred_lb = "*"
    # extract
    if (os.path.exists(absolute_dataset_log_file)):
        with open(absolute_dataset_log_file, 'r') as logfile:
            for line in logfile:
                line_parse = re.findall(r'Exit status:[\s]+(\d+)', line)
                if line_parse:
                    if line_parse[0] == '0':
                        with open(absolute_dataset_ana_file, 'r') as anafile:
                            first_line = anafile.readline()
                            resval = first_line.split(';')
                            cputime = '{0:.2f}'.format(float(resval[-7]))
                            nbr_pattern = resval[-5]
                            nbr_pattern_witness = resval[-3]
                            nbr_nodes = resval[-4]  
                            nbr_var_filtred_lb = resval[-2]
                            
    return cputime, nbr_pattern, nbr_nodes, nbr_pattern_witness, nbr_var_filtred_lb

def read_result_by_dataset(queue, project_res_dir, config):
    
    try:
        filename = config[0].split('.')[0]
        absolute_dataset_CP_res_dir = os.path.abspath(os.path.join(project_res_dir, "Closed", filename))
        absolute_dataset_CD_res_dir = os.path.abspath(os.path.join(project_res_dir, "ClosedDiversityNew", filename))
        absolute_dataset_graph_dir = os.path.abspath(os.path.join("graph", filename))
        
        os.makedirs(absolute_dataset_graph_dir, exist_ok=True)
        dataset_log_file = os.path.abspath(os.path.join(absolute_dataset_graph_dir, filename + "_all_config.log"))
        
        launch_log_file = open(dataset_log_file, "a")
        for threshold in config[1]:
            absolute_dataset_CP_res_file = os.path.abspath(os.path.join(
                absolute_dataset_CP_res_dir, filename + "-" + threshold.replace(".", "v") + ".res"))
            absolute_dataset_CP_ana_file = os.path.abspath(os.path.join(
                absolute_dataset_CP_res_dir, filename + "-" + threshold.replace(".", "v") + ".ana"))
            absolute_dataset_CP_log_file = os.path.abspath(os.path.join(
                absolute_dataset_CP_res_dir, filename + "-" + threshold.replace(".", "v") + ".log"))
            
            cputime_cp, nbr_pattern_cp, nbr_nodes_cp = readResultClosed(
                    absolute_dataset_CP_res_file, absolute_dataset_CP_ana_file, absolute_dataset_CP_log_file)
            
            data_cpu = ""
            data_pattern = ""
            data_nodes = ""
            i = 0
            for jmax in config[2]:
                i = i+1
                
                data_cpu = data_cpu + jmax + "\t" + str(i) + "\t" + cputime_cp
                data_pattern = data_pattern + jmax + "\t" + str((i*10)) + "\t" + nbr_pattern_cp
                data_nodes = data_nodes + jmax + "\t" + str((i*10)) + "\t" + nbr_nodes_cp.replace("\n", "")
                
                for strategy in config[3]:
                    data_cpu = data_cpu + "\t"
                    data_pattern = data_pattern + "\t"
                    data_nodes = data_nodes + "\t"
                    
                    absolute_dataset_CD_res_file = os.path.abspath(os.path.join(
                            absolute_dataset_CD_res_dir, filename + "-" + threshold.replace(".", "v") + 
                            "-" + jmax.replace(".", "v") + "-" + aggreg + "-" + strategy + "-0-" + timeout + ".res"))
                    absolute_dataset_CD_ana_file = os.path.abspath(os.path.join(
                            absolute_dataset_CD_res_dir, filename + "-" + threshold.replace(".", "v") + 
                            "-" + jmax.replace(".", "v") + "-" + aggreg + "-" + strategy + "-0-" + timeout + ".ana"))
                    absolute_dataset_CD_log_file = os.path.abspath(os.path.join(
                            absolute_dataset_CD_res_dir, filename + "-" + threshold.replace(".", "v") + 
                            "-" + jmax.replace(".", "v") + "-" + aggreg + "-" + strategy + "-0-" + timeout + ".log"))
                    
                    cputime_cd, nbr_pattern_cd, nbr_nodes_cd, nbr_pattern_witness_cd, nbr_var_filtred_lb_cd = readResultClosedDiversity(
                            absolute_dataset_CD_res_file, absolute_dataset_CD_ana_file, absolute_dataset_CD_log_file)
                    
                    data_cpu = data_cpu + cputime_cd
                    data_pattern = data_pattern + nbr_pattern_cd
                    data_nodes = data_nodes + nbr_nodes_cd
                    
                data_cpu = data_cpu + "\n"
                data_pattern = data_pattern + "\n"
                data_nodes = data_nodes + "\n"
            
            absolute_dataset_cpu_graph_file = os.path.abspath(os.path.join(absolute_dataset_graph_dir, filename + "_CPU.txt"))
            absolute_dataset_patterns_graph_file = os.path.abspath(os.path.join(absolute_dataset_graph_dir, filename + "_PATTERNS.txt"))
            absolute_dataset_nodes_graph_file = os.path.abspath(os.path.join(absolute_dataset_graph_dir, filename + "_NODES.txt"))
            
            write_graph_data(absolute_dataset_cpu_graph_file, data_cpu, "CPU")
            write_graph_data(absolute_dataset_patterns_graph_file, data_pattern, "Patterns number")
            write_graph_data(absolute_dataset_nodes_graph_file, data_nodes, "Nodes number")
            
    finally:
        queue.put(mp.current_process().name)

def write_graph_data(graph_data_file, graph_data, datatype):
    with open(graph_data_file, 'w') as f:
        f.write(graph_data)
        
    print("***", datatype, "graph data written in file *** \n\n\n")

if __name__ == '__main__':
    # checking required needed directories and files 
    if (not os.path.exists(project_data_dir)):
        print("Error: the data directory was not found")
        sys.exit(1)
    if (not os.path.exists(project_res_dir)):
        os.makedirs(project_res_dir, exist_ok=True)
    
    
    # loop on the dataset available in the data directory
    configs = []
    for filename in os.listdir(project_data_dir):
        if filename.endswith(".dat"):
            if filename in fthresholds:
                absolute_dataset_file = os.path.abspath(os.path.join(project_data_dir, filename))
                configs.append((filename, fthresholds[filename], jmaxThresholds[filename], searchstrategies))
                    
    curr = 0
    procs = dict()
    queue = mp.Queue()
    
    """
    manager = mp.Manager()
    allResults = manager.dict()
    """
    
    for i in range(0, npr):
        if curr < len(configs):
            # launch
            print(configs[i][0], configs[curr])
            proc = Process(target=read_result_by_dataset, args=(queue, project_res_dir, configs[curr],))
            proc.start()
            procs[proc.name] = proc
            curr += 1
    # using the queue, launch a new process whenever an old process finishes its workload
    while procs:
        name = queue.get()
        proc = procs[name]
        print(proc) 
        proc.join()
        del procs[name]
        if curr < len(configs):
            print(configs[i][0], configs[curr])
            proc = Process(target=read_result_by_dataset, args=(queue, project_res_dir, configs[curr],))
            proc.start()
            procs[proc.name] = proc
            curr += 1
    print("finished")
    
