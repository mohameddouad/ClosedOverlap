'''
Created on 25 fev 2020

@author: Arnold Hien

Interpreter: Python 3
'''

from include import *
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
#               "BMS1.dat" : ["0.0015", "0.0014"],
#               "connect.dat" : ["0.4", "0.3", "0.2", "0.15"],
#               "german-credit.dat" : ["0.1", "0.025", "0.01", "0.001"],
                "hepatitis.dat" : ["0.2"]
#               "mushroom.dat" : ["0.05", "0.02", "0.01", "0.005"],
#               "pumsb.dat" : [ "0.70", "0.4", "0.1"],
#               "retail.dat" : [ "0.1", "0.05", "0.01", "0.005", "0.003",],
#               "T10I4D100K.dat" : [ "0.05", "0.01", "0.005" ],
#               "vote.dat" : ["0.1", "0.01", "0"],
#               "chess.dat" : ["0.4", "0.15"],
#               "heart-cleveland.dat" : [ "0.3", "0.2", "0.1", "0.05"],
#               "kr-vs-kp.dat" : ["0.4", "0.3", "0.2"],
#               "primary-tumor.dat" : [ "0.1", "0.01", "0"],
#               "splice1.dat" : [ "0.1", "0.05", "0.01" ],
#               "T40I10D100K.dat" : [ "0.1", "0.01", "0.005" ],
#               'ijcai16.dat': ["0.3", "0.2", "0.1"]
}
# """

# diversitythresholds = ["0.5", "0.4"]
diversitythresholds = ["0.1"]

# searchstrategies = ["FIRSTWITCOV", "MINWITCOV", "MINCOV", "DEFAULT"]
searchstrategies = ["FIRSTWITCOV"]

def nbrTrans(absolute_input_dataset_file):
    with open(absolute_input_dataset_file, "r") as infile:
        nbr_trans = 0
        for line in infile:
            if line.rstrip() and line[0] != '@':
                nbr_trans += 1
        return nbr_trans

def closedDiversityJaccardEvaluation(queue, script_file_name, project_res_dir, config):
    # Getting the dataset file name
    
    try:
        absolute_dataset_res_dir = os.path.abspath(os.path.join(project_res_dir, "ClosedDiversityNew", 
                                                                 config[0].split('.')[0]))
        
        absolute_dataset_res_file = os.path.abspath(os.path.join(
                absolute_dataset_res_dir, config[0].split('.')[0] + "-" + config[1].replace(".", "v") + 
                "-" + config[3].replace(".", "v") + "-" + aggreg + "-" + config[4] + "-0-" + timeout + ".res"))
        
        absolute_dataset_eval_file = os.path.abspath(os.path.join(
                absolute_dataset_res_dir, config[0].split('.')[0] + "-" + config[1].replace(".", "v") + 
                "-" + config[3].replace(".", "v") + "-" + aggreg + "-" + config[4] + "-0-" + timeout + ".eval"))
        
        absolute_dataset_log_file = os.path.abspath(os.path.join(
                absolute_dataset_res_dir, config[0].split('.')[0] + "-" + config[1].replace(".", "v") + 
                "-" + config[3].replace(".", "v") + "-" + aggreg + "-" + config[4] + "-0-" + timeout + ".log"))
        
        absolute_script_file = os.path.abspath(os.path.join(project_dir, "scripts", script_file_name))
        print(absolute_script_file)
        
        if (not os.path.exists(absolute_dataset_res_file)):
            print("Error: fmin =", config[3], "--> needed files for launching are missing!")
            print("Info: actual res file =", absolute_dataset_res_file, "\n")
            sys.exit(1)
        launch_log_file = open(absolute_dataset_log_file, "a")
        subprocess.run(["/usr/bin/timeout " + timeout + " python3 '" + absolute_script_file + 
                        "' '" + absolute_dataset_res_file + "' '" + absolute_dataset_eval_file + 
                        "' " + config[2] + "; echo \"Exit status: $?\" "], shell=True, check=True, 
                        stdout=launch_log_file, stderr=launch_log_file)
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
                    for div in diversitythresholds:
                        for strat in searchstrategies:
                            absolute_dataset_file = os.path.abspath(os.path.join(project_data_dir, filename))
                            absolute_threshold = int(math.ceil(float(threshold) * nbrTrans(absolute_dataset_file)))
                            configs.append((filename, threshold, str(absolute_threshold), div, strat))
                    #absolute_dataset_file = os.path.abspath(os.path.join(project_data_dir, filename))
                    #absolute_threshold = int(math.ceil(float(threshold) * nbrTrans(absolute_dataset_file)))
                    #files.append((filename, threshold, str(absolute_threshold)))
   
    # launch a chunk of processes all at once
    curr = 0
    procs = dict()
    queue = mp.Queue()
    scriptFileName = "jaccardsEvaluations.py"
    for i in range(0, npr):
        if curr < len(configs):
            # launch
            print(configs[i][0], configs[curr])
            proc = Process(target=closedDiversityJaccardEvaluation, args=(queue, scriptFileName, project_res_dir, configs[curr],))
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
            proc = Process(target=closedDiversityJaccardEvaluation, args=(queue, scriptFileName, project_res_dir, configs[curr],))
            proc.start()
            procs[proc.name] = proc
            curr += 1
    print("finished")
