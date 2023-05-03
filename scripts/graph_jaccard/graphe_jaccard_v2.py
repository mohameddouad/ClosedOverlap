"""
Created on Wed Apr  1 12:21:29 2020
Update 31 May 2020 by Arnold

@author: hien
"""

from include import *
import matplotlib.pyplot as plt
from datetime import date, datetime

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
                lb.append(float(val[0]))
                jac.append(float(val[1]))
                ub.append(float(val[2]))
    
    return descriptions, lb, jac, ub


if __name__ == "__main__":
    print("\n##############################################")
    print("########## New-Diversity-Estimated-Frequency evaluation ##########")
    print("Date =", date.today(), "- Time =", datetime.now())
    evalFile = sys.argv[1]
    imageFile = sys.argv[2]
    dataset_name = sys.argv[3]
    fmin = sys.argv[4]
    jmax = sys.argv[5]
    
    freq = 100 * float(fmin)
    fmin_2 = "" + str(freq) + "%"
    
    jm = 100 * float(jmax)
    jmax_2 = "" + str(jm) + "%"
    
    all_Patterns, all_LB, all_JAC, all_UB = parseEvalFile(evalFile)
    
#    print(all_LB, "\n", all_JAC, "\n", all_UB, "\n\n")
    tab_diversity = np.array([all_LB, all_JAC, all_UB])
#    print("\n\n", tab_diversity)

    tab_diversity = np.array([all_LB, all_JAC, all_UB]).transpose()
#    print("\n\n", tab_diversity)
    
    # sort tab diversity by descending order of column 3 (UB)
    tab_diversity = tab_diversity[np.argsort(-tab_diversity[:, 2])]
#    print("\n\n", tab_diversity)
    
    # all_diff_jacc = np.array([[val_lb-val_jac, val_ub-val_jac] for val_lb, val_jac, val_ub in tab_diversity[:]])
    # all_diff_jacc = np.array([[(val_lb-val_jac)/(max(tab_diversity[:,0])-val_jac), (val_ub-val_jac)/(max(tab_diversity[:,2])-val_jac)] for val_lb, val_jac, val_ub in tab_diversity[:]])
    all_diff_jacc = []
    max_lb = max(tab_diversity[:,0])
    max_ub = max(tab_diversity[:,2])
    for i in range(0, len(tab_diversity)):
        val_lb = tab_diversity[i, 0]
        val_jac = tab_diversity[i, 1]
        val_ub = tab_diversity[i, 2]
        
        diff_lb = 1.0
        diff_ub = 1.0
        if max_lb != val_jac:
            c_lb = max_lb - val_jac
            diff_lb = (val_lb - val_jac) / c_lb
        if max_ub != val_jac:
            c_ub = max_ub - val_jac
            diff_ub = (val_ub - val_jac) / c_ub
        
#        diff_lb = (val_lb - val_jac) / c_lb
 #       diff_ub = (val_ub - val_jac) / c_ub
        all_diff_jacc.append((diff_lb, diff_ub))
    
    all_diff_jacc = np.array(all_diff_jacc)
#    print("\n\n", all_diff_jacc)
    
    # y_lb = all_diff_jacc[:, 0]
    y_lb = tab_diversity[:, 0]
    y_ub = tab_diversity[:, 2]
    y_jac = tab_diversity[:, 1]
    # y_ub = all_diff_jacc[:, 1]
    
#    x = []
#    for i in range(0, len(y_lb)):
#        x.append(i+1)
    x = []
    y_jmax = []
    for i in range(0, len(y_lb)):
        x.append(i+1)
        y_jmax.append(float(jmax))
    
#    x = [i for i in range(1, len(y_lb[:,0])+1)]
    
    plt.plot(x, y_lb, 'o', label="LB", linewidth=2, linestyle="solid")
    plt.plot(x, y_ub, '*', label="UB", linewidth=2, linestyle="solid")
    plt.plot(x, y_jac, 'x',  label="Jaccard", linewidth=2, linestyle="solid")
    plt.plot(x, y_jmax, label="JMAX", linewidth=2, linestyle="dotted")
    titre = dataset_name + " - fmin=" + fmin + " - jmax=" + jmax
    plt.title(titre)
    plt.xlabel("Patterns")
    plt.ylabel("Jaccard Values")
    plt.legend()
    
    plt.savefig(imageFile)
    
    print("\n########## Picture saved ##########\n")
    
