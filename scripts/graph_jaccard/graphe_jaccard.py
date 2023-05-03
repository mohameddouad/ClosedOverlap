#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 12:21:29 2020

@author: hien
"""

from include import *
import matplotlib as plt

def parseEvalFile(absolute_dataset_eval_file):
    descriptions = []
    lb = []
    ub = []
    jac = []
    with open(absolute_dataset_eval_file, "r") as infile:
        for line in infile:
            blocks = re.findall('\[(.*?)\]', line)
            assert(len(blocks) == 3)
            if len(blocks[1].strip()) != 0:  # avoid loading empty set
                descriptions.append(blocks[1].strip().split(" "))
                
                val = blocks[2].strip().split(" ")
                lb = float(val[0])
                jac = float(val[1])
                ub = float(val[2])
    
    return descriptions, lb, jac, ub


def sort_by_ub(description, lbs, jacs, ubs):
    


if __name__ == "__main__":
    print("\n##############################################")
    print("########## New diversity evaluation ##########")
    print("Date =", date.today(), "- Time =", datetime.now())
    evalFile = sys.argv[1]
    imageFile = sys.argv[2]
    fmin = sys.argv[3]
    jmax = sys.argv[4]
    
    
    all_Patterns, all_LB, all_JAC, all_UB = parseEvalFile(evalFile)
    
    tab_diversity = np.array([all_LB, all_JAC, all_UB]).transpose()
    
    # sort tab diversity by descending order of column 3 (UB)
    tab_diversity = tab_diversity[np.argsort(-tab_diversity[:, 2])]
    
    # all_diff_jacc = np.array([[val_lb-val_jac, val_ub-val_jac] for val_lb, val_jac, val_ub in tab_diversity[:]])
    all_diff_jacc = np.array([[(val_lb-val_jac)/(max(tab_diversity[:,0])-val_jac), 
                               (val_ub-val_jac)/(max(tab_diversity[:,2])-val_jac)] 
                               for val_lb, val_jac, val_ub in tab_diversity[:]])
    
    y_lb = all_diff_jacc[:, 0]
    y_ub = all_diff_jacc[:, 1]
    x = [i for i in range(1, len(y_lb[:,0])+1)]
    
    plt.plot(x, y_lb, 'o', label="LB", linewidth=2, linestyle="solid")
    plt.plot(x, y_ub, 'o', label="UB", linewidth=2, linestyle="solid")
    titre = "Valeurs de diversité des motifs - fmin=" + fmin + " - jmax=" + jmax
    plt.title(titre)
    plt.legend()
    
    plt.savefig(imageFile)
    
    print("\n########## Picture saved ##########\n")
    
