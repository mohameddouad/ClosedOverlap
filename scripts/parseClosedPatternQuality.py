'''
Created on 22 janv. 2020

@author: Abdelkader Ouali
'''

from include import *

# program parameters
# methods = ["Closed", "ClosedDiversity"]
methods = ["ClosedDiversityTopK"]

jmax = "0.1"  # maximum jaccard-similarity threshold 
threads = "0"  # number of threads used by the global constraint
historyAggregator = "MAX"
branchStrategy = "MINCOV"
timeout = "86400s"
npr = 10

fthresholds = {
"BMS1.dat" : ["0.0016", "0.0015", "0.0014", "0.0012"],
"connect.dat" : ["0.4", "0.3", "0.2", "0.15"],
"german-credit.dat" : ["0.1", "0.01", "0.001", "0.025"],
"hepatitis.dat" : ["0.3", "0.2", "0.1"],
"mushroom.dat" : ["0.05", "0.02", "0.01", "0.005"],
"pumsb.dat" : [ "0.70", "0.4", "0.1"],
"retail.dat" : [ "0.1", "0.05", "0.01", "0.005", "0.003" ],
"T10I4D100K.dat" : [ "0.05", "0.01", "0.005" ],
"vote.dat" : ["0.1", "0.01", "0"],
"chess.dat" : ["0.4", "0.3", "0.2", "0.15"],
"heart-cleveland.dat" : [ "0.3", "0.2", "0.1", "0.05"],
"kr-vs-kp.dat" : ["0.4", "0.3", "0.2"],
"primary-tumor.dat" : [ "0.1", "0.01", "0"],
"splice1.dat" : [ "0.1", "0.05", "0.01" ],
"T40I10D100K.dat" : [ "0.1", "0.01", "0.005" ],
'ijcai16.dat': ["0.3", "0.2", "0.1"]
}

diversity_thresholds = ["0.2", "0.1"]

# tpk paramters 
kvals = ["1000", "1500", "2000", "2500", "3000"]
index_in_fthresholds = 2

# quality functions

def nbrTrans(absolute_input_dataset_file):
    with open(absolute_input_dataset_file, "r") as infile:
        nbr_trans = 0
        for line in infile:
            if line.rstrip() and line[0] != '@':
                nbr_trans += 1
        return nbr_trans

def loadDataset(absolute_dataset_filename):
    '''
    Important access on transactions starts from index 0
    '''
    dataset_items = []
    dataset_trans = []
    with open(absolute_dataset_filename, "r") as infile:
        for line in infile:
            if line.rstrip() and line[0] != '@':
                items = []
                for i in line.split(" "):
                    i = i.strip()
                    if i != '': 
                        items.append(i)
                        if i not in dataset_items:
                            dataset_items.append(i)
                dataset_trans.append(items)
    return dataset_items, dataset_trans

def evaluateQuality_Closed(queue, script_file_name, project_res_dir, config):
    try:
        # preparing directories
        absolute_dataset_res_dir = os.path.abspath(os.path.join(project_res_dir, "Closed", config[0].split('.')[0]))
        os.makedirs(absolute_dataset_res_dir, exist_ok=True)
        absolute_dataset_res_file = os.path.abspath(os.path.join(
                absolute_dataset_res_dir, config[0].split('.')[0] + "-" + config[1].replace(".", "v") + ".res"))
        
        absolute_dataset_quality_file = os.path.abspath(os.path.join(
                absolute_dataset_res_dir, config[0].split('.')[0] + "-" + config[1].replace(".", "v") + ".qual"))
        
        absolute_dataset_log_file = os.path.abspath(os.path.join(
                absolute_dataset_res_dir, config[0].split('.')[0] + "-" + config[1].replace(".", "v") + ".log"))
        
        absolute_script_file = os.path.abspath(os.path.join("scripts", script_file_name))
        
        # Getting the dataset file name
        if (not os.path.exists(absolute_dataset_res_file)):
            print("Error: needed files for launching are missing!")
            sys.exit(1)
        
        launch_log_file = open(absolute_dataset_log_file, "a")
        subprocess.run(["python3 '" + absolute_script_file + "' '" + absolute_dataset_res_file + 
                        "' '" + absolute_dataset_quality_file + "; echo \"Exit status: $?\" "], shell=True, check=True, 
                        stdout=launch_log_file, stderr=launch_log_file)        
    finally:
        queue.put(mp.current_process().name)


if __name__ == '__main__':
    all_ics_icd = []
    configs_closed = []
    configs_diversity = []
    for filename in os.listdir(project_data_dir):
        if filename.endswith(".dat"):
            if filename in fthresholds:
                for threshold in fthresholds[filename]:
                    absolute_dataset_file = os.path.abspath(os.path.join(project_data_dir, filename))
                    absolute_threshold = int(math.ceil(float(threshold) * nbrTrans(absolute_dataset_file)))
                    configs_diversity.append((filename, threshold, str(absolute_threshold), str(div), 
                                              str(historyAggregator), str(branchStrategy), str(threads), str(timeout)))
                    configs_closed.append((filename, threshold, str(absolute_threshold)))
                    
                    
    # launch a chunk of processes all at once
    curr = 0
    procs = dict()
    queue = mp.Queue()
    scriptFileName = "parseQuality.py"
    for i in range(0, npr):
        if curr < len(configs_closed):
            # launch
            print(configs_diversity[i][0], configs_closed[curr])
            proc = Process(target=evaluateQuality_Closed, args=(queue, scriptFileName, project_res_dir, configs_diversity[curr],))
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
        if curr < len(configs_closed):
            print(configs_diversity[i][0], configs_closed[curr])
            proc = Process(target=evaluateQuality_Closed, args=(queue, scriptFileName, project_res_dir, configs_diversity[curr],))
            proc.start()
            procs[proc.name] = proc
            curr += 1
    print("finished")
    
    sys.exit(0)

