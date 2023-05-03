'''
Created on 23 juil. 2020

@author: ouali193
'''

from include import *

fthresholds = {
               "BMS1.dat" : ["0.0015", "0.0014", "0.0012"],
               "connect.dat" : ["0.4", "0.3", "0.18", "0.17", "0.15"],
               "hepatitis.dat" : ["0.3", "0.2", "0.1"],
               "mushroom.dat" : ["0.05", "0.01", "0.008", "0.005"],
               "pumsb.dat" : [ "0.4", "0.3", "0.2"],
               "retail.dat" : [ "0.05", "0.01", "0.004" ],
               "T10I4D100K.dat" : [ "0.05", "0.01", "0.005" ],
               "chess.dat" : ["0.4", "0.3", "0.2", "0.15", "0.1"],
               "heart-cleveland.dat" : [ "0.2", "0.1", "0.08", "0.06"],
               "kr-vs-kp.dat" : ["0.4", "0.3", "0.2"],
               "splice1.dat" : [ "0.1", "0.05", "0.02", "0.01" ],
               "T40I10D100K.dat" : [ "0.1", "0.08", "0.05", "0.03", "0.01" ],
               "ijcai16.dat": ["0.1", "0.2", "0.3"]
               }
machine = "foxrex"  # working machine

# extract the number of solutions
version = "ClosedDiversity_2"
jmax = "0.1"  # maximum jaccard-similarity threshold
threads = "0"  # number of threads used by the global constraint
historyAggregator = "MAX"
branchStrategy = "MINCOV"
cdtimeout = "91800s"
jmax = "0.1"

work = "ijcai16"
lp_model = "0"
optimization = "-min"
kmin = "3"  # default value
kmax = "20"  # default value
objective = "4"
timeout = "86400"


def lenFile(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
        return i + 1
    return 0
# or  num_lines = sum(1 for line in open('myfile.txt'))


def loadPatterns(absolute_patterns_filename, all_info=False):
    descriptions = []
    coverages = []
    witness = []
    ub_jac_lb = []
    with open(absolute_patterns_filename, "r") as infile:
        for line in infile:
            blocks = re.findall('\[(.*?)\]', line)
            if len(blocks) == 4:
                if len(blocks[1].strip()) != 0:  # avoid loading empty set
                    descriptions.append(blocks[1].strip().split(" "))
                    # we should start from index 0 instead of index 1 that is provided in the file
                    coverage = []
                    for t in blocks[2].strip().split(" "):
                        coverage.append(int(t) - 1)
                    coverages.append(coverage)
                    witness.append(int(blocks[0]))
                    ub_jac_lb.append(blocks[3].strip().split(" "))
            elif len(blocks) == 3:
                if len(blocks[0].strip()) != 0:  # avoid loading empty set
                    descriptions.append(blocks[0].strip().split(" "))
                    # we should start from index 0 instead of index 1 that is provided in the file
                    coverage = []
                    for t in blocks[1].strip().split(" "):
                        coverage.append(int(t))
                    coverages.append(coverage)     
            else:
                print("Error unknown *.res format")
                sys.exit(1)
                
    if all_info:
        return descriptions, coverages, witness, ub_jac_lb
    else:
        return descriptions, coverages


def convertPatternFile(absolute_patterns_cd_file, absolute_patterns_psmlp_file):
    descriptions, coverages = loadPatterns(absolute_patterns_cd_file)
    with open(absolute_patterns_psmlp_file, "w") as outfile:
        for p in range(0, len(descriptions)):
            outfile.write("[ ")
            for i in  descriptions[p]:
                outfile.write(str(i) + " ")
            outfile.write("] [ ") 
            for t in  coverages[p]:
                outfile.write(str(t) + " ")
            outfile.write("] [ ]\n")


if __name__ == '__main__':
    
    # print date and time
    timenow = datetime.datetime.now()
    print(timenow.strftime("%d/%m/%Y %H:%M:%S"), work, lp_model, optimization, objective, timeout)
    # checking required directories and files
    if (not os.path.exists(project_psm_lp_bin)):
        print("Error: the patterset binary file was not found")
        sys.exit(1) 
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
                absolute_dataset_file = os.path.abspath(os.path.join(project_data_dir, filename))
                for threshold in fthresholds[filename]:
                    absolute_dataset_res_dir = os.path.abspath(os.path.join(project_res_dir, version + "_" + branchStrategy, filename.split('.')[0]))
                    absolute_dataset_patterns_file = os.path.abspath(os.path.join(absolute_dataset_res_dir, filename.split('.')[0] + "-" + threshold.replace(".", "v") + "-" + jmax.replace(".", "v") + "-" + historyAggregator + "-" + branchStrategy + "-" + threads + "-" + cdtimeout + ".res"))
                    if (os.path.exists(absolute_dataset_patterns_file)):
                        # convert the file for psmlp
                        absolute_psmlp_patterns_file = os.path.abspath(os.path.join(absolute_dataset_res_dir, filename.split('.')[0] + "-" + threshold.replace(".", "v") + "-" + jmax.replace(".", "v") + "-" + historyAggregator + "-" + branchStrategy + "-" + threads + "-" + cdtimeout + ".ptr"))
                        if not os.path.exists(absolute_psmlp_patterns_file):
                            convertPatternFile(absolute_dataset_patterns_file, absolute_psmlp_patterns_file)
                        # getting the number of diversified closed patterns found by the strategy
                        k = lenFile(absolute_psmlp_patterns_file)
                        kmin = kmax = str(k)  # remove the empty space
                        # set the directories for PSMLP
                        absolute_dataset_sol_dir = os.path.abspath(os.path.join(project_res_dir, machine, "PSMLP", filename.split('.')[0]))
                        if not os.path.exists(absolute_dataset_sol_dir):
                            os.makedirs(absolute_dataset_sol_dir, exist_ok=True)                                                                 
                        absolute_dataset_sol_file = os.path.abspath(os.path.join(absolute_dataset_sol_dir, filename.split('.')[0] + "-" + threshold.replace(".", "v") + "-" + work + "-" + lp_model + "-" + optimization + "-" + kmin + "-" + kmax + "-" + objective + "-" + timeout + ".sol"))
                        absolute_dataset_log_file = os.path.abspath(os.path.join(absolute_dataset_sol_dir, filename.split('.')[0] + "-" + threshold.replace(".", "v") + "-" + work + "-" + lp_model + "-" + optimization + "-" + kmin + "-" + kmax + "-" + objective + "-" + timeout + ".log"))          
                        configs.append((absolute_dataset_file, absolute_psmlp_patterns_file, absolute_dataset_sol_file, absolute_dataset_log_file, kmin, kmax))
    # launch a chunk of processes all at once
    for config in configs:
        print(project_psm_lp_bin + " --conference " + work + " --lp-model " + lp_model + " --database-file " + config[0] + " --patterns-file " + config[1] + " " + optimization + " --k-min " + config[4] + " --k-max " + config[5] + " --output-file " + config[2] + " --objective-function " + objective + " --cplex-timeout " + timeout)
        launch_log_file = open(config[3], "w")
        subprocess.run([project_psm_lp_bin + " --conference " + work + " --lp-model " + lp_model + " --database-file " + config[0] + " --patterns-file " + config[1] + " " + optimization + " --k-min " + config[4] + " --k-max " + config[5] + " --output-file " + config[2] + " --objective-function " + objective + " --cplex-timeout " + timeout + " ; echo \"Exit status: $?\" "], shell=True, check=True, stdout=launch_log_file, stderr=launch_log_file)
        subprocess.run(["chmod 770 -R " + os.path.abspath(os.path.join(config[2], os.path.pardir))], shell=True, check=True)
        
    print("finished")

