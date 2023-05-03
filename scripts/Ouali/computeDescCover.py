'''
Created on 25 mars 2020

@author: Abdelkader Ouali
'''

from include import *

# number parallel launches
npr = 8

# program parameters
fthresholds = {
               "BMS1.dat" : ["0.0015", "0.0014", "0.0012"],
               "connect.dat" : ["0.3", "0.18", "0.17", "0.15"],
               "hepatitis.dat" : ["0.3", "0.2", "0.1"],
               "mushroom.dat" : ["0.05", "0.01", "0.008", "0.005"],
               "pumsb.dat" : [ "0.4", "0.3", "0.2"],
               "retail.dat" : [ "0.05", "0.01", "0.004"],
               "T10I4D100K.dat" : [ "0.05", "0.01", "0.005" ],
               "chess.dat" : ["0.4", "0.3", "0.2", "0.15"],
               "heart-cleveland.dat" : [ "0.2", "0.1", "0.08", "0.06"],
               "kr-vs-kp.dat" : ["0.4", "0.3", "0.2"],
               "splice1.dat" : [ "0.1", "0.05", "0.02", "0.01" ],
               "T40I10D100K.dat" : [ "0.1", "0.08", "0.05", "0.03", "0.01"],
               'ijcai16.dat': ["0.3", "0.2", "0.1"]
               }

timeout = "91800s"


def loadDataset(absolute_input_dataset_file):
    with open(absolute_input_dataset_file, "r") as infile:
        db = []
        for line in infile:
            tmp = line.strip().split()
            if tmp :
                db.append(tmp)
        return db


def loadPatterns(absolute_patterns_filename):
    descriptions = []
    with open(absolute_patterns_filename, "r") as infile:
        for line in infile:
            blocks = re.findall('\[(.*?)\]', line)
            assert(len(blocks) == 1)
            if len(blocks[0].strip()) != 0:  # avoid loading empty set
                descriptions.append(blocks[0].strip().split(" "))
    return descriptions


def computeSaveCover(queue, dataset, descriptions, absolute_dataset_new_res_file):
    try:
        with open(absolute_dataset_new_res_file, "w") as resfile:
            for desc in descriptions:
                cover = []
                desc_set = set(desc)
                for t in range(0, len(dataset)):
                    if desc_set.issubset(set(dataset[t])):
                        cover.append(t + 1)
                resfile.write("[ 0 ] [ ")
                for d in desc:
                    resfile.write(str(d) + " ")
                resfile.write("] [ ")
                for c in cover:
                    resfile.write(str(c) + " ")
                resfile.write("] [ 0 0 0 ]\n")    
    finally:
        queue.put(mp.current_process().name)   


# now parsing the results of the available methods, this method should be modified, unless a new method is added
if __name__ == '__main__':
    # prepare the different configurations
    configs = []
    for filename in os.listdir(project_data_dir):
        if filename.endswith(".dat"):
            if filename in fthresholds:
                for threshold in fthresholds[filename]:
                    # absolute_dataset_file = os.path.abspath(os.path.join(project_data_dir, filename))
                    configs.append((filename, threshold))
    # launch a chunk of processes all at once
    curr = 0
    curr_dataset = ""
    procs = dict()
    queue = mp.Queue()
    for i in range(0, npr):
        if curr < len(configs):
            if curr == 0 or configs[curr][0] != curr_dataset:
                absolute_dataset_file = os.path.abspath(os.path.join(project_data_dir, configs[curr][0]))
                dataset = loadDataset(absolute_dataset_file)
                curr_dataset = configs[curr][0]
            absolute_dataset_res_dir = os.path.abspath(os.path.join(project_res_dir, "foxrex", "Closed", configs[curr][0].split('.')[0]))
            absolute_dataset_res_file = os.path.abspath(os.path.join(absolute_dataset_res_dir, configs[curr][0].split('.')[0] + "-" + configs[curr][1].replace(".", "v") + ".res"))
            absolute_dataset_new_res_file = os.path.abspath(os.path.join(absolute_dataset_res_dir, configs[curr][0].split('.')[0] + "-" + configs[curr][1].replace(".", "v") + "-WITHCOVER" + ".res"))
            descriptions = loadPatterns(absolute_dataset_res_file)
            # launch
            proc = Process(target=computeSaveCover, args=(queue, dataset, descriptions, absolute_dataset_new_res_file,))
            proc.start()
            procs[proc.name] = proc
            curr += 1
    # using the queue, launch a new process whenever an old process finishes its workload
    while procs:
        name = queue.get()
        proc = procs[name]
        proc.join()
        del procs[name]
        if curr < len(configs):
            if curr == 0 or configs[curr][0] != curr_dataset:
                absolute_dataset_file = os.path.abspath(os.path.join(project_data_dir, configs[curr][0]))
                dataset = loadDataset(absolute_dataset_file)
                curr_dataset = configs[curr][0]
            absolute_dataset_res_dir = os.path.abspath(os.path.join(project_res_dir, "foxrex", "Closed", configs[curr][0].split('.')[0]))
            absolute_dataset_res_file = os.path.abspath(os.path.join(absolute_dataset_res_dir, configs[curr][0].split('.')[0] + "-" + configs[curr][1].replace(".", "v") + ".res"))
            absolute_dataset_new_res_file = os.path.abspath(os.path.join(absolute_dataset_res_dir, configs[curr][0].split('.')[0] + "-" + configs[curr][1].replace(".", "v") + "-WITHCOVER" + ".res"))
            descriptions = loadPatterns(absolute_dataset_res_file)
            # launch
            proc = Process(target=computeSaveCover, args=(queue, dataset, descriptions, absolute_dataset_new_res_file,))
            proc.start()
            procs[proc.name] = proc
            curr += 1
    print("finished")
