'''
Created on 25 fev 2020

@author: Arnold Hien

Interpreter: Python 3
'''

import sys
import matplotlib.pyplot as plt

def parseResults(filePath):
    with open(filePath, 'r') as f:
        content = f.readlines()
        allPatterns = []
        allCovers = []
        for line in content:
            # each line corresponds to a solution
            [allPartialPatterns, allPartialCover] = line.split("#")
            
            partialP = allPartialPatterns.split(" ] [ ")
            partialP[0] = partialP[0].replace("[ ", "")
            partialP[len(partialP)-1] = partialP[len(partialP)-1].replace(" ]", "")
            
            partialC = allPartialCover.split(" ] [ ")
            partialC[0] = partialC[0].replace("[ ", "")
            partialC[len(partialC)-1] = partialC[len(partialC)-1].replace(" ]\n", "")
            
            partialCovers = []
            partialPatterns = []
            for i in range(0, len(partialP)):
                # for all partial pattern that led to solution Si
                
                # store all partial patterns j
                items = set(map(int, set(partialP[i].split(" "))))
                partialPatterns.append(items)
                
                # store all partial patterns_j' cover
                transactions = set(map(int, set(partialC[i].split(" "))))
                partialCovers.append(transactions)
                
            # for each solution (a complete pattern) we store all the 
            # intermediate pattern
            allPatterns.append(partialPatterns)
            allCovers.append(partialCovers)
    
    return allPatterns, allCovers

def parseHistoryFile(filePath):
    with open(filePath, 'r') as f:
        content = f.readlines()
        
        allHistoryPatterns = []
        allHistoryCovers = []
        for line in content:
            elements = line.split(" ]#[ ")
            elements[0] = elements[0].replace("[ ", "")
            elements[len(elements)-1] = elements[len(elements)-1].replace(" ]", "")
            
            allHistoryPatterns.append(set(map(
                    int, set(elements[0].split(" "))))) 
            allHistoryCovers.append(set(map(
                    int, set(elements[len(elements)-1].split(" ")))))
    
    return allHistoryPatterns, allHistoryCovers

def writeFinalResults(outputFile, finalData):
    with open(outputFile, 'w') as f:
        for line in finalData:
            f.write(line+"\n")
        
    print("*** Fin de l'écriture ***\n")

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
    denom = len(covX) + len(covP_X) + len(covY) - seuil
    lb = 0
    if(num > 0):
        lb = num/denom
    
    return lb

def evaluate_UB_Jaccard(covX, covY, seuil):
    covP_X = covX.difference(covY)
    ub = (len(covX) - len(covP_X)) / (seuil + len(covP_X))
    
    return ub

def solution_i_diversity(partialPatternsCovers, historyCoverTab, seuil):
    allLB = []
    allJaccard = []
    allUB = []
    
    for covX in partialPatternsCovers:
        lb_jaccard = 0.0
        jaccard_value = 0.0
        ub_jaccard = 0.0
        
        for covHi in historyCoverTab:
            lb = evaluate_LB_Jaccard(covX, covHi, seuil)
            jaccard = evaluate_Jaccard(covX, covHi)
            ub = evaluate_UB_Jaccard(covX, covHi, seuil)
            
            lb = max(lb, 0.0)
            ub = min(ub, 1.0)
            
            lb_jaccard = max(lb_jaccard, lb)
            jaccard_value = max(jaccard_value, jaccard)
            ub_jaccard = max(ub_jaccard, ub)
            
        allLB.append(lb_jaccard)
        allJaccard.append(jaccard_value)
        allUB.append(ub_jaccard)
    
    return allLB, allJaccard, allUB

def all_solutions_diversity(allSolutionsTab, allSolutionsCoversTab, 
              historyPatternTab, historyCoverTab, seuil):
    allSolutionsLBTab = []
    allSolutionsJaccardTab = []
    allSolutionsUBTab = []
    
    for i in range(0, len(allSolutionsTab)):
        lb_i, jaccard_i, ub_i = solution_i_diversity(allSolutionsCoversTab[i], 
                                                     historyCoverTab, seuil)
        
        allSolutionsLBTab.append(lb_i)
        allSolutionsJaccardTab.append(jaccard_i)
        allSolutionsUBTab.append(ub_i)
    
    return allSolutionsLBTab, allSolutionsJaccardTab, allSolutionsUBTab


if __name__ == "__main__":
    
    resultsFile = sys.argv[1]
    historyFile = sys.argv[2]
    fmin = int(sys.argv[3])
    indice = int(sys.argv[4])
    
    # patterns' label + patterns + covers (each pattern's cover is a string 
    # containing the transactions) 
    tabOfPatterns, tabOfCovers = parseResults(resultsFile)
    if indice >= len(tabOfPatterns):
        print("Error: there is less than {} solutions".format(indice))
        print("Error: the number of solutions is {}".format(len(tabOfPatterns)))
        print("Error: give an indice beetween 1 and {} \n".format(len(tabOfPatterns)))
        sys.exit(1)
    elif indice == 0:
        print("Info: please, give an indice beetween 1 and {} \n".format(len(tabOfPatterns)))
        sys.exit(1)
    
    tabOfHistoryPatterns, tabOfHistoryCovers = parseHistoryFile(historyFile)
    LBs, Jaccards, UBs = all_solutions_diversity(tabOfPatterns, tabOfCovers, 
                                                 tabOfHistoryPatterns, 
                                                 tabOfHistoryCovers, fmin)
    
    itemsets = tabOfPatterns[indice]
    lbs = LBs[indice]
    jac = Jaccards[indice]
    ubs = UBs[indice]
    
    itemsets.reverse()
    lbs.reverse()
    jac.reverse()
    ubs.reverse()
    
    nbElement = len(itemsets)
    x = range(0, nbElement)
    
    
    plt.plot(x, lbs, 'x', label="LB des motifs", 
             linewidth=2, linestyle="solid")
    plt.plot(x, jac, 'o', label="Jaccard des motifs", 
             linewidth=2, linestyle="solid")
    plt.plot(x, ubs, '*', label="UB des motifs", 
             linewidth=2, linestyle="solid")
    
    for i in range(nbElement):
        plt.annotate(list(itemsets[i]), xy=(i, 0.4), xytext=(i, 0.45), rotation=90)
    
    plt.title("Valeurs de diversité des motifs")
    plt.legend()
    plt.show()
    
    print("\n***** END *****\n.....")
    
