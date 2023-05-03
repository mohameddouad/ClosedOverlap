"""
Created on Wed Apr  1 11:50:57 2020

@author: hien
"""

from include_2 import *
import multiprocessing as mp

# number parallel launches
npr = 5
timeout = "91800s"

# program parameters
smax = "0.3"  # maximum jaccard-similarity threshold 
aggreg = "MAX" # the aggregation function
searchH = "MINCOV" # the search heuristic
nbThreads = "20" # thenumber of threads


fthresholds = {
#                "BMS1.dat" : ["0.0016", "0.0015", "0.0014", "0.0012"],
                "connect.dat" : ["0.4"],
                "hepatitis.dat" : ["0.2"],
                "mushroom.dat" : ["0.05"],
                "pumsb.dat" : ["0.4"],
                "retail.dat" : ["0.05"],
                "T10I4D100K.dat" : [ "0.05"],
                "chess.dat" : ["0.4"],
                "heart-cleveland.dat" : [ "0.2"],
                "kr-vs-kp.dat" : ["0.4"],
                "splice1.dat" : [ "0.1" ],
                "T40I10D100K.dat" : [ "0.05" ]
}
# """

# diversitythresholds = ["0.5", "0.4"]
diversitythresholds = ["0.1"]

# searchstrategies = ["FIRSTWITCOV", "MINWITCOV", "MINCOV", "DEFAULT"]
# searchstrategies = ["MINCOV"]
searchstrategies = ["FIRSTWITCOV"]


def nbrTrans(absolute_input_dataset_file):
    with open(absolute_input_dataset_file, "r") as infile:
        nbr_trans = 0
        for line in infile:
            if line.rstrip() and line[0] != '@':
                nbr_trans += 1
        return nbr_trans

def closedDiversityJaccardGraph(queue, script_file_name, project_res_dir, config):
    # Getting the dataset file name
    
    try:
#        absolute_dataset_images_dir = os.path.abspath(os.path.join(project_dir, "images", 
#                "ClosedDiversityJMAXVar_V2_estFreq"))
        absolute_dataset_images_dir = os.path.abspath(os.path.join(project_dir, "images", 
                "ClosedDiversityJMAXVar_estFreq", config[0].split('.')[0]))
        
        absolute_dataset_log_file = os.path.abspath(os.path.join(absolute_dataset_images_dir, config[0].split('.')[0] + 
                "-" + config[1].replace(".", "v") + "-" + aggreg + "-0-" + timeout + ".log"))

#        absolute_script_file = os.path.abspath(os.path.join(project_dir, "scripts", "graph_jaccard", script_file_name))
        absolute_script_file = os.path.abspath(os.path.join(project_dir, "scripts", script_file_name))
        
#        if (not os.path.exists(absolute_dataset_eval_file)):
#            print("Error: fmin =", config[3], "--> needed files for launching are missing!")
#            print("Info: actual given eval file =", absolute_dataset_eval_file, "\n")
#            sys.exit(1)
        
        if (not os.path.exists(absolute_dataset_images_dir)):
            os.makedirs(absolute_dataset_images_dir, exist_ok=True)
        
        launch_log_file = open(absolute_dataset_log_file, "w")
        subprocess.run(["/usr/bin/timeout " + timeout + " python3 '" + absolute_script_file + "' '" + absolute_dataset_images_dir + 
                         "' " + config[0].split('.')[0] + " " + config[1] + " " + aggreg + " " + timeout + 
                         "; echo \"Exit status: $?\" "], shell=True, check=True, stdout=launch_log_file, stderr=launch_log_file)
        
        
    finally:
        queue.put(mp.current_process().name)
    

if __name__ == "__main__":
    # checking required needed directories and files 
    if (not os.path.exists(project_data_dir)):
        print("Error: the data directory was not found")
        sys.exit(1)
    if (not os.path.exists(project_bin_closed_diversity_new_file)):
        print("Error: the project binary file was not found")
        print("Info: compile first the project using mvn package")
        sys.exit(1)  
    if (not os.path.exists(project_res_dir)):
        os.makedirs(project_res_dir, exist_ok=True)
    # loop on the dataset available in the data directory
    configs = []
    for filename in os.listdir(project_data_dir):
        if filename.endswith(".dat"):
            if filename in fthresholds:
                for threshold in fthresholds[filename]:
                    # absolute_dataset_file = os.path.abspath(os.path.join(project_data_dir, filename))
                    # absolute_threshold = int(math.ceil(float(threshold) * nbrTrans(absolute_dataset_file)))
                    # configs.append((filename, threshold, str(absolute_threshold)))
                    
                    configs.append((filename, threshold))
   
    # launch a chunk of processes all at once
    curr = 0
    procs = dict()
    queue = mp.Queue()
    scriptFileName = "graphe_jaccard_v4.py"
    for i in range(0, npr):
        if curr < len(configs):
            # launch
            print(configs[i][0], configs[curr])
            proc = Process(target=closedDiversityJaccardGraph, args=(queue, scriptFileName, project_res_dir, configs[curr],))
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
            proc = Process(target=closedDiversityJaccardGraph, args=(queue, scriptFileName, project_res_dir, configs[curr],))
            proc.start()
            procs[proc.name] = proc
            curr += 1
    print("finished")
