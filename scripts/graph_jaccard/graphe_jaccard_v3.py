"""
Created on Wed Apr  1 12:21:29 2020
Update 31 May 2020 by Arnold

@author: hien
"""

from include_2 import *
import matplotlib.pyplot as plt
from datetime import date, datetime

#diversitythresholds = ["0.05", "0.1", "0.2", "0.25", "0.3", "0.35", "0.4", "0.45", "0.5", "0.6", "0.7"]
diversitythresholds = ["0.05", "0.2", "0.25"]

searchstrategies = ["MINCOV", "FIRSTWITCOV"]
# searchstrategies = ["MINCOV"]

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
    print("########## DRAWING GRAPHS  ########## ")
    print("Date =", date.today(), "- Time =", datetime.now())
    
    dataset_images_dir = sys.argv[1]
    dataset_name = sys.argv[2]
    fmin = sys.argv[3]
    aggreg = sys.argv[4]
    timeout = sys.argv[5]
    
    imageFile = os.path.abspath(os.path.join(dataset_images_dir, dataset_name, dataset_name + 
            "-" + fmin.replace(".", "v") + "-" + aggreg + "-0-" + timeout + ".png"))
    
    it = 1
    
    plt.figure(figsize=(10,3))
    
    for strat in range(0, len(searchstrategies)):
        debut_X = 0
        #dataset_res_dir = os.path.abspath(os.path.join(
        #        project_res_dir, "ClosedDiversityJMAXVar_"+searchstrategies[strat]+"_V2_estFreq", dataset_name))
        
        if searchstrategies[strat] == "MINCOV":
            dataset_res_dir = os.path.abspath(os.path.join(project_res_dir, 
                    project_res_dir, "ClosedDiversityJMAXVar_"+searchstrategies[strat]+"_V2_estFreq", dataset_name))
        else:
            dataset_res_dir = os.path.abspath(os.path.join(project_res_dir, 
                    project_res_dir, "ClosedDiversityJMAXVar_NewUB_"+searchstrategies[strat]+"_estFreq", dataset_name))
        
        for div in range(0, len(diversitythresholds)):
            evalFile = os.path.abspath(os.path.join(dataset_res_dir, dataset_name + 
                    "-" + fmin.replace(".", "v") + "-" + diversitythresholds[div].replace(".", "v") + 
                    "-" + aggreg + "-" + searchstrategies[strat] + "-0-" + timeout + ".eval"))
            
            if (not os.path.exists(evalFile)):
                continue
            
            fmin_2 = "" + str(100 * float(fmin)) + "%"
            jmax = "" + str(100 * float(diversitythresholds[div])) + "%"
            
            all_Patterns, all_LB, all_JAC, all_UB = parseEvalFile(evalFile)
            tab_diversity = np.array([all_LB, all_JAC, all_UB])
            tab_diversity = np.array([all_LB, all_JAC, all_UB]).transpose()
    
            # sort tab diversity by descending order of column 3 (UB)
            tab_diversity = tab_diversity[np.argsort(-tab_diversity[:, 2])]
            
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
                
                all_diff_jacc.append((diff_lb, diff_ub))
                
            all_diff_jacc = np.array(all_diff_jacc)
            
            y_lb = tab_diversity[:, 0]
            y_jac = tab_diversity[:, 1]
            y_ub = tab_diversity[:, 2]
            
            x = []
            y_jmax = []
            for i in range(0, len(y_lb)):
                x.append(i+1)
#                y_jmax.append(float(jmax))
                y_jmax.append(float(diversitythresholds[div]))
            
            titre = ""+searchstrategies[strat]+" - Jmax="+jmax
            plt.subplot(len(searchstrategies), len(diversitythresholds), it, title=titre)
            plt.scatter(x, y_lb, s=20, c='blue', marker='o')
            plt.scatter(x, y_jac, s=20, c='green', marker=(5, 2))
            plt.scatter(x, y_ub, s=20, c='orange', marker='+')
            plt.scatter(x, y_jmax, s=20, c='red', marker='_')
            
            # plt.plot(x, y_lb, 'o', label="LB", linewidth=2, linestyle="solid")
            # plt.plot(x, y_jac, 'x',  label="Jaccard", linewidth=2, linestyle="solid")
            # plt.plot(x, y_ub, '*', label="UB", linewidth=2, linestyle="solid")
            # plt.plot(x, y_jmax, label="JMAX", linewidth=2, linestyle="dotted")
            
            it = it+1
        
    
#    plt.rcParams['xtick.bottom'] = plt.rcParams['xtick.labelbottom'] = False
#    plt.rcParams['xtick.top'] = plt.rcParams['xtick.labeltop'] = True
#    plt.rcParams['xtick.top'] = True
    
#    plt.subplots_adjust(bottom=0.1, right=0.8, top=0.9)
#    plt.subplots_adjust(right=0.3, top=0.2)
    
#    titre = "" + dataset_name + " - Freq=" + fmin_2 + " - Jmax=" + jmax
#    plt.title(titre)
    
    fg = plt.gcf()
#    fg.tight_layout()
#    fg.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
    fg.set_size_inches(11, 6.5)
    
    plt.savefig(imageFile)
    
    print("\n########## Picture saved ##########\n")
    
