'''
Created on 22 déc. 2019

@author: ouali193
'''

from include import *

# parameters 
npr = 6  # number of parallel processes
'''
function 0 converts an arff file to transaction format without including the class.
function 1 increases the index of all items by 1. Our program requires an index starting from 1. 
'''
function = 1


def arff2trans(absolute_input_dataset_file, absolute_output_dataset_file):
    with open(absolute_input_dataset_file, "r") as infile, open(absolute_output_dataset_file, "w") as outfile:
        for line in infile:
            if line.rstrip() and line[0] != '@':
                for ele in line.split()[0:-1]:
                    outfile.write(ele + " ")
                outfile.write("\n")


def increaseItemsByOne(absolute_input_dataset_file, absolute_output_dataset_file):
    with open(absolute_input_dataset_file, "r") as infile, open(absolute_output_dataset_file, "w") as outfile:
        for line in infile:
                for ele in line.split():
                    new_ele = int(ele) + 1
                    outfile.write(str(new_ele) + " ")
                outfile.write("\n")


if __name__ == '__main__': 
    # checking required needed directories and configs 
    if function == 0:
        # input directory
        absolute_arff_dataset_dir = os.path.abspath(os.path.join(project_data_dir, "arff"))
        if (not os.path.exists(absolute_arff_dataset_dir)):
            print("Error: the data directory was not found")
            sys.exit(1)
        # loop on the dataset available in the data directory
        configs = []
        for filename in os.listdir(absolute_arff_dataset_dir):
            if filename.endswith(".txt"): 
                configs.append(filename)
        # making chunk of configs for a parallel launching 
        chunks = [configs[x:x + npr] for x in range(0, len(configs), npr)]
        # launch in parallel each chunk of datasets
        for chunk in chunks:
            procs = []
            for filename in chunk:
                # prepare paths
                absolute_input_dataset_file = os.path.abspath(os.path.join(absolute_arff_dataset_dir, filename))
                absolute_output_dataset_file = os.path.abspath(os.path.join(project_data_dir, filename.split('.')[0] + '.dat'))
                # launch
                proc = Process(target=arff2trans, args=(absolute_input_dataset_file, absolute_output_dataset_file,))
                proc.start()
                procs.append(proc)
            for proc in procs:
                    proc.join()
    elif function == 1:
        # input directory
        absolute_itemzero_dataset_dir = os.path.abspath(os.path.join(project_data_dir, "itemzero"))
        if (not os.path.exists(absolute_itemzero_dataset_dir)):
            print("Error: the data directory was not found")
            sys.exit(1)
        # loop on the dataset available in the data directory
        configs = []
        for filename in os.listdir(absolute_itemzero_dataset_dir):
            if filename.endswith(".dat"): 
                configs.append(filename)
        # making chunk of configs for a parallel launching 
        chunks = [configs[x:x + npr] for x in range(0, len(configs), npr)]
        # launch in parallel each chunk of datasets
        for chunk in chunks:
            procs = []
            for filename in chunk:
                # prepare paths
                absolute_input_dataset_file = os.path.abspath(os.path.join(absolute_itemzero_dataset_dir, filename))
                absolute_output_dataset_file = os.path.abspath(os.path.join(project_data_dir, filename))
                # launch
                proc = Process(target=increaseItemsByOne, args=(absolute_input_dataset_file, absolute_output_dataset_file,))
                proc.start()
                procs.append(proc)
            for proc in procs:
                    proc.join()
    else :
        print("Error: function's value not specified.")
        sys.exit(1)
            
