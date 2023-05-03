'''
Created on 12 avril 2020

@author: Arnold Hien

'''

from include import *
import multiprocessing as mp

# number parallel launches
npr = 2

# program parameters 
fthresholds = {
               "chess.fimi" : ["0.4"]
#               "BMS1.fimi" : ["0.0015", "0.0014", "0.0012"],
#2               "connect.fimi" : ["0.3", "0.18", "0.17", "0.15"],
#2               "hepatitis.fimi" : ["0.3", "0.2", "0.1"],
#               "mushroom.fimi" : ["0.05", "0.01", "0.008", "0.005"],
#2               "pumsb.fimi" : [ "0.4", "0.3", "0.2"],
#               "retail.fimi" : [ "0.05", "0.01", "0.004"],
#1**               "T10I4D100K.fimi" : [ "0.05", "0.01", "0.005" ],
#3**               "chess.fimi" : ["0.4", "0.3", "0.2", "0.15", "0.1"],
#               "heart-cleveland.fimi" : [ "0.2", "0.1", "0.08", "0.06"],
#1**               "kr-vs-kp.fimi" : ["0.4", "0.3", "0.2", "0.1"],
#               "splice1.fimi" : [ "0.1", "0.05", "0.02", "0.01" ],
#               "T40I10D100K.fimi" : [ "0.1", "0.08", "0.05", "0.03", "0.01" ]
#**: finished
               }

minLengthThresholds = {
               "BMS1.fimi" : ["1", "2", "3", "5", "8", "10"],
               "connect.fimi" : ["1", "2", "3", "5", "8", "10"],
#               "german-credit.fimi" : ["1", "2", "3", "5", "8", "10"],
               "hepatitis.fimi" : ["1", "2", "3", "5", "8", "10"],
               "mushroom.fimi" : ["1", "2", "3", "5", "8", "10"],
               "pumsb.fimi" : ["1", "2", "3", "5", "8", "10"],
               "retail.fimi" : ["1", "2", "3", "5", "8", "10"],
               "T10I4D100K.fimi" : ["1", "2", "3", "5", "8", "10"],
#               "vote.fimi" : ["1", "2", "3", "5", "8", "10"],
               "chess.fimi" : ["1", "2", "3", "5", "8", "10"],
               "heart-cleveland.fimi" : ["1", "2", "3", "5", "8", "10"],
               "kr-vs-kp.fimi" : ["1", "2", "3", "5", "8", "10"],
#               "primary-tumor.fimi" : ["1", "2", "3", "5", "8", "10"],
               "splice1.fimi" : ["1", "2", "3", "5", "8", "10"],
               "T40I10D100K.fimi" : ["1", "2", "3", "5", "8", "10"],
               "ijcai16.fimi": ["1", "2", "3", "5", "8", "10"]
               }

allSamples = {
               "BMS1.fimi" : ["609", "668", "823"],
               "connect.fimi" : ["18", "197", "272", "509"],
               "hepatitis.fimi" : ["12", "57", "2270"],
               "mushroom.fimi" : ["727", "12139", "15715", "27768"],
               "pumsb.fimi" : ["4", "15", "52"],
               "retail.fimi" : ["13", "111", "528"],
               "T10I4D100K.fimi" : ["11", "361", "617"],
               "chess.fimi" : ["5", "16", "96", "393", "4204"],
               "heart-cleveland.fimi" : ["81", "3496", "12842", "58240"],
               "kr-vs-kp.fimi" : ["5", "17", "96", "4120"],
#               "splice1.fimi" : ["422", "8781", "", ""],
               "T40I10D100K.fimi" : ["83", "127", "288", "598", "7402"]

               }

oracle = "gflexics"
qualityMeasure = "frequency" # it can be "uniform" or "purity" 

constraintParameter = "F,C" # F -> minFreq, L -> minLength, C -> Closed -- They can be combined : example -> F,C means closed with a certain minimum frequency

taskTODO = "sample"

#error_tolerance = ["0.9", "0.5", "0.1"] # error tolerance
error_tolerance = ["0.5", "0.1"]
#error_tolerance = ["0.1"] # error tolerance

numberOfSample = "20"

timeout = "91800s"

def nbrTrans(absolute_input_dataset_file):
    with open(absolute_input_dataset_file, "r") as infile:
        nbr_trans = 0
        for line in infile:
            if line.rstrip() and line[0] != '@':
                nbr_trans += 1
        return nbr_trans


def flexics(queue, project_flexics_script_file, project_data_dir, project_res_dir, config):
    '''
    config is a list of (filename, freq_threshold, absolute_freq_threshold, jmax, historyAggregator, branchStrategy, number_threads and timeout))
    '''
    try:
        # preparing directories
        absolute_dataset_file = os.path.abspath(os.path.join(project_data_dir, config[0]))
        absolute_dataset_res_dir = os.path.abspath(os.path.join(project_res_dir, "Flexics", "GFlexics", config[0].split('.')[0]))
        os.makedirs(absolute_dataset_res_dir, exist_ok=True)
        
        constr = constraintParameter.replace(",", "-")
        
        # absolute_dataset_temp_res_file = os.path.abspath(os.path.join(absolute_dataset_res_dir, config[0].split('.')[0] + "-" + config[4].replace(".", "v") + "-" + config[1] + "-" + config[2] + "-" + config[3].replace(",", "-") + "-" + config[5] + "-" + config[6].replace(".", "v") + "-" + config[7] + "-" + config[8] + ".txt"))
        absolute_dataset_temp_res_file = os.path.abspath(os.path.join(absolute_dataset_res_dir, config[0].split('.')[0] + "-" + config[1] + "-" + config[2] + "-" + config[4].replace(".", "v") + "-" + constr + "-" + config[5] + "-" + config[6].replace(".", "v") + "-" + config[7] + "-" + config[8] + ".txt"))
        
        # absolute_dataset_res_file = os.path.abspath(os.path.join(absolute_dataset_res_dir, config[0].split('.')[0] + "-" + config[4].replace(".", "v") + "-" + config[1] + "-" + config[2] + "-" + config[3].replace(",", "-") + "-" + config[5] + "-" + config[6].replace(".", "v") + "-" + config[7] + "-" + config[8] + ".res"))
        absolute_dataset_res_file = os.path.abspath(os.path.join(absolute_dataset_res_dir, config[0].split('.')[0] + "-" + config[1] + "-" + config[2] + "-" + config[4].replace(".", "v") + "-" + constr + "-" + config[5] + "-" + config[6].replace(".", "v") + "-" + config[7] + "-" + config[8] + ".res"))
        
        # absolute_dataset_log_file = os.path.abspath(os.path.join(absolute_dataset_res_dir, config[0].split('.')[0] + "-" + config[4].replace(".", "v") + "-" + config[1] + "-" + config[2] + "-" + config[3].replace(",", "-") + "-" + config[5] + "-" + config[6].replace(".", "v") + "-" + config[7] + "-" + config[8] + ".log"))
        absolute_dataset_log_file = os.path.abspath(os.path.join(absolute_dataset_res_dir, config[0].split('.')[0] + "-" + config[1] + "-" + config[2] + "-" + config[4].replace(".", "v") + "-" + constr + "-" + config[5] + "-" + config[6].replace(".", "v") + "-" + config[7] + "-" + config[8] + ".log"))
        
        # absolute_time_log_file = os.path.abspath(os.path.join(absolute_dataset_res_dir, config[0].split('.')[0] + "-" + config[4].replace(".", "v") + "-" + config[1] + "-" + config[2] + "-" + config[4].replace(".", "v") + "-" + constr + "-" + config[5] + "-" + config[6].replace(".", "v") + "-" + config[7] + "-" + config[8] + ".time"))
        absolute_time_log_file = os.path.abspath(os.path.join(absolute_dataset_res_dir, config[0].split('.')[0] + "-" + config[1] + "-" + config[2] + "-" + config[4].replace(".", "v") + "-" + constr + "-" + config[5] + "-" + config[6].replace(".", "v") + "-" + config[7] + "-" + config[8] + ".time"))
        
        # Getting the dataset file name
        if not os.path.exists(project_flexics_script_file):
            print("Error: needed script files for launching are missing!")
            print("Script file location : ", project_flexics_script_file, "\n")
            sys.exit(1)
        if not os.path.exists(absolute_dataset_file):
            print("Error: needed dataset files for launching are missing!")
            sys.exit(1)
        
        launch_log_file = open(absolute_dataset_log_file, "w")
        print("/usr/bin/timeout " + config[8] + " bash " + project_flexics_script_file + "  " + config[1] + " " + config[2] + " " + config[0] + " " + config[3] + " " + config[5] + " " + config[6] + " " + config[7])
        
        # subprocess.run(["time /usr/bin/timeout " + config[8] + " bash " + project_flexics_script_file + " " + config[1] + " " + config[2] + " " + config[0] + " " + config[3] + " " + config[5] + " " + config[6] + " " + config[7] + "; java -jar fin.jar > '" + absolute_dataset_temp_res_file + "'; echo \" \nExit status: $?\" "], shell=True, check=True, stdout=launch_log_file, stderr=launch_log_file)
        subprocess.run(["/usr/bin/timeout " + config[8] + " /usr/bin/time -v -o " + absolute_time_log_file + " bash " + project_flexics_script_file + " " + config[1] + " " + config[2] + " " + config[0] + " " + config[3] + " " + config[5] + " " + config[6] + " " + config[7] + " > '" + absolute_dataset_temp_res_file + "'; echo \" \nExit status: $?\" "], shell=True, check=True, stdout=launch_log_file, stderr=launch_log_file)
        
    finally:
        queue.put(mp.current_process().name)    


def postProcessFlexicsResults(queue, project_flexics_script_file, project_res_dir, config):
    try:
        # preparing directories
        absolute_dataset_res_dir = os.path.abspath(os.path.join(project_res_dir, "Flexics", "GFlexics", config[0].split('.')[0]))
        os.makedirs(absolute_dataset_res_dir, exist_ok=True)
        
        constr = constraintParameter.replace(",", "-")
        
        # absolute_dataset_temp_res_file = os.path.abspath(os.path.join(absolute_dataset_res_dir, config[0].split('.')[0] + "-" + config[4].replace(".", "v") + "-" + config[1] + "-" + config[2] + "-" + config[3].replace(",", "-") + "-" + config[5] + "-" + config[6].replace(".", "v") + "-" + config[7] + "-" + config[8] + ".txt"))
        absolute_dataset_temp_res_file = os.path.abspath(os.path.join(absolute_dataset_res_dir, config[0].split('.')[0] + "-" + config[1] + "-" + config[2] + "-" + config[4].replace(".", "v") + "-" + constr + "-" + config[5] + "-" + config[6].replace(".", "v") + "-" + config[7] + "-" + config[8] + ".txt"))
        
        # absolute_dataset_res_file = os.path.abspath(os.path.join(absolute_dataset_res_dir, config[0].split('.')[0] + "-" + config[4].replace(".", "v") + "-" + config[1] + "-" + config[2] + "-" + config[3].replace(",", "-") + "-" + config[5] + "-" + config[6].replace(".", "v") + "-" + config[7] + "-" + config[8] + ".res"))
        absolute_dataset_res_file = os.path.abspath(os.path.join(absolute_dataset_res_dir, config[0].split('.')[0] + "-" + config[1] + "-" + config[2] + "-" + config[4].replace(".", "v") + "-" + constr + "-" + config[5] + "-" + config[6].replace(".", "v") + "-" + config[7] + "-" + config[8] + ".res"))
        
        # absolute_dataset_log_file = os.path.abspath(os.path.join(absolute_dataset_res_dir, config[0].split('.')[0] + "-" + config[4].replace(".", "v") + "-" + config[1] + "-" + config[2] + "-" + config[3].replace(",", "-") + "-" + config[5] + "-" + config[6].replace(".", "v") + "-" + config[7] + "-" + config[8] + ".log"))
        absolute_dataset_log_file = os.path.abspath(os.path.join(absolute_dataset_res_dir, config[0].split('.')[0] + "-" + config[1] + "-" + config[2] + "-" + config[4].replace(".", "v") + "-" + constr + "-" + config[5] + "-" + config[6].replace(".", "v") + "-" + config[7] + "-" + config[8] + ".log"))
        
        if not os.path.exists(project_flexics_postprocess_file):
            print("Error: needed files for launching are missing!")
            print("postprocess script file missing : ", project_flexics_postprocess_file, "\n")
            sys.exit(1)
        
        if not os.path.exists(absolute_dataset_temp_res_file):
            print("Error: needed files for launching are missing!")
            print("res file missing : ", absolute_dataset_temp_res_file, "\n")
            sys.exit(1)
        
        launch_log_file = open(absolute_dataset_log_file, "a")
        # print("\n**********************************\n\n POST-PROCESS FLEXICS File\n")
        print("python3 " + project_flexics_postprocess_file + " '" + absolute_dataset_temp_res_file + "' '" + absolute_dataset_res_file)
        subprocess.run(["python3 " + project_flexics_postprocess_file + " '" + absolute_dataset_temp_res_file + "' '" + absolute_dataset_res_file + "'; echo \" \nExit status: $?\" "], shell=True, check=True, stdout=launch_log_file, stderr=launch_log_file)
        
    finally:
        queue.put(mp.current_process().name)    


if __name__ == '__main__':
    
    # print date and time
    # timenow = datetime.datetime.now()
    # print(timenow.strftime("%d/%m/%Y %H:%M:%S"), npr, timeout, jmax,historyAggregator, branchStrategy, threads, fthresholds)
    # checking required needed directories and files 
    if (not os.path.exists(project_flexics_data_dir)):
        print("Error: the data directory was not found")
        # print(project_flexics_data_dir)
        sys.exit(1)
    if (not os.path.exists(project_res_dir)):
        os.makedirs(project_res_dir, exist_ok=True)
    # prepare the different configurations
    configs = []
    for filename in os.listdir(project_flexics_data_dir):
        if filename.endswith(".cp4im") or filename.endswith(".fimi"):
            if filename in fthresholds:
                absolute_dataset_file = os.path.abspath(os.path.join(project_flexics_data_dir, filename))
                # for threshold in fthresholds[filename]:
                for i in range(0, len(fthresholds[filename])):
                    # absolute_threshold = int(math.ceil(float(threshold) * nbrTrans(absolute_dataset_file)))
                    absolute_threshold = int(math.ceil(float(fthresholds[filename][i]) * nbrTrans(absolute_dataset_file)))
                    for kappa in error_tolerance:
                        constraint = constraintParameter.replace("F", "F"+str(absolute_threshold))
                        
                        if "L" in constraint:
                            for minLength in minLengthThresholds[filename]:
                                constraint = constraint.replace("L", "L"+minLength)
                                # configs.append((filename, taskTODO, oracle, constraint, threshold, qualityMeasure, kappa, numberOfSample, str(timeout)))
                                configs.append((filename, taskTODO, oracle, constraint, fthresholds[filename][i], qualityMeasure, kappa, allSamples[filename][i], str(timeout)))
                        else:
                            # configs.append((filename, taskTODO, oracle, constraint, threshold, qualityMeasure, kappa, numberOfSample, str(timeout)))
                            configs.append((filename, taskTODO, oracle, constraint, fthresholds[filename][i], qualityMeasure, kappa, allSamples[filename][i], str(timeout)))
                            
    
    print("\n***** CONFIGS *****\n")
    print("", configs, "\n")
    print("\n***** Launch FLEXICS process *****\n")
    
    # launch all flexics processes one after another
    curr = 0
    procs = dict()
    queue = mp.Queue()
    for i in range(0, npr):
        if curr < len(configs):
            # launch
            print(configs[i][0], configs[curr])
            proc = Process(target=flexics, args=(queue, project_flexics_script_file, project_flexics_data_dir, project_res_dir, configs[curr],))
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
            proc = Process(target=flexics, args=(queue, project_flexics_script_file, project_flexics_data_dir, project_res_dir, configs[curr],))
            proc.start()
            procs[proc.name] = proc
            curr += 1
    
    # launch all flexics post-processes one after another
    # print("\n\n")
    print("\n***** POST PROCESS *****\n")
    #"""
    curr = 0
    procs = dict()
    queue = mp.Queue()
    for i in range(0, npr):
        if curr < len(configs):
            # launch
            print(configs[i][0], configs[curr])
            proc = Process(target=postProcessFlexicsResults, args=(queue, postProcessFlexicsResults, project_res_dir, configs[curr],))
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
            proc = Process(target=postProcessFlexicsResults, args=(queue, postProcessFlexicsResults, project_res_dir, configs[curr],))
            proc.start()
            procs[proc.name] = proc
            curr += 1
    #"""
    print("\n\n***** All flexics XPs finished *****\n***********************************\n\n")
