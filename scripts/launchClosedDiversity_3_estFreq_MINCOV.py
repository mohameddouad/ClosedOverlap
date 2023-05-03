'''
Created on 20 févr. 2020

@author: Abdelkader Ouali
update: Arnold Hien (09/03/2020)

'''

from include import *
import multiprocessing as mp

# number parallel launches
npr = 6 
# program parameters 
fthresholds = {
               "BMS1.dat" : ["0.0015", "0.0014", "0.0012"],
               "connect.dat" : ["0.4", "0.3", "0.18", "0.17", "0.15", "0.10"],
#               "german-credit.dat" : ["0.1", "0.01", "0.001", "0.025"],
               "hepatitis.dat" : ["0.3", "0.2", "0.1", "0.05"],
               "mushroom.dat" : ["0.05", "0.01", "0.008", "0.005"],
               "pumsb.dat" : [ "0.4", "0.3", "0.2", "0.1" ],
               "retail.dat" : [ "0.05", "0.01", "0.004" ],
               "T10I4D100K.dat" : [ "0.05", "0.01", "0.005" ],
#               "vote.dat" : ["0.1", "0.01", "0"],
               "chess.dat" : ["0.4", "0.3", "0.2", "0.15", "0.1", "0.05"],
               "heart-cleveland.dat" : [ "0.2", "0.1", "0.08", "0.06"],
               "kr-vs-kp.dat" : ["0.4", "0.3", "0.2", "0.1", "0.05"],
#               "primary-tumor.dat" : [ "0.1", "0.01", "0"],
               "splice1.dat" : [ "0.1", "0.05", "0.02", "0.01" ],
               "T40I10D100K.dat" : [ "0.1", "0.08", "0.05", "0.03", "0.01" ],
               "ijcai16.dat": ["0.3", "0.2", "0.1"]
               }

jmax = "0.05"  # maximum jaccard-similarity threshold
threads = "0"  # number of threads used by the global constraint
historyAggregator = "MAX"
branchStrategy = "MINCOV"
timeout = "91800s"

def nbrTrans(absolute_input_dataset_file):
    with open(absolute_input_dataset_file, "r") as infile:
        nbr_trans = 0
        for line in infile:
            if line.rstrip() and line[0] != '@':
                nbr_trans += 1
        return nbr_trans


def closedDiversity(queue, project_bin_file, project_data_dir, project_res_dir, config):
    '''
    config is a list of (filename, freq_threshold, absolute_freq_threshold, jmax, historyAggregator, branchStrategy, number_threads and timeout))
    '''
    try:
        # preparing directories
        absolute_dataset_file = os.path.abspath(os.path.join(project_data_dir, config[0]))
        absolute_dataset_res_dir = os.path.abspath(os.path.join(project_res_dir, "ClosedDiversity_3_estFreq_MINCOV", config[0].split('.')[0]))
        os.makedirs(absolute_dataset_res_dir, exist_ok=True)
        absolute_dataset_res_file = os.path.abspath(os.path.join(absolute_dataset_res_dir, config[0].split('.')[0] + "-" + config[1].replace(".", "v") + "-" + config[3].replace(".", "v") + "-" + config[4] + "-" + config[5] + "-" + config[6] + "-" + config[7] + ".res"))
        absolute_dataset_ana_file = os.path.abspath(os.path.join(absolute_dataset_res_dir, config[0].split('.')[0] + "-" + config[1].replace(".", "v") + "-" + config[3].replace(".", "v") + "-" + config[4] + "-" + config[5] + "-" + config[6] + "-" + config[7] + ".ana"))
        absolute_dataset_log_file = os.path.abspath(os.path.join(absolute_dataset_res_dir, config[0].split('.')[0] + "-" + config[1].replace(".", "v") + "-" + config[3].replace(".", "v") + "-" + config[4] + "-" + config[5] + "-" + config[6] + "-" + config[7] + ".log"))
        # Getting the dataset file name
        if (not os.path.exists(project_bin_file) or not os.path.exists(absolute_dataset_file)):
            print("Error: needed files for launching are missing!")
            sys.exit(1)
        launch_log_file = open(absolute_dataset_log_file, "w")
        print("/usr/bin/timeout " + config[7] + " java -jar " + project_bin_file + "  '" + absolute_dataset_file + "' '" + absolute_dataset_res_file + "' '" + absolute_dataset_ana_file + "' -f " + config[2] + " -j " + config[3] + " -ag " + config[4] + " -s " + config[5] + " -th " + config[6])
        subprocess.run(["/usr/bin/timeout " + config[7] + " java -jar " + project_bin_file + "  '" + absolute_dataset_file + "' '" + absolute_dataset_res_file + "' '" + absolute_dataset_ana_file + "' -f " + config[2] + " -j " + config[3] + " -ag " + config[4] + " -s " + config[5] + " -th " + config[6] + "; echo \"Exit status: $?\" "], shell=True, check=True, stdout=launch_log_file, stderr=launch_log_file)
	subprocess.run(["/bin/chmod 770 -R " + absolute_dataset_res_dir], shell=True, check=True)
    finally:
        queue.put(mp.current_process().name)    


if __name__ == '__main__':
    
    # print date and time
    timenow = datetime.datetime.now()
    print(timenow.strftime("%d/%m/%Y %H:%M:%S"), npr, timeout, jmax,historyAggregator, branchStrategy, threads, fthresholds)
    # checking required needed directories and files 
    if (not os.path.exists(project_data_dir)):
        print("Error: the data directory was not found")
        sys.exit(1)
    if (not os.path.exists(project_res_dir)):
        os.makedirs(project_res_dir, exist_ok=True)
    # prepare the different configurations
    configs = []
    for filename in os.listdir(project_data_dir):
        if filename.endswith(".dat"):
            if filename in fthresholds:
                for threshold in fthresholds[filename]:
                    absolute_dataset_file = os.path.abspath(os.path.join(project_data_dir, filename))
                    absolute_threshold = int(math.ceil(float(threshold) * nbrTrans(absolute_dataset_file)))
                    configs.append((filename, threshold, str(absolute_threshold), str(jmax), str(historyAggregator), str(branchStrategy), str(threads), str(timeout)))
    # launch a chunk of processes all at once
    curr = 0
    procs = dict()
    queue = mp.Queue()
    for i in range(0, npr):
        if curr < len(configs):
            # launch
            print(configs[i][0], configs[curr])
            proc = Process(target=closedDiversity, args=(queue, project_bin_closed_diversity_3_file, project_data_dir, project_res_dir, configs[curr],))
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
            proc = Process(target=closedDiversity, args=(queue, project_bin_closed_diversity_3_file, project_data_dir, project_res_dir, configs[curr],))
            proc.start()
            procs[proc.name] = proc
            curr += 1
    print("finished")
    # subprocess.run(["/bin/chmod 770 -R " + project_res_dir], shell=True, check=True)