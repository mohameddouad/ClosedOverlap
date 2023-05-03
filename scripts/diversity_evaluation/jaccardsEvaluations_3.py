# -*- coding: utf-8 -*-
"""
Created on 28 may 2020

@author: hien

Interpreter: Python 3
"""

import sys
# from multiprocessing import Process
import multiprocessing as mp
from datetime import date, datetime


# number of parallel launches
npr = 5
# allDiversity = dict()

def parseResults(path):
    with open(path, 'r') as f:
        content = f.readlines()
        patternsLabel = []
        allPatterns = []
        allCovers = []
        for line in content:
            elements = line.split("] [")
            
            patternsLabel.append(elements[0].replace("[", "").replace(" ", "")) 
            allPatterns.append(elements[1][1:-1])
            allCovers.append(elements[2].replace("]", "")[1:-1])
        
    return patternsLabel, allPatterns, allCovers

def getAllCoversInt(covers):
    coverInt = []
    for cover in covers:
        coverInt.append(set(map(int, set(cover.split(" ")))))
    
    return coverInt

def evaluate_Jaccard(covX, covY):
    temp = covX
    covX = covX.union(covY)
    covY = covY.intersection(temp)
    jaccard = 0
    if(len(covX) > 0):
        jaccard = len(covY)/len(covX)
    
    return jaccard

def evaluate_LB_Jaccard(covX, covY, seuil):
    covP_X = covX.difference(covY)
    num = seuil - len(covP_X)
    denom = len(covY) + len(covP_X)
    lb = 0
    if(num > 0):
        lb = num/denom
    
    return lb

def evaluate_UB_Jaccard(covX, covY, seuil):
    ub = 1.0
    covP_Y = covY.difference(covX)
    cov_X_intersect_Y = covX.intersection(covY)
    
    if len(cov_X_intersect_Y) < seuil:
        ub = len(cov_X_intersect_Y)/(seuil+len(covP_Y))
    else:
        ub = len(cov_X_intersect_Y)/(len(cov_X_intersect_Y)+len(covP_Y))
    
    if ub > 1.0:
        ub = 1.0
    
    return ub

def evaluate_one_itemset_diversity(queue, allDiversity, itemset_index, patternsLabel, 
                                   patternsTab, coversSetTab, coversTab, seuil):
    
    queue.put(mp.current_process().name)
    
    lb = 0.0
    jaccard = 0.0
    ub = 0.0
    
    first = False
    lbl = -1
    for j in range(0, itemset_index):
        '''
        if int(patternsLabel[j]) != 0:
            if patternsLabel[j] == patternsLabel[itemset_index]:
                continue
            if not first:
                first = True
                lbl = patternsLabel[j]
            else if patternsLabel[j] != lbl:
                lbl = -1
                first = False
            else:
                continue
        else:
            first = False
        '''
        
        lbj = evaluate_LB_Jaccard(coversSetTab[itemset_index], coversSetTab[j], 
                                  seuil)
        ubj = evaluate_UB_Jaccard(coversSetTab[itemset_index], coversSetTab[j], 
                                  seuil)
        jac = evaluate_Jaccard(coversSetTab[itemset_index], coversSetTab[j])
        
        if lbj < 0:
            lbj = 0.0
        if ubj > 1:
            ubj = 1.0
        
        lb = max(lb, lbj)
        jaccard = max(jaccard, jac)
        ub = max(ub, ubj)
    
    allDiversity[patternsTab[itemset_index]] = [lb, jaccard, ub]
    """
    print("[", patternsLabel[itemset_index], "] [", patternsTab[itemset_index], "]", 
          allDiversity[patternsTab[itemset_index]], "")
    """

def evaluate_all_itemsets_diversity(allDiversity, patternsLabel, patternsTab, 
                                    coversSetTab, coversTab, seuil):
    procs = dict()
    
    if len(patternsLabel) == 0:
        print("ERROR, there's no itemsets")
        sys.exit(1)
    else:
        l0 = "[ " + str(patternsLabel[0] )+ " ] [ " + str(patternsTab[0])
        l0 += " ] [ " + str(coversTab[0]) + " ] [ 0.0 1.0 1.0 ]"
        
        allDiversity[patternsTab[0]] = [0.0, 1.0, 1.0]
        queue = mp.Queue()
        
        curr = 1 # iterator on itemsets to evaluate
        for iterPar in range(0, npr):
            if curr < len(patternsTab):
                allDiversity[patternsTab[curr]] = [0.0, 1.0, 1.0]
                proc = mp.Process(target=evaluate_one_itemset_diversity, 
                               args=(queue, allDiversity, curr, patternsLabel, 
                                   patternsTab, coversSetTab, coversTab, seuil,))
                proc.start()
                procs[proc.name] = proc
                curr += 1
            
        # using the queue, launch a new process whenever
        # an old process finishes its workload
        while procs:
            name = queue.get()
            proc = procs[name]
            proc.join()
            del procs[name]
            if curr < len(patternsTab):
                allDiversity[patternsTab[curr]] = [0.0, 1.0, 1.0]
                proc = mp.Process(target=evaluate_one_itemset_diversity, 
                               args=(queue, allDiversity, curr, patternsLabel, 
                                   patternsTab, coversSetTab, coversTab, seuil,))
                proc.start()
                procs[proc.name] = proc
                curr += 1
            
        print("\nEND OF THE EVALUATIONS")
    #return allDiversity

def write_final_results(outputFile, allDiversity, patternsLabel):
    with open(outputFile, 'w') as f:
        i = 0
        for itemset in allDiversity.keys():
            # [lb, jaccard, ub] = allDiversity[itemset]
            line = "[ " + patternsLabel[i] + " ] [ " + itemset + " ] "
            # line += "[ " + str(lb) + " " + str(jaccard) + " " + str(ub) + " ]"
            line += "[ " + str(allDiversity[itemset][0]) + " "
            line += str(allDiversity[itemset][1]) + " "
            line += str(allDiversity[itemset][2]) + " ]"
            f.write(line+"\n")
            i = i+1
        
    print("*** results written in file ***")


if __name__ == "__main__":
    print("\n##############################################")
    print("########## New diversity evaluation ##########")
    print("Date =", date.today(), "- Time =", datetime.now())
    resultsFile = sys.argv[1]
    evalFile = sys.argv[2]
    fmin = int(sys.argv[3])
    
    # patterns' label + patterns + covers (each pattern's cover is a string containing the transactions) 
    labelOfPatterns, itemsets, tabCoversSTR = parseResults(resultsFile)
    
    # we convert our string tab into a tab of set (each cover 
    # is a set of transaction, each transaction is an integer) 
    tabCoversSet = getAllCoversInt(tabCoversSTR)
    
    manager = mp.Manager()
    allDiversity = manager.dict()
    
    evaluate_all_itemsets_diversity(allDiversity, labelOfPatterns, itemsets, tabCoversSet, 
                                    tabCoversSTR, fmin) # will be change soon
    
    # outputPath = resultsFile.split(".")[0] + "_FINAL.txt"
    write_final_results(evalFile, allDiversity, labelOfPatterns)
    print("\n########## END ##########\n")
    

