'''
Created on 11 janv. 2020

@author: Abdelkader Ouali
'''

from include import *

for dataset in os.listdir(project_data_dir):
    if dataset.endswith(".dat"):
        data_name = dataset.split('.')[0]
        absolute_dataset_filename = os.path.abspath(os.path.join(project_data_dir, dataset))
        with open(absolute_dataset_filename, "r") as infile:
            nbr_trans = 0
            items = []
            presents = 0
            for line in infile:
                if line.rstrip() and line[0] != '@':
                    for i in line.split(" "):
                        i = i.strip()
                        if i != '': 
                            if i not in items:
                                items.append(i)
                            presents += 1
                    nbr_trans += 1
            print(data_name, '&', nbr_trans, '&', len(items), '&', '{0:.2f}'.format(float((presents / (nbr_trans * len(items)))*100)), '\\\\\\hline')
